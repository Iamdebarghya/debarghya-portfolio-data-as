# Power BI Build Guide | LogiFlow

This guide turns the repository assets into a three-page Power BI report. It is written for Power BI Desktop. The GitHub repository contains the source assets, not a finished PBIX.

## 1. Get the data
- Open the source project: https://github.com/dikagra123/Last-Mile-Delivery-Project
- Download `Delivery_Logistics.csv` from the source repository.
- Keep an unchanged raw copy.
- Confirm the source's reuse terms before redistribution.
- Compare actual CSV headers with `docs/data_dictionary.md`. Rename columns to the canonical names before applying the M query.

## 2. Import and clean
1. Power BI Desktop → Get Data → Text/CSV.
2. Select Transform Data.
3. Open Advanced Editor and adapt `power-query/LogiFlow_Staging.m`.
4. If the time fields arrive as malformed epoch/timestamp values, stop and inspect the raw representation. The source README says the original analysis recovered underlying nanosecond values as hours. Do not use a generic Date/Time conversion or guess a divisor.
5. Remove exact duplicate rows only after recording the before/after counts.
6. Confirm `row_id` is unique. Preserve `delivery_id` as a trace field only.
7. Close & Apply.

## 3. Model
- Use `Fact_Deliveries` as the central table.
- Create dimensions for Partner, Region, Vehicle, Mode and Weather using Reference → Remove Other Columns → Remove Duplicates.
- Create one-to-many, single-direction relationships from each dimension to Fact_Deliveries.
- Create Dim_Date only if the raw file has a genuine delivery date. Do not treat duration fields as dates.

## 4. Add calculated columns
Create these in Fact_Deliveries after the duration values have been validated:

```DAX
calculated_delay_flag =
IF (
    Fact_Deliveries[delivery_time_hours]
        > Fact_Deliveries[expected_time_hours],
    1,
    0
)

delay_hours =
Fact_Deliveries[delivery_time_hours]
    - Fact_Deliveries[expected_time_hours]

delay_band =
SWITCH (
    TRUE(),
    Fact_Deliveries[delay_hours] <= 0, "On time / Early",
    Fact_Deliveries[delay_hours] <= 2, "0-2 hours",
    Fact_Deliveries[delay_hours] <= 6, "2-6 hours",
    Fact_Deliveries[delay_hours] <= 12, "6-12 hours",
    "12+ hours"
)
```

## 5. Add measures
Copy measures from `dax/LogiFlow_Measures.dax`. Format:
- On-Time Delivery % and Delay Rate % as Percentage, 1 decimal.
- Cost measures as currency, 2 decimals.
- Hour and distance measures as Decimal, 1 or 2 decimals.
- Delivery counts as whole numbers.

## 6. Build the report pages

### Page 1 — Executive Overview
| Position | Visual | Fields |
|---|---|---|
| Top row | 6 KPI cards | Total Deliveries; On-Time Delivery %; Delay Rate %; Average Actual Delivery Time; Total Delivery Cost; Cost per KM |
| Left middle | Clustered bar | Axis: delivery_mode; Values: On-Time Delivery % |
| Right middle | Clustered column | Axis: region; Values: Delayed Deliveries and On-Time Deliveries |
| Bottom left | Bar | Axis: weather; Values: Delay Rate % |
| Bottom right | Matrix | Rows: region; Columns: delivery_mode; Values: Total Deliveries, On-Time Delivery % |

Slicers: delivery_partner, region, delivery_mode, vehicle_type, weather. Do not add a date slicer unless a valid date exists.

### Page 2 — Partner Scorecard
| Visual | Fields |
|---|---|
| Partner table | delivery_partner, Total Deliveries, On-Time Delivery %, Delay Rate %, Cost per KM, Average Delivery Rating |
| Scatter | X: Cost per KM; Y: On-Time Delivery %; Size: Total Deliveries; Details: delivery_partner |
| Ranked bar | Axis: delivery_partner; Values: On-Time Delivery % |
| Tooltip page | Total Deliveries, On-Time Delivery %, Delay Rate %, Average Delivery Rating, Average Actual Delivery Time |

