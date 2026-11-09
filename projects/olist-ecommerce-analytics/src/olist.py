from pathlib import Path
import pandas as pd

FILES = {
    "orders": "olist_orders_dataset.csv",
    "items": "olist_order_items_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "translation": "product_category_name_translation.csv",
}

def load_dataset(data_dir="data/raw"):
    root = Path(data_dir)
    missing = [filename for filename in FILES.values() if not (root / filename).exists()]
    if missing:
        raise FileNotFoundError(
            "Kaggle CSV files are missing from data/raw: " + ", ".join(missing)
            + ". Download and extract https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce"
        )
    frames = {}
    for key, filename in FILES.items():
        # Reviews may contain text with non-UTF8 bytes in some distributed copies.
        try:
            frames[key] = pd.read_csv(root / filename)
        except UnicodeDecodeError:
            frames[key] = pd.read_csv(root / filename, encoding="latin1")
    return frames

def prepare_orders(frames):
    orders = frames["orders"].copy()
    items = frames["items"].copy()
    payments = frames["payments"].copy()
    customers = frames["customers"].copy()
    products = frames["products"].copy()
    reviews = frames["reviews"].copy()
    translation = frames["translation"].copy()

    for col in ["order_purchase_timestamp", "order_delivered_customer_date",
                "order_estimated_delivery_date"]:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")

    # Aggregate each one-to-many child table to order grain before joining.
    item_order = items.groupby("order_id", as_index=False).agg(
        item_revenue=("price", "sum"),
        freight_value=("freight_value", "sum"),
        item_count=("order_item_id", "count"),
        unique_products=("product_id", "nunique"),
    )
    payment_order = payments.groupby("order_id", as_index=False).agg(
        paid_value=("payment_value", "sum"),
        payment_records=("payment_sequential", "count"),
        max_installments=("payment_installments", "max"),
    )
    review_order = reviews.groupby("order_id", as_index=False).agg(
        review_score=("review_score", "mean"),
        review_count=("review_id", "nunique"),
    )

    product_names = products[["product_id", "product_category_name"]].merge(
        translation, on="product_category_name", how="left"
    )
    product_names["product_category_name_english"] = (
        product_names["product_category_name_english"].fillna(
            product_names["product_category_name"].fillna("unknown")
        )
    )
    category_by_order = items.merge(
        product_names[["product_id", "product_category_name_english"]],
        on="product_id", how="left"
    ).groupby("order_id", as_index=False).agg(
        primary_category=("product_category_name_english",
                          lambda s: s.mode().iloc[0] if not s.mode().empty else "unknown")
    )

    result = (orders
        .merge(customers[["customer_id", "customer_state"]], on="customer_id", how="left")
        .merge(item_order, on="order_id", how="left")
        .merge(payment_order, on="order_id", how="left")
        .merge(review_order, on="order_id", how="left")
        .merge(category_by_order, on="order_id", how="left"))

    result["is_delivered"] = result["order_status"].eq("delivered")
    result["is_late"] = (
        result["is_delivered"]
        & result["order_delivered_customer_date"].notna()
        & result["order_estimated_delivery_date"].notna()
        & (result["order_delivered_customer_date"] > result["order_estimated_delivery_date"])
    )
    result["delivery_days"] = (
        result["order_delivered_customer_date"] - result["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    result["purchase_month"] = result["order_purchase_timestamp"].dt.to_period("M").astype("string")
    result["item_revenue"] = result["item_revenue"].fillna(0)
    result["freight_value"] = result["freight_value"].fillna(0)
    return result

def calculate_kpis(orders):
    eligible = orders[~orders["order_status"].isin(["canceled", "unavailable"])]
    delivered = orders[orders["is_delivered"]]
    return {
        "orders": int(eligible["order_id"].nunique()),
        "gmv": float(eligible["item_revenue"].sum()),
        "freight": float(eligible["freight_value"].sum()),
        "aov": float(eligible["item_revenue"].sum() / eligible["order_id"].nunique())
            if eligible["order_id"].nunique() else 0.0,
        "late_rate": float(delivered["is_late"].mean()) if len(delivered) else 0.0,
        "avg_review": float(orders["review_score"].mean()) if orders["review_score"].notna().any() else 0.0,
    }
