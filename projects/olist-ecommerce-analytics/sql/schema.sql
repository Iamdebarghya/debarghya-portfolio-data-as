-- PostgreSQL star-schema starter for Olist public dataset.
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE TABLE IF NOT EXISTS analytics.dim_customer (
  customer_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id VARCHAR(40) UNIQUE NOT NULL,
  customer_unique_id VARCHAR(40),
  customer_city TEXT,
  customer_state CHAR(2)
);
CREATE TABLE IF NOT EXISTS analytics.dim_product (
  product_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  product_id VARCHAR(40) UNIQUE NOT NULL,
  category_name TEXT,
  category_name_english TEXT
);
CREATE TABLE IF NOT EXISTS analytics.dim_seller (
  seller_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  seller_id VARCHAR(40) UNIQUE NOT NULL,
  seller_city TEXT,
  seller_state CHAR(2)
);
CREATE TABLE IF NOT EXISTS analytics.dim_date (
  date_key INTEGER PRIMARY KEY,
  full_date DATE UNIQUE NOT NULL,
  calendar_year SMALLINT NOT NULL,
  calendar_month SMALLINT NOT NULL,
  month_name TEXT NOT NULL,
  quarter SMALLINT NOT NULL
);
CREATE TABLE IF NOT EXISTS analytics.fact_order_item (
  order_id VARCHAR(40) NOT NULL,
  order_item_id INTEGER NOT NULL,
  customer_key BIGINT REFERENCES analytics.dim_customer(customer_key),
  product_key BIGINT REFERENCES analytics.dim_product(product_key),
  seller_key BIGINT REFERENCES analytics.dim_seller(seller_key),
  order_date_key INTEGER REFERENCES analytics.dim_date(date_key),
  item_price NUMERIC(12,2) NOT NULL,
  freight_value NUMERIC(12,2) NOT NULL,
  PRIMARY KEY (order_id, order_item_id)
);
CREATE TABLE IF NOT EXISTS analytics.fact_order_payment (
  order_id VARCHAR(40) NOT NULL,
  payment_sequential INTEGER NOT NULL,
  payment_type TEXT,
  payment_installments INTEGER,
  payment_value NUMERIC(12,2) NOT NULL,
  PRIMARY KEY (order_id, payment_sequential)
);
