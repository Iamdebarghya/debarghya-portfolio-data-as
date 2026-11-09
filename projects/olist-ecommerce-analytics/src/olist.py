from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
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
        try:
            frames[key] = pd.read_csv(root / filename)
        except UnicodeDecodeError:
            frames[key] = pd.read_csv(root / filename, encoding="latin1")
    return frames


def load_dataset_from_zip(uploaded_zip):
    """Read the required Olist CSVs directly from a user-uploaded Kaggle ZIP."""
    frames = {}
    with ZipFile(uploaded_zip) as archive:
        members = {Path(name).name: name for name in archive.namelist() if name.lower().endswith(".csv")}
        missing = [filename for filename in FILES.values() if filename not in members]
        if missing:
            raise ValueError("ZIP is missing required CSV files: " + ", ".join(missing))
        for key, filename in FILES.items():
            raw = archive.read(members[filename])
            try:
                frames[key] = pd.read_csv(BytesIO(raw))
            except UnicodeDecodeError:
                frames[key] = pd.read_csv(BytesIO(raw), encoding="latin1")
    return frames

def _category_items(frames):
    items = frames["items"].copy()
    products = frames["products"][["product_id", "product_category_name"]]
    translation = frames["translation"]
    product_names = products.merge(translation, on="product_category_name", how="left")
    product_names["category"] = (
        product_names["product_category_name_english"]
        .fillna(product_names["product_category_name"]).fillna("unknown")
    )
    return items.merge(product_names[["product_id", "category"]], on="product_id", how="left")

def prepare_category_revenue(frames, eligible_order_ids=None):
    """Return item-grain category revenue, not a representative category per order."""
    rows = _category_items(frames)
    if eligible_order_ids is not None:
        rows = rows[rows["order_id"].isin(eligible_order_ids)]
    return rows.groupby("category", as_index=False).agg(
        item_revenue=("price", "sum"),
        order_count=("order_id", "nunique"),
        item_count=("order_id", "size"),
    ).sort_values("item_revenue", ascending=False)

def prepare_orders(frames):
    orders = frames["orders"].copy()
    items = frames["items"].copy()
    payments = frames["payments"].copy()
    customers = frames["customers"].copy()
    reviews = frames["reviews"].copy()
    for col in ["order_purchase_timestamp", "order_delivered_customer_date",
                "order_estimated_delivery_date"]:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")

    item_order = items.groupby("order_id", as_index=False).agg(
        item_revenue=("price", "sum"), freight_value=("freight_value", "sum"),
        item_count=("order_item_id", "count"), unique_products=("product_id", "nunique"))
    payment_order = payments.groupby("order_id", as_index=False).agg(
        paid_value=("payment_value", "sum"), payment_records=("payment_sequential", "count"),
        max_installments=("payment_installments", "max"))
    review_order = reviews.groupby("order_id", as_index=False).agg(
        review_score=("review_score", "mean"), review_count=("review_id", "nunique"))

    result = (orders
        .merge(customers[["customer_id", "customer_state"]], on="customer_id", how="left")
        .merge(item_order, on="order_id", how="left")
        .merge(payment_order, on="order_id", how="left")
        .merge(review_order, on="order_id", how="left"))
    result["is_delivered"] = result["order_status"].eq("delivered")
    has_dates = (result["order_delivered_customer_date"].notna()
                 & result["order_estimated_delivery_date"].notna())
    result["has_delivery_dates"] = result["is_delivered"] & has_dates
    result["is_late"] = (result["has_delivery_dates"] &
                         (result["order_delivered_customer_date"] > result["order_estimated_delivery_date"]))
    result["purchase_month"] = result["order_purchase_timestamp"].dt.to_period("M").astype("string")
    result["delivery_days"] = (
        result["order_delivered_customer_date"] - result["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    result["item_revenue"] = result["item_revenue"].fillna(0)
    result["freight_value"] = result["freight_value"].fillna(0)
    return result

def calculate_kpis(orders):
    eligible = orders[~orders["order_status"].isin(["canceled", "unavailable"])]
    delivered = orders[orders["is_delivered"]]
    dated = delivered[delivered["has_delivery_dates"]] if "has_delivery_dates" in delivered else delivered
    return {
        "orders": int(eligible["order_id"].nunique()),
        "gmv": float(eligible["item_revenue"].sum()),
        "freight": float(eligible["freight_value"].sum()),
        "aov": float(eligible["item_revenue"].sum() / eligible["order_id"].nunique())
            if eligible["order_id"].nunique() else 0.0,
        "late_rate": float(dated["is_late"].mean()) if len(dated) else 0.0,
        "avg_review": float((orders["review_score"].fillna(0) * orders["review_count"].fillna(0)).sum() / orders["review_count"].sum())
            if orders["review_count"].sum() else 0.0,
    }
