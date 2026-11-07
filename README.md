# debarghya-portfolio-data-as
# India Online Sales Performance Analysis

**An Interactive Business Intelligence Case Study**

**Author:** Debarghya Hajra  
**Role:** Data Analyst  
**Project Type:** Business Intelligence & Data Analytics

---

## 1. Project Overview

This project explores an Indian online sales dataset to understand business performance across products, regions, payment methods and time periods.

The objective was to transform raw order-level CSV files into an interactive dashboard that helps users explore sales performance, profitability and product trends.

The dashboard runs directly in the browser. Users can upload the source CSV files, apply filters and explore the results without sending their data to an external server.

## 2. Business Objectives

The analysis focuses on five key questions:

1. What is the overall sales and profit performance?
2. How do sales change month by month?
3. Which product categories contribute most to sales?
4. Which states generate higher profits?
5. How do different payment methods contribute to revenue?

## 3. Dataset

The dashboard uses two CSV files from a public Kaggle dataset:

- `Details.csv`
- `Orders.csv`

The dashboard combines order details with order-level information using the available order identifiers.

**Data loaded during the demonstrated analysis:**
- 1,500 order-detail rows loaded
- 0 unmatched or invalid rows reported by the dashboard

## 4. Tools & Technologies

| Technology | Purpose |
|---|---|
| HTML | Page structure |
| CSS | Dashboard styling |
| JavaScript | Data processing and interactivity |
| Chart.js | Data visualization |
| PapaParse | CSV parsing |
| SheetJS (XLSX) | Spreadsheet processing |

## 5. Key Performance Indicators

The following results were displayed after loading the dataset:

| KPI | Result |
|---|---:|
| Gross Sales | ₹4,37,771 |
| Total Profit | ₹36,963 |
| Units Sold | 5,615 |
| Profit Margin | 8.4% |
| Order Lines | 1,500 |

*These figures represent the loaded dataset shown in the dashboard, not live business data.*

## 6. Dashboard Features

### Interactive Filters
- State filter
- Product category filter
- Payment mode filter

### Visual Analysis
- Monthly sales trend
- Sales by product category
- Profit by state
- Sales by payment mode

### Data Processing
- Upload two CSV source files
- Match order details with order records
- Calculate sales, profit, quantity and margin
- Update dashboard metrics and visualizations based on selected filters

## 7. Key Observations

Based on the displayed dashboard:

- Gross sales were ₹4,37,771.
- Recorded profit was ₹36,963.
- The calculated profit margin was approximately 8.4%.
- Madhya Pradesh and Maharashtra appeared among the leading states in the displayed profit comparison.
- Electronics, Clothing and Furniture were represented in the category analysis.
- COD, Credit Card, EMI, UPI and Debit Card were included in the payment-mode analysis.

These observations describe the displayed dataset. Further investigation would be required before making business recommendations.

## 8. Privacy & Data Handling

All CSV processing and calculations take place locally in the user's browser.

The uploaded files are not sent to a backend server by this dashboard.

## 9. Live Project

**Live Dashboard:**  
https://iamdebarghya.github.io/debarghya-portfolio-data-as/dashboard.html

**GitHub Repository:**  
https://github.com/lamdebarghya/debarghya-portfolio-data-as

## 10. What I Learned

Through this project, I practised:

- Combining multiple CSV datasets
- Data validation and preprocessing
- KPI calculation
- Interactive data visualization
- Building browser-based analytical tools
- Presenting business data through a structured dashboard

---

**Project by Debarghya Hajra**  
Data Analytics | SQL | Python | Power BI | Business Intelligence
