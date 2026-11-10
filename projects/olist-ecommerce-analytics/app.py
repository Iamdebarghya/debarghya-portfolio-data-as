import streamlit as st
import plotly.express as px
from src.olist import load_dataset, load_dataset_from_zip, prepare_orders, prepare_category_revenue, calculate_kpis

st.set_page_config(page_title="Olist E-commerce Analytics", page_icon="📦", layout="wide")
st.title("Brazilian E-commerce | Business Performance")
st.caption("Analysis of Olist's anonymised public commercial dataset (2016–2018).")
st.sidebar.header("Dataset")
uploaded_zip = st.sidebar.file_uploader("Upload Olist Kaggle ZIP", type=["zip"],
    help="Upload the original Brazilian E-Commerce Public Dataset ZIP. The app reads it in memory.")
try:
    frames = load_dataset_from_zip(uploaded_zip) if uploaded_zip else load_dataset()
    data = prepare_orders(frames)
except Exception as exc:
    st.warning(f"Dataset not loaded: {exc}")
    st.markdown("[Download the Olist Kaggle dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)")
    st.info("Upload the ZIP in the sidebar. The raw data is processed in memory and is not committed to GitHub.")
    st.stop()

months = sorted(data["purchase_month"].dropna().unique().tolist())
states = sorted(data["customer_state"].dropna().unique().tolist())
with st.sidebar:
    st.header("Filters")
    selected_months = st.multiselect("Purchase month", months, default=months)
    selected_states = st.multiselect("Customer state", states, default=states)
    statuses = sorted(data["order_status"].dropna().unique().tolist())
    selected_statuses = st.multiselect("Order status", statuses, default=statuses)
filtered = data[data["purchase_month"].isin(selected_months)
    & data["customer_state"].isin(selected_states)
    & data["order_status"].isin(selected_statuses)]
k = calculate_kpis(filtered)
c1,c2,c3,c4 = st.columns(4)
c1.metric("Eligible orders", f"{k['orders']:,}")
c2.metric("Item GMV", f"R$ {k['gmv']:,.0f}")
c3.metric("Average order value", f"R$ {k['aov']:,.2f}")
c4.metric("Late delivery rate", f"{k['late_rate']:.1%}")
st.caption("GMV uses item prices, excluding freight. Late-delivery rate uses only delivered orders with both delivery dates.")

monthly = filtered.dropna(subset=["purchase_month"]).groupby("purchase_month",as_index=False)["item_revenue"].sum()
if not monthly.empty:
    st.subheader("Monthly item revenue")
    st.plotly_chart(px.line(monthly,x="purchase_month",y="item_revenue",markers=True,
        labels={"purchase_month":"Month","item_revenue":"Item revenue (BRL)"}),use_container_width=True)

left,right = st.columns(2)
eligible_ids = set(filtered.loc[~filtered["order_status"].isin(["canceled","unavailable"]),"order_id"])
category = prepare_category_revenue(frames,eligible_ids).nlargest(12,"item_revenue")
left.subheader("Top product categories")
left.plotly_chart(px.bar(category,x="item_revenue",y="category",orientation="h",
    labels={"item_revenue":"Item revenue (BRL)","category":"Category"}),use_container_width=True)
state = filtered.groupby("customer_state",as_index=False)["item_revenue"].sum().nlargest(15,"item_revenue")
right.subheader("Revenue by customer state")
right.plotly_chart(px.bar(state,x="customer_state",y="item_revenue",
    labels={"customer_state":"State","item_revenue":"Item revenue (BRL)"}),use_container_width=True)

st.subheader("Delivery and customer experience")
delivered = filtered[filtered["is_delivered"]]
d1,d2 = st.columns(2)
d1.metric("Average delivery time",f"{delivered['delivery_days'].mean():.1f} days" if delivered["delivery_days"].notna().any() else "N/A")
d2.metric("Average review score",f"{k['avg_review']:.2f} / 5" if k["avg_review"] else "N/A")
review_rows = delivered.dropna(subset=["review_score","delivery_days"])
if not review_rows.empty:
    plot_data = review_rows.assign(delivery_status=review_rows.apply(lambda row: "Late" if row["is_late"] else ("On time" if row["has_delivery_dates"] else "Estimated date missing"), axis=1))
    st.plotly_chart(px.box(plot_data,x="delivery_status",y="review_score",points="outliers",
        labels={"delivery_status":"Delivery status","review_score":"Review score"}),use_container_width=True)
st.download_button("Download filtered order-level data",filtered.to_csv(index=False).encode("utf-8-sig"),
    "olist_filtered_orders.csv","text/csv")
st.caption("Category revenue is calculated from item-level rows, avoiding one-category-per-order attribution.")
