import streamlit as st
import pandas as pd
import plotly.express as px
from src.hr_metrics import validate_hr_data, overall_metrics, attrition_by, compare_income

st.set_page_config(page_title="HR Attrition Analytics", page_icon="👥", layout="wide")
st.title("HR Attrition & Workforce Analysis")
st.caption("IBM fictional educational dataset hosted on Kaggle. Not real employee records.")
st.info("Dataset provenance: IBM states that this dataset was created by its data scientists as a fictional dataset. Use for learning and portfolio demonstration only.")
upload = st.file_uploader("Upload WA_Fn-UseC_-HR-Employee-Attrition.csv", type=["csv"])
if upload is None:
    st.markdown("[Download dataset from Kaggle](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)")
    st.stop()
try:
    df = validate_hr_data(pd.read_csv(upload))
except Exception as exc:
    st.error(f"Could not validate dataset: {exc}")
    st.stop()

with st.sidebar:
    st.header("Filters")
    departments = sorted(df["Department"].dropna().unique())
    roles = sorted(df["JobRole"].dropna().unique())
    chosen_departments = st.multiselect("Department", departments, default=departments)
    chosen_roles = st.multiselect("Job role", roles, default=roles)
    overtime = sorted(df["OverTime"].dropna().unique())
    chosen_overtime = st.multiselect("Overtime", overtime, default=overtime)

view = df[df["Department"].isin(chosen_departments) & df["JobRole"].isin(chosen_roles) & df["OverTime"].isin(chosen_overtime)]
m = overall_metrics(view)
a,b,c = st.columns(3)
a.metric("Employees in selection", f"{m['employees']:,}")
b.metric("Attrition count", f"{m['attrition_count']:,}")
c.metric("Attrition rate", f"{m['attrition_rate']:.1%}")
st.caption("Rates are calculated within the filtered population; small groups can produce volatile percentages.")

left,right = st.columns(2)
by_dept = attrition_by(view, "Department")
left.subheader("Attrition by department")
left.plotly_chart(px.bar(by_dept, x="Department", y="attrition_rate", hover_data=["employees","attrition_count"], labels={"attrition_rate":"Attrition rate"}), use_container_width=True)
by_role = attrition_by(view, "JobRole")
right.subheader("Attrition by job role")
right.plotly_chart(px.bar(by_role, x="attrition_rate", y="JobRole", orientation="h", hover_data=["employees","attrition_count"], labels={"attrition_rate":"Attrition rate"}), use_container_width=True)

overtime_data = attrition_by(view, "OverTime")
st.subheader("Overtime and attrition")
st.plotly_chart(px.bar(overtime_data, x="OverTime", y="attrition_rate", hover_data=["employees","attrition_count"]), use_container_width=True)
income = compare_income(view)
st.subheader("Income by attrition status")
st.plotly_chart(px.bar(income, x="Attrition", y="median_income", hover_data=["employees","average_income"], labels={"median_income":"Median monthly income"}), use_container_width=True)

st.subheader("Filtered data")
st.dataframe(view, use_container_width=True)
st.download_button("Download filtered CSV", view.to_csv(index=False).encode("utf-8-sig"), "hr_attrition_filtered.csv", "text/csv")
