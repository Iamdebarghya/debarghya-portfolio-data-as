# LogiFlow | Last-Mile Delivery Performance Analytics

**Power BI · DAX · SQL · Power Query · Public Dataset**

An executive-style logistics analytics case study built around a publicly available dataset of **25,000 last-mile delivery records**. The goal is to identify the operational drivers of delivery delays and turn them into measurable service and cost improvement opportunities.

> **Data provenance:** The source dataset and its published analysis are maintained by [dikagra123/Last-Mile-Delivery-Project](https://github.com/dikagra123/Last-Mile-Delivery-Project). This repository links to the original public source rather than redistributing its raw CSV. Review the source repository's data-use terms before downloading or reusing the file. This portfolio is an independent analysis and is not affiliated with the dataset author.

## Business questions
1. What is the overall on-time delivery rate and how does it vary by delivery mode?
2. Which delivery partners have the strongest balance of reliability, cost and rating?
3. How do region, weather, vehicle type and distance relate to delays?
4. Which deliveries should be prioritized for operational review?
5. What is the directional financial impact of late deliveries?

## Dataset overview
The source README describes 25,000 records with fields covering:
- Delivery partner, package type, vehicle type, delivery mode and region
- Weather condition, distance and package weight
- Actual and expected delivery time
- Delay label, delivery rating and delivery cost

The source project reports data-quality issues that must remain visible in any reproduction:
- Time columns were exported as malformed 1970-epoch timestamps; the source analysis recovered underlying nanosecond values as hour values.
- `delivery_id` is not a reliable unique key; the source analysis generated a sequential `row_id`.
- About 1,203 records (~4.8%) have a mismatch between the business delay label and delay recalculated from actual vs expected time. The original `delayed` label was retained as the primary analysis target.
- Exact duplicate rows were removed during cleaning.

**Important:** Verify the downloaded CSV's exact headers and data types before using the starter SQL/DAX. Field aliases below are based on the source README and may need to be mapped to the exact file headers.

## Published source findings (as documented by the source project)
- Overall on-time rate: **73.32%** across 25,000 deliveries.
- Delivery mode is reported as the strongest delay differentiator.
- Approximate on-time rates: Standard ~100%, Two Day ~99–100%, Same Day ~65–69%, Express ~26%.
- Regional on-time rates are reported in a relatively narrow ~73–74% range.
- Delhivery is reported at 75% on-time; Amazon Logistics at 73%.
- A two-sample t-test comparing Delhivery and Amazon Logistics is reported as t=-2.045, p=0.041. Statistical significance does not establish meaningful business impact.

These are **source-reported results**, not independently recalculated by this repository yet.

## Dashboard design
### Page 1 — Executive Delivery Overview
- KPI cards: Deliveries, On-Time %, Delayed %, Avg Delivery Time, Avg Distance, Delivery Cost
- Monthly delivery trend
- On-time rate by delivery mode
- Delay rate by region and weather
- Slicers: Date, Region, Delivery Mode, Vehicle Type

### Page 2 — Partner Scorecard
- Partner on-time %, volume, average cost/km and rating
- Reliability vs cost scatter plot
- Partner rank by on-time rate
- Drill-through to partner detail

### Page 3 — Delay Drivers & Exceptions
- Delay distribution and delay-hour buckets
- Vehicle, weather, distance and package-weight analysis
- Exception table with delivery ID/row ID, partner, region, mode, distance and delay
- High-risk operational review filters

## Metric definitions
- **On-Time %** = on-time deliveries / total deliveries.
- **Delay %** = deliveries flagged delayed / total deliveries.
- **Average Delay Hours** = average of non-negative delay hours; confirm the business rule used for early deliveries.
- **Cost per KM** = total delivery cost / total distance. This is a ratio of sums, not an average of row-level ratios.
- **Estimated Delay Cost** = delivery cost of delayed deliveries × 15%. This is a scenario assumption from the source project, not an observed cost or audited financial figure.

## Build instructions
1. Download the CSV from the [original dataset repository](https://github.com/dikagra123/Last-Mile-Delivery-Project).
2. Inspect the file headers and license/terms. Keep the raw file local if redistribution rights are unclear.
3. Import into Power BI Desktop and rename the source columns to the canonical names documented in `docs/data_dictionary.md`.
4. Create a Date table and relationships as documented in `docs/data_model.md`.
5. Add measures from `dax/LogiFlow_Measures.dax`.
6. Use `sql/logiflow_analysis.sql` for independent KPI checks after mapping source fields.
7. Build the three report pages using `docs/report_blueprint.md` and the SVG mockups.
8. Validate all numbers against the raw data before publishing.

## Integrity notes
- This repository does not contain a PBIX file or claim that an interactive report has already been published.
- SVG files are static design mockups, not screenshots of a running Power BI report.
- All numerical findings above are attributed to the linked source project's README until independently reproduced.
- Do not describe the 15% delay-cost scenario as actual company loss.
