# HR Attrition Analysis (IBM public educational dataset)

A reproducible HR analytics case study using IBM's fictional Employee Attrition & Performance dataset hosted on Kaggle.

**Dataset:** https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset  
**Important:** Kaggle's dataset description explicitly says this is a fictional dataset created by IBM data scientists. It is useful for demonstrating HR analytics methods, but it is not observed workforce data and must never be described as real employee records or a real company's attrition experience.

## Questions
- What is the overall attrition rate in this dataset?
- How does attrition vary by department, job role, overtime and tenure?
- How do satisfaction scores compare between employees marked as left and stayed?
- How does monthly income vary by job level and attrition status?

## Data
Download `WA_Fn-UseC_-HR-Employee-Attrition.csv` from the Kaggle page and place it in `data/`. The raw file is not redistributed in this repository.

## Run
```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
streamlit run app.py
```

The dashboard also supports uploading the CSV directly in the browser. It validates required columns and labels all output as analysis of IBM's fictional educational dataset.

## Methodology
- Attrition rate = count(Attrition = Yes) / count(all employees).
- Group attrition rates use each group's own employee count as denominator.
- Income comparisons use median as well as mean to reduce sensitivity to skew.
- EmployeeNumber, EmployeeCount, StandardHours and Over18 are not treated as explanatory variables.
- Demographic breakdowns are descriptive, not causal. Do not use this sample analysis for employment decisions about real people.

## Source and attribution
Dataset by IBM data scientists, distributed via Kaggle. See the Kaggle dataset page for license and reuse terms. This project does not claim IBM endorsement.
