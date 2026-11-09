-- PostgreSQL examples. Load the Kaggle CSV into a staging table named stg_hr_attrition.
-- The source is fictional educational data created by IBM; these are descriptive analyses.

-- 1. Overall attrition.
SELECT COUNT(*) AS employees,
       COUNT(*) FILTER (WHERE attrition = 'Yes') AS attrition_count,
       ROUND(100.0 * COUNT(*) FILTER (WHERE attrition = 'Yes') / NULLIF(COUNT(*),0), 2) AS attrition_pct
FROM stg_hr_attrition;

-- 2. Attrition by department with group denominator.
SELECT department, COUNT(*) AS employees,
       COUNT(*) FILTER (WHERE attrition = 'Yes') AS leavers,
       ROUND(100.0 * COUNT(*) FILTER (WHERE attrition = 'Yes') / NULLIF(COUNT(*),0), 2) AS attrition_pct
FROM stg_hr_attrition
GROUP BY department
ORDER BY attrition_pct DESC;

-- 3. Attrition by overtime.
SELECT overtime, COUNT(*) AS employees,
       ROUND(100.0 * COUNT(*) FILTER (WHERE attrition = 'Yes') / NULLIF(COUNT(*),0), 2) AS attrition_pct
FROM stg_hr_attrition
GROUP BY overtime
ORDER BY attrition_pct DESC;

-- 4. Median and average monthly income by attrition.
SELECT attrition, COUNT(*) AS employees,
       percentile_cont(0.5) WITHIN GROUP (ORDER BY monthlyincome) AS median_monthly_income,
       AVG(monthlyincome) AS average_monthly_income
FROM stg_hr_attrition
GROUP BY attrition;