Use volume context when interpreting rankings. Do not claim a tiny percentage-point difference is operationally meaningful without validation.

### Page 3 — Delay Drivers & Exceptions
| Visual | Fields |
|---|---|
| Delay band column | Axis: delay_band; Values: Total Deliveries |
| Distance analysis | Axis: distance bucket (create only after validating units); Values: Delay Rate % |
| Vehicle analysis | Axis: vehicle_type; Values: Delay Rate % |
| Exception table | row_id, delivery_id, delivery_partner, region, delivery_mode, distance_km, package_weight_kg, delivery_time_hours, expected_time_hours, delay_hours, delivery_cost |

Filter exception table to delayed = 1. Sort by delay_hours descending.

## 7. QA checklist before publishing
- [ ] CSV headers mapped and all required fields present.
- [ ] Duration conversion verified against raw values and source methodology.
- [ ] Fact row count reconciles with the cleaned source.
- [ ] row_id unique and non-null.
- [ ] On-time + delayed = total deliveries.
- [ ] DAX KPI values reconcile with SQL results.
- [ ] Cost per KM uses total cost / total distance, not average row-level ratio.
- [ ] Mismatch count is reported, not silently corrected.
- [ ] 15% estimated delay cost is labelled as a scenario assumption, not actual loss.
- [ ] No time trend shown without a genuine event date.
- [ ] SVG previews are labelled as mockups, not Power BI screenshots.

## 8. Publish and portfolio proof
After building in Power BI Desktop, save the PBIX locally, publish to Power BI Service if your account supports it, and add genuine screenshots plus the verified report link to this folder. Never describe a mockup as a live dashboard.


## 9. Interaction-first design (required for portfolio proof)

The report must behave like a working analyst-built Power BI report, not a static dashboard image.

### Global interactions
- Add synced slicers for Region, Delivery Mode, Vehicle Type, Weather and Delivery Partner.
- Turn on visual interactions so selecting a bar/segment filters or highlights the other visuals where it makes analytical sense.
- Add a visible Reset Filters bookmark/button.
- Add a dynamic page subtitle that reflects the current filter context.
- Show selected filter context in a small text card (for example, selected region and delivery mode).
- Ensure KPI cards recalculate under slicers and cross-highlighting.

### Dynamic DAX examples

```DAX
Selected Region Label =
"Region: " &
COALESCE (
    SELECTEDVALUE ( Dim_Region[region] ),
    "All regions"
)

Selected Delivery Mode Label =
"Delivery mode: " &
COALESCE (
    SELECTEDVALUE ( Dim_Mode[delivery_mode] ),
    "All modes"
)

Dynamic Report Context =
[Selected Region Label] & " | " & [Selected Delivery Mode Label]

On-Time % Previous Partner Context =
CALCULATE (
    [On-Time Delivery %],
    REMOVEFILTERS ( Dim_Partner )
)

Partner On-Time Difference (pp) =
100 * (
    [On-Time Delivery %] - [On-Time % Previous Partner Context]
)
```

Only create these measures if the corresponding dimensions exist and are related to Fact_Deliveries.

### Page-specific analyst storytelling
- **Executive Overview:** start with the question "Where are delays concentrated?" Add a short text insight that changes with the selected delivery mode/region. Avoid hard-coded conclusions.
- **Partner Scorecard:** allow a partner selection to update the KPI cards and delivery-mode mix. Include volume beside percentages so low-volume partners are not misrepresented.
- **Delay Drivers:** selecting weather, vehicle or distance category should update the exception table. Add a drill-through destination for a selected partner or delivery mode.

### Proof that the report is genuinely interactive
Capture three screenshots after the PBIX is built:
1. Default/all-data view.
2. Same page after selecting one region.
3. Same page after selecting a delivery mode while the region filter remains active.

The screenshots must come from the running Power BI report, not SVG mockups or generated illustrations. Keep one screenshot of the Power Query steps and one of the DAX measure pane as build evidence. Do not fake changing numbers in a static image.

- [Analyst storytelling & interview walkthrough](analyst_storytelling.md)
