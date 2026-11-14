# LogiFlow Data Model

## Recommended model
For a first reproducible Power BI version, use a single fact table plus conformed dimensions.

- **Fact_Deliveries**: one row per cleaned delivery record, keyed by `row_id`.
- **Dim_Date**: one row per calendar date, derived from the true delivery date field if present in the CSV. Do not derive dates from the malformed duration fields.
- **Dim_Partner**: distinct delivery partner.
- **Dim_Region**: distinct region.
- **Dim_Vehicle**: distinct vehicle type.
- **Dim_Mode**: distinct delivery mode.
- **Dim_Weather**: distinct weather condition.

## Relationships
- Dim_Date[Date] 1 → * Fact_Deliveries[delivery_date] (only if a genuine date column exists)
- Dim_Partner[delivery_partner] 1 → * Fact_Deliveries[delivery_partner]
- Dim_Region[region] 1 → * Fact_Deliveries[region]
- Dim_Vehicle[vehicle_type] 1 → * Fact_Deliveries[vehicle_type]
- Dim_Mode[delivery_mode] 1 → * Fact_Deliveries[delivery_mode]
- Dim_Weather[weather] 1 → * Fact_Deliveries[weather]

Use single-direction filtering from dimensions to fact. Avoid many-to-many relationships.

## Date caveat
The source README's described fields do not explicitly guarantee a delivery-date column. If the raw CSV has no valid event date, omit the date relationship and do not display a fabricated time trend. Use category/partner/region segmentation instead.

## Validation
- Fact row count equals cleaned source row count.
- row_id is unique and non-null.
- Dimension keys are unique.
- Relationship orphan counts are zero or explained.
- Total cost and delivery count reconcile with SQL/source summaries.
