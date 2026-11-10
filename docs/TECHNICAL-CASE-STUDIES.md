# Technical Case Studies

These case studies are based on the source code and project documentation in this repository. They distinguish measured results from methodology and interpretation. The HR dataset is fictional, and the Olist dataset is public anonymised data, not employer or client data.

---

# 1. Olist Brazilian E-commerce Analytics

## Project context

Olist's public Brazilian E-Commerce dataset covers marketplace transactions from 2016 to 2018. The project explores sales, order behaviour, delivery performance, product categories, customer geography, payments and submitted reviews.

**Data source:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce  
**License:** CC BY-NC-SA 4.0. Follow the dataset license and attribution requirements.

## Business questions
- How does item revenue change month to month?
- Which product categories and customer states contribute most to item revenue?
- How timely are deliveries, and how do review scores vary with delivery status?
- What payment types and installment patterns appear in the dataset?
- How concentrated are transactions across customers and sellers?

## Data and preparation

The Streamlit app expects eight CSV files: orders, order items, customers, payments, reviews, products, sellers and category translations. The optional geolocation CSV is not used by the current app. The Python implementation loads local CSV files or an uploaded Kaggle ZIP. It prepares an order-level view for KPI and delivery analysis, and calculates category revenue separately from item-level rows. Sidebar filters apply purchase month, customer state and order status.

## Data model and technical decisions

The SQL implementation uses customer, product, seller and date dimensions, plus separate order-item, payment and review fact tables. The order-item fact has a composite key of order ID and item ID. Payment and review records retain their own grain.

This separation matters because one order can have multiple item rows, payment records and reviews. Joining all raw child tables together can multiply rows and overstate sums. The analysis SQL calculates item revenue from the item fact and payment mix from the separate payment fact. Aggregate to the intended grain before joining.

The ETL uses ON CONFLICT upserts to make dimension and fact loads repeatable. Date keys use YYYYMMDD. Product category translations are applied when available.

## KPI definitions

| KPI | Definition used by the project |
|---|---|
| Item GMV | Sum of item price, excluding freight, for eligible orders |
| Freight | Sum of item freight charges |
| Paid amount | Sum of payment records, reported separately from item GMV |
| Average order value | Item GMV divided by distinct eligible orders |
| Late delivery | Actual customer delivery timestamp is later than estimated delivery timestamp |
| On-time delivery rate | Delivered orders on or before estimate divided by delivered orders with both timestamps |
| Average delivery time | Mean days from purchase to customer delivery for delivered orders |
| Average review score | Mean of submitted review records |

Canceled and unavailable orders are excluded from eligible item GMV calculations. Delivery rates use only delivered orders with both required timestamps.

## Results recorded in the project README

The documented dataset profile contains 99,441 orders, 112,650 order-item rows, 32,951 products, 3,095 sellers and 96,478 delivered orders. The README records these results from the uploaded CSV snapshot:

| Result | Value |
|---|---:|
| Delivered item GMV | R$13,221,498.11 |
| Delivered orders | 96,478 |
| Delivered average order value | R$137.04 |
| On-time delivery rate | 91.89% |
| Average delivery time | 12.56 days |
| Average submitted review score | 4.09 / 5 |

The README lists Health & Beauty, Watches & Gifts, Bed Bath & Table, Sports & Leisure, and Computers & Accessories among the top item-revenue categories. These are descriptive findings from the public dataset snapshot, not client or employer results.

## Limitations and interpretation
- Review scores exist only for submitted reviews, not every customer.
- Delivery calculations depend on the availability of actual and estimated timestamps.
- Payment value is not interchangeable with item GMV.
- Category revenue is an item-grain measure.
- The figures above are documented results from the uploaded dataset snapshot. Re-run the project against a fresh download before treating them as newly validated.

## How to reproduce

Follow the data download and local run instructions in the Olist project README. Inspect src/olist.py, sql/schema.sql, sql/etl.sql, sql/analysis.sql and tests/test_olist.py.

---

# 2. HR Attrition Analysis

## Project context

This project uses IBM's fictional Employee Attrition & Performance educational dataset, distributed through Kaggle. IBM describes the data as fictional. It is a learning and portfolio exercise, not a real company's workforce history and not suitable for decisions about real employees.

