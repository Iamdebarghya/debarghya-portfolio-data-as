import io
import re
import urllib.request

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="LogiFlow | Delivery Intelligence", page_icon="🚚", layout="wide")

GOLD = "#D6AE52"
BG = "#111111"
PANEL = "#1D1D1D"
DATA_URL = "https://raw.githubusercontent.com/dikagra123/Last-Mile-Delivery-Project/main/Delivery_Logistics.csv"

st.markdown("""
<style>
.stApp {background:#111111;color:#F2EBDD}
[data-testid="stMetric"] {background:#1D1D1D;border:1px solid #5C4A27;padding:16px;border-radius:12px}
[data-testid="stMetricLabel"] {color:#B6AA91}
[data-testid="stMetricValue"] {color:#D6AE52}
section[data-testid="stSidebar"] {background:#181818}
h1,h2,h3 {color:#F2EBDD}
.small-note {color:#B6AA91;font-size:0.86rem}
</style>
""", unsafe_allow_html=True)

st.title("🚚 LogiFlow | Delivery Intelligence")
st.caption("Last-mile delivery performance • Public-data portfolio project • Power BI-inspired interactive analytics")

@st.cache_data(show_spinner=False)
def load_remote(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        raw = response.read()
    return pd.read_csv(io.BytesIO(raw))

def norm(s):
    return re.sub(r"[^a-z0-9]+", "", str(s).lower())

ALIASES = {
    "delivery_partner": ["delivery_partner", "partner", "carrier", "logistics_partner"],
    "package_type": ["package_type", "package"],
    "vehicle_type": ["vehicle_type", "vehicle"],
    "delivery_mode": ["delivery_mode", "shipping_mode", "mode"],
    "region": ["region", "delivery_region"],
    "weather": ["weather", "weather_condition", "condition"],
    "distance_km": ["distance_km", "distance", "distanceinkm"],
    "package_weight_kg": ["package_weight_kg", "weight_kg", "package_weight", "weight"],
    "delivery_time_hours": ["delivery_time_hours", "actual_delivery_time", "actual_time_hours"],
    "expected_time_hours": ["expected_time_hours", "expected_delivery_time", "expected_time"],
    "delayed": ["delayed", "is_delayed", "delay_status"],
    "delivery_rating": ["delivery_rating", "rating", "customer_rating"],
    "delivery_cost": ["delivery_cost", "cost", "shipping_cost"],
    "delivery_id": ["delivery_id", "order_id", "shipment_id"],
}

def map_columns(df):
    lookup = {norm(c): c for c in df.columns}
    ren = {}
    for canonical, candidates in ALIASES.items():
        for candidate in candidates:
            if norm(candidate) in lookup:
                ren[lookup[norm(candidate)]] = canonical
                break
    return df.rename(columns=ren)

def numeric_hours(series):
    # Handles ordinary numeric hour values and malformed 1970 epoch-like values.
    n = pd.to_numeric(series, errors="coerce")
    if n.notna().mean() > 0.8:
        return n
    dt = pd.to_datetime(series, errors="coerce")
    if dt.notna().mean() > 0.5:
        ns = dt.astype("int64", errors="ignore")
        # Timestamp's epoch nanoseconds are the original numeric hour values in this source.
        return pd.Series(np.where(dt.notna(), ns / 1e9, np.nan), index=series.index)
    extracted = series.astype(str).str.extract(r"1970-01-01 00:00:00\.(\d+)")[0]
    return pd.to_numeric(extracted, errors="coerce") / 1e9

def prepare(raw):
    df = map_columns(raw.copy())
    for col in ["distance_km", "package_weight_kg", "delivery_time_hours", "expected_time_hours", "delivery_rating", "delivery_cost"]:
        if col in df:
            if col in ["delivery_time_hours", "expected_time_hours"]:
                df[col] = numeric_hours(df[col])
            else:
                df[col] = pd.to_numeric(df[col], errors="coerce")
    if "delayed" in df:
        if df["delayed"].dtype == object:
            df["delayed"] = df["delayed"].astype(str).str.strip().str.lower().map({
                "1":1,"true":1,"yes":1,"y":1,"delayed":1,
                "0":0,"false":0,"no":0,"n":0,"on time":0,"ontime":0
            })
        else:
            df["delayed"] = pd.to_numeric(df["delayed"], errors="coerce")
    if "delivery_time_hours" in df and "expected_time_hours" in df:
        df["delay_hours"] = df["delivery_time_hours"] - df["expected_time_hours"]
        df["calculated_delay_flag"] = (df["delay_hours"] > 0).astype("Int64")
    if "delayed" in df:
        df["delayed"] = df["delayed"].fillna(0).astype(int)
        df["delivery_status"] = np.where(df["delayed"] == 1, "Delayed", "On time")
    if "distance_km" in df and "delivery_cost" in df:
        df["cost_per_km"] = np.where(df["distance_km"] > 0, df["delivery_cost"] / df["distance_km"], np.nan)
    df = df.drop_duplicates().reset_index(drop=True)
    df.insert(0, "row_id", np.arange(1, len(df) + 1))
    return df

with st.sidebar:
    st.header("Data source")
    uploaded = st.file_uploader("Upload Delivery_Logistics.csv", type=["csv"])
    use_remote = st.checkbox("Try public source URL automatically", value=True)
    st.caption("The source CSV is hosted in the original public GitHub project. If that URL is unavailable, upload the CSV manually.")

raw = None
load_error = None
if uploaded is not None:
    raw = pd.read_csv(uploaded)
elif use_remote:
    try:
        with st.spinner("Loading public delivery dataset..."):
            raw = load_remote(DATA_URL)
    except Exception as exc:
        load_error = str(exc)

if raw is None:
    st.warning("Dataset could not be loaded automatically. Upload the original Delivery_Logistics.csv using the sidebar.")
    if load_error:
        st.caption(f"Source loading message: {load_error[:300]}")
    st.markdown(f"[Open original public dataset repository]({DATA_URL.replace('/raw.githubusercontent.com/', 'https://github.com/').replace('/main/', '/blob/main/')})")
    st.stop()

df = prepare(raw)
st.success(f"Loaded {len(df):,} rows and {len(df.columns):,} columns.")
st.caption("Source: dikagra123/Last-Mile-Delivery-Project. Verify field mapping and data-quality rules against the original source before external publication.")

required = ["delayed"]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error("Could not identify the delay-label column. Check CSV headers and update ALIASES in app.py.")
    st.write("Detected columns:", list(df.columns))
    st.stop()

with st.sidebar:
    st.header("Filters")
    def choices(col):
        return sorted(df[col].dropna().astype(str).unique().tolist()) if col in df else []
    selected = {}
    for col, label in [("region","Region"),("delivery_partner","Delivery partner"),("delivery_mode","Delivery mode"),("vehicle_type","Vehicle type"),("weather","Weather")]:
        if col in df:
            opts = choices(col)
            selected[col] = st.multiselect(label, opts, default=opts)
filtered = df.copy()
for col, vals in selected.items():
    if vals:
        filtered = filtered[filtered[col].astype(str).isin(vals)]

total = len(filtered)
delayed = int(filtered["delayed"].sum())
on_time = total - delayed
on_time_pct = on_time / total * 100 if total else 0
delay_pct = delayed / total * 100 if total else 0
cost_total = filtered["delivery_cost"].sum() if "delivery_cost" in filtered else np.nan
cost_km = filtered["delivery_cost"].sum() / filtered["distance_km"].sum() if {"delivery_cost","distance_km"}.issubset(filtered.columns) and filtered["distance_km"].sum() else np.nan

m1,m2,m3,m4,m5 = st.columns(5)
m1.metric("Total deliveries", f"{total:,}")
m2.metric("On-time rate", f"{on_time_pct:.2f}%")
m3.metric("Delay rate", f"{delay_pct:.2f}%")
m4.metric("Total delivery cost", f"{cost_total:,.2f}" if pd.notna(cost_total) else "N/A")
m5.metric("Cost per KM", f"{cost_km:,.2f}" if pd.notna(cost_km) else "N/A")

st.divider()
tab1,tab2,tab3,tab4 = st.tabs(["Executive overview","Partner scorecard","Delay drivers","Data quality"])

with tab1:
    left,right = st.columns([1.3,1])
    with left:
        st.subheader("Delivery mode performance")
        if "delivery_mode" in filtered:
            g = filtered.groupby("delivery_mode", dropna=False).agg(deliveries=("delayed","size"), delayed=("delayed","sum")).reset_index()
            g["on_time_pct"] = (g["deliveries"]-g["delayed"])/g["deliveries"]*100
            fig = px.bar(g.sort_values("on_time_pct"), x="on_time_pct", y="delivery_mode", orientation="h", text=g.sort_values("on_time_pct")["on_time_pct"].map(lambda x:f"{x:.1f}%"), color_discrete_sequence=[GOLD], labels={"on_time_pct":"On-time %","delivery_mode":"Delivery mode"})
            fig.update_layout(template="plotly_dark",paper_bgcolor=PANEL,plot_bgcolor=PANEL,margin=dict(l=10,r=10,t=20,b=10))
            st.plotly_chart(fig,use_container_width=True)
        else: st.info("Delivery mode column not found.")
    with right:
        st.subheader("On-time vs delayed")
        fig = px.pie(names=["On time","Delayed"],values=[on_time,delayed],hole=.62,color_discrete_sequence=[GOLD,"#8A4F45"])
        fig.update_layout(template="plotly_dark",paper_bgcolor=PANEL,margin=dict(l=5,r=5,t=20,b=5),showlegend=True)
        st.plotly_chart(fig,use_container_width=True)
    if "region" in filtered:
        st.subheader("Regional delivery performance")
        rg=filtered.groupby("region").agg(deliveries=("delayed","size"),delayed=("delayed","sum")).reset_index()
        rg["delay_rate_pct"]=rg["delayed"]/rg["deliveries"]*100
        fig=px.bar(rg.sort_values("delay_rate_pct",ascending=False),x="region",y="delay_rate_pct",color="delay_rate_pct",color_continuous_scale=["#6C5A32",GOLD],labels={"delay_rate_pct":"Delay rate %"})
        fig.update_layout(template="plotly_dark",paper_bgcolor=PANEL,plot_bgcolor=PANEL)
        st.plotly_chart(fig,use_container_width=True)

with tab2:
    st.subheader("Partner scorecard")
    if "delivery_partner" in filtered:
        agg={"delayed":("delayed","sum"),"deliveries":("delayed","size")}
        if "delivery_cost" in filtered: agg["total_cost"]=("delivery_cost","sum")
        if "distance_km" in filtered: agg["total_distance"]=("distance_km","sum")
        if "delivery_rating" in filtered: agg["avg_rating"]=("delivery_rating","mean")
        p=filtered.groupby("delivery_partner").agg(**agg).reset_index()
        p["on_time_pct"]=(p["deliveries"]-p["delayed"])/p["deliveries"]*100
        if {"total_cost","total_distance"}.issubset(p.columns): p["cost_per_km"]=p["total_cost"]/p["total_distance"].replace(0,np.nan)
        st.dataframe(p.sort_values("on_time_pct",ascending=False).round(2),use_container_width=True,hide_index=True)
        fig=px.bar(p.sort_values("on_time_pct"),x="on_time_pct",y="delivery_partner",orientation="h",color_discrete_sequence=[GOLD],labels={"on_time_pct":"On-time %","delivery_partner":"Partner"})
        fig.update_layout(template="plotly_dark",paper_bgcolor=PANEL,plot_bgcolor=PANEL)
        st.plotly_chart(fig,use_container_width=True)
        if "cost_per_km" in p:
            fig=px.scatter(p,x="cost_per_km",y="on_time_pct",size="deliveries",hover_name="delivery_partner",color_discrete_sequence=[GOLD],labels={"cost_per_km":"Cost per KM","on_time_pct":"On-time %"})
            fig.update_layout(template="plotly_dark",paper_bgcolor=PANEL,plot_bgcolor=PANEL)
            st.plotly_chart(fig,use_container_width=True)
    else: st.info("Partner column not found.")

with tab3:
    st.subheader("Delay drivers")
    dims=[c for c in ["delivery_mode","region","weather","vehicle_type","package_type"] if c in filtered]
    if dims:
        dimension=st.selectbox("Segment deliveries by",dims)
        z=filtered.groupby(dimension).agg(deliveries=("delayed","size"),delayed=("delayed","sum")).reset_index()
        z["delay_rate_pct"]=z["delayed"]/z["deliveries"]*100
        fig=px.bar(z.sort_values("delay_rate_pct",ascending=False),x=dimension,y="delay_rate_pct",hover_data=["deliveries","delayed"],color_discrete_sequence=[GOLD])
        fig.update_layout(template="plotly_dark",paper_bgcolor=PANEL,plot_bgcolor=PANEL)
        st.plotly_chart(fig,use_container_width=True)
    if "delay_hours" in filtered:
        st.subheader("Delay-hour distribution")
        fig=px.histogram(filtered[filtered["delay_hours"].notna()],x="delay_hours",nbins=35,color_discrete_sequence=[GOLD])
        fig.update_layout(template="plotly_dark",paper_bgcolor=PANEL,plot_bgcolor=PANEL)
        st.plotly_chart(fig,use_container_width=True)
    if "distance_km" in filtered:
        st.subheader("Distance vs delay")
        fig=px.scatter(filtered,x="distance_km",y="delay_hours" if "delay_hours" in filtered else "delayed",color="delivery_status" if "delivery_status" in filtered else None,opacity=.55,color_discrete_sequence=[GOLD,"#8A4F45"])
        fig.update_layout(template="plotly_dark",paper_bgcolor=PANEL,plot_bgcolor=PANEL)
        st.plotly_chart(fig,use_container_width=True)

with tab4:
    st.subheader("Data-quality checks")
    dq=pd.DataFrame({"column":df.columns,"missing_values":[int(df[c].isna().sum()) for c in df.columns],"missing_pct":[round(df[c].isna().mean()*100,2) for c in df.columns],"dtype":[str(df[c].dtype) for c in df.columns]})
    st.dataframe(dq,use_container_width=True,hide_index=True)
    st.metric("Exact duplicate rows removed", f"{len(raw)-len(df):,}")
    if "calculated_delay_flag" in df:
        mismatches=int((df["calculated_delay_flag"].fillna(-1).astype(int)!=df["delayed"]).sum())
        st.metric("Business label vs calculated-time mismatches",f"{mismatches:,}")
        st.caption("Mismatch is an audit flag only. The original business-provided delayed label remains the primary KPI.")
    st.download_button("Download filtered data as CSV",filtered.to_csv(index=False).encode("utf-8"),"logiflow_filtered_deliveries.csv","text/csv")

st.divider()
st.caption("Portfolio project by Debarghya Hajra • Public dataset attribution retained • Estimated delay cost is intentionally not shown as actual financial loss.")
