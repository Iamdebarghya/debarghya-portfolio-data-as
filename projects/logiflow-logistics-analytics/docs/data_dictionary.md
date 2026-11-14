# Data Dictionary & Canonical Field Mapping

Use this as a **Power BI staging schema**. The public source README describes these concepts, but exact CSV header spellings must be checked in the downloaded file.

| Canonical field | Type | Description | Required for |
|---|---|---|---|
| row_id | Whole number | Sequential surrogate key created during cleaning | Unique row identity |
| delivery_id | Text | Original source identifier; source warns it is not unique | Traceability only |
| delivery_partner | Text | Logistics provider | Partner scorecard |
| package_type | Text | Package category | Segmentation |
| vehicle_type | Text | Vehicle category | Operations analysis |
| delivery_mode | Text | Standard, Two Day, Same Day, Express etc. | Delay-driver analysis |
| region | Text | Delivery region | Regional performance |
| weather | Text | Weather condition | Delay segmentation |
| distance_km | Decimal | Delivery distance in kilometres | Cost efficiency |
| package_weight_kg | Decimal | Package weight | Operational segmentation |
| delivery_time_hours | Decimal | Actual delivery duration in hours after source-specific timestamp repair | Actual duration |
| expected_time_hours | Decimal | Expected delivery duration in hours after source-specific timestamp repair | Delay calculation |
| delayed | Whole number / Boolean | Original business delay label | Primary delay KPI |
| delivery_rating | Decimal | Customer/delivery rating | Quality analysis |
| delivery_cost | Decimal / Currency | Delivery cost | Cost analysis |
| is_delayed | Whole number | Cleaned binary alias of original delayed label | DAX convenience |
| delay_hours | Decimal | Actual minus expected duration, with negative values retained or separately flagged | Delay magnitude |
| cost_per_km | Decimal | Row delivery cost divided by distance, where distance > 0 | Efficiency |

## Data-quality treatment
1. Preserve a raw copy before transformations.
2. Repair malformed duration columns using the source project's documented underlying numeric values. Do not interpret the malformed 1970 timestamps as real delivery dates.
3. Generate `row_id`; do not use `delivery_id` as a unique primary key.
4. Preserve original `delayed` label. Create a separate `calculated_delay_flag` from actual vs expected time to audit disagreements.
5. Flag the approximately 1,203 source-reported label/measurement mismatches for investigation; do not silently overwrite labels.
6. Remove only exact duplicate records and document the row count before/after cleaning.
7. Exclude or flag zero/negative distance before calculating cost per KM.
