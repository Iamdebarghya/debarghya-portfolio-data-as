import pandas as pd

REQUIRED = {
    "Attrition", "Department", "JobRole", "OverTime", "MonthlyIncome",
    "YearsAtCompany", "JobSatisfaction", "Age", "EmployeeNumber"
}

def validate_hr_data(df):
    if df is None or df.empty:
        raise ValueError("The employee dataset is empty.")
    missing = REQUIRED.difference(df.columns)
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))
    if df["EmployeeNumber"].duplicated().any():
        raise ValueError("EmployeeNumber must be unique for employee-level analysis.")
    if not set(df["Attrition"].dropna().unique()).issubset({"Yes", "No"}):
        raise ValueError("Attrition must contain Yes/No values.")
    return df.copy()

def overall_metrics(df):
    n = int(len(df))
    left = int(df["Attrition"].eq("Yes").sum())
    return {"employees": n, "attrition_count": left,
            "attrition_rate": left / n if n else 0.0,
            "median_income": float(pd.to_numeric(df["MonthlyIncome"], errors="coerce").median()) if n else 0.0}

def attrition_by(df, dimension):
    if dimension not in df.columns:
        raise KeyError(f"Unknown dimension: {dimension}")
    work = df[[dimension, "Attrition"]].dropna()
    out = work.groupby(dimension).agg(
        employees=("Attrition", "size"),
        attrition_count=("Attrition", lambda s: int(s.eq("Yes").sum()))
    ).reset_index()
    out["attrition_rate"] = out["attrition_count"] / out["employees"]
    return out.sort_values(["attrition_rate", "employees"], ascending=[False, False])

def compare_income(df, dimension="Attrition"):
    if dimension not in df.columns:
        raise KeyError(f"Unknown dimension: {dimension}")
    work = df[[dimension, "MonthlyIncome"]].copy()
    work["MonthlyIncome"] = pd.to_numeric(work["MonthlyIncome"], errors="coerce")
    return work.dropna().groupby(dimension)["MonthlyIncome"].agg(
        employees="count", median_income="median", average_income="mean"
    ).reset_index()
