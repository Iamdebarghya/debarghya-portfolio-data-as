# Olist Brazilian E-commerce Analytics

An end-to-end analytics project built from the real, anonymised Brazilian E-Commerce Public Dataset published by Olist on Kaggle.

**Dataset:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce  
**License:** CC BY-NC-SA 4.0. Review the dataset license before reuse or redistribution.  
**Period:** 2016–2018  
**Scope:** orders, order items, customers, sellers, products, payments, reviews and category translations.

> The dataset contains real anonymised commercial transactions supplied by Olist. It is not Debarghya's employer data, and findings must be described as analysis of the public Olist dataset.

## Business questions
1. How do order value and sales change month to month?
2. Which product categories and states contribute most to sales?
3. How do delivery delays relate to customer review scores?
4. Which payment methods and installment patterns are most common?
5. How concentrated are sales across customers and sellers?

## Project structure
- `app.py` — interactive Streamlit dashboard.
- `src/olist.py` — data loading, validation and metric calculations.
- `sql/schema.sql` — analytical star-schema DDL.
- `sql/analysis.sql` — reproducible business queries.
- `tests/test_olist.py` — unit tests for calculations and validation.

## Get the data
Create a Kaggle account and accept the dataset terms. Then download and extract the dataset:

```bash
pip install -r requirements.txt
kaggle datasets download -d olistbr/brazilian-ecommerce -p data/raw --unzip
```

If you prefer manual download, get the ZIP from the Kaggle page above and extract its CSV files into `data/raw/`.

Expected files include `olist_orders_dataset.csv`, `olist_order_items_dataset.csv`, `olist_customers_dataset.csv`, `olist_order_payments_dataset.csv`, `olist_order_reviews_dataset.csv`, `olist_products_dataset.csv`, `olist_sellers_dataset.csv`, and `product_category_name_translation.csv`.

## Run locally
```bash
python -m venv .venv
# activate the environment, then:
pip install -r requirements.txt
python -m unittest discover -s tests -v
streamlit run app.py
```

The app does not bundle or redistribute Kaggle data. It reads the CSV files from `data/raw/`. Missing files are reported clearly.

## Metric definitions
- **Gross merchandise value (GMV):** sum of item price, excluding freight, for items belonging to eligible orders.
- **Freight value:** sum of item freight charges.
- **Paid order value:** sum of payment records. Do not add this to GMV; it is a separate payment-based measure.
- **Average order value:** GMV divided by distinct eligible orders.
- **Late delivery:** actual customer delivery timestamp is later than the estimated delivery timestamp.
- **On-time delivery rate:** delivered orders not classified as late divided by delivered orders with both timestamps.

## Data quality and interpretation
The source has one-to-many relationships. Joining order items directly to payments or reviews can multiply rows and inflate totals. Aggregate each child table to order grain before combining, or calculate metrics from their correct grain. Canceled/unavailable orders and missing timestamps are handled explicitly in the code. Review scores indicate submitted reviews, not all customers.

## Attribution
Dataset provided by Olist via Kaggle. Please retain attribution and comply with the CC BY-NC-SA 4.0 license.