**Data source:** https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset

## Business questions
- What is the overall attrition rate in the selected dataset?
- How does attrition vary by department, job role, overtime and tenure?
- How do satisfaction scores compare between employees marked as left and stayed?
- How does monthly income vary by job level and attrition status?

## Data validation and preparation

The Python validation function checks that the input is not empty, that required columns are present, that EmployeeNumber is unique, and that Attrition contains only Yes/No values. It returns a copy of the validated dataframe.

Required fields include Attrition, Department, JobRole, OverTime, MonthlyIncome, YearsAtCompany, JobSatisfaction, Age and EmployeeNumber.

## Analysis methodology
- Overall attrition rate is the number marked Yes divided by the number of employees in the selected population.
- Group attrition rates use the employee count within that group as the denominator.
- Income comparisons show both median and mean, since income distributions can be skewed.
- EmployeeNumber, EmployeeCount, StandardHours and Over18 are not treated as explanatory variables.
- Department, job role and overtime filters are applied before displayed metrics are calculated.

## Dashboard outputs

The Streamlit app displays the selected employee count, attrition count and attrition rate. It provides breakdowns by department, job role and overtime, plus median monthly income by attrition status. It also displays and allows download of the filtered rows.

## Interpretation and limitations

These comparisons are descriptive, not causal. A higher group rate in this sample does not establish that a particular job role, department or overtime status causes attrition. Small filtered groups can produce volatile percentages. The project must not be presented as analysis of actual employees or used to make employment decisions.

## How to reproduce

Download WA_Fn-UseC_-HR-Employee-Attrition.csv from the linked Kaggle page, place it in the project's data directory, then follow the HR project README. Inspect src/hr_metrics.py, app.py and tests.

---

# 3. India Online Sales Performance Dashboard

## Project context

This is a browser-based dashboard for exploring sales and profitability from two user-supplied CSV files: an order-details file and an orders file. The user selects both files and builds the dashboard. Parsing and calculations take place locally in the browser.

## Business questions
- What are the total sales, total recorded profit and units sold?
- What is the profit margin?
- How do sales change month to month?
- Which product categories and states contribute to sales or profit?
- How does sales value vary by payment mode?
- Which sub-categories lead on sales?

## Input and workflow

The page uses PapaParse to read CSV files and Chart.js to render visualisations. The user supplies both source files. The dashboard provides filters for state, category and payment mode.

## KPI definitions shown in the dashboard

| KPI | Calculation / meaning |
|---|---|
| Gross sales | Sum of order line amounts |
| Total profit | Sum of recorded profit |
| Units sold | Sum of quantity |
| Profit margin | Total profit divided by gross sales |

The dashboard also displays a monthly sales trend, category sales, profit by state, payment-mode sales, business observations and a top-ten sub-category table.

## Limitations

The dashboard's output depends on the uploaded CSV files and their field definitions. No numerical sales result is claimed here because a specific source CSV snapshot is not included as evidence. Reviewers should use the original data dictionary and inspect the input columns before interpreting calculations. The page processes files locally in the browser and states that the files are not uploaded to a server.

## How to reproduce

Open dashboard.html, select the order-details CSV and orders CSV, then choose Build dashboard. The source file and its calculations can be inspected directly in this repository.

---

## Interview discussion prompts

1. Why can joining order items directly to payments and reviews inflate revenue?
2. What is the grain of each Olist fact table, and which key identifies a row?
3. Why is item GMV kept separate from payment value and freight?
4. What denominator is used for the Olist on-time delivery rate, and which orders are excluded?
5. Why should attrition rate be recalculated inside each filtered group?
6. Why are median and mean both useful for income comparisons?
7. What checks prevent duplicate employee records or invalid attrition labels from entering the HR analysis?
8. What assumptions must be checked in the two CSV files before trusting the sales dashboard?
9. Which results are descriptive, and why do they not establish causation?
10. How would you test a new KPI or filter and demonstrate that the output is correct?

## Evidence and transparency

The case studies describe the code and documentation currently present in this portfolio. Public and fictional educational datasets are labelled as such. No private client data, employer outcomes or unverified business impact is claimed. For reproducibility steps and known validation limitations, also read docs/VERIFICATION-GUIDE.md.