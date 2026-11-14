/*
LogiFlow Power Query staging template
1) Confirm the source CSV URL and exact headers before refresh.
2) This query assumes canonical headers from docs/data_dictionary.md.
3) The source README documents malformed duration timestamps. This query does NOT
   guess their repair; inspect raw values and apply the source-specific repair
   only after confirming the exported representation.
*/
let
    SourceUrl = "https://raw.githubusercontent.com/dikagra123/Last-Mile-Delivery-Project/main/Delivery_Logistics.csv",
    RawCsv = Csv.Document(
        Web.Contents(SourceUrl),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(RawCsv, [PromoteAllScalars = true]),
    TrimmedHeaders = Table.TransformColumnNames(PromotedHeaders, each Text.Trim(_)),
    RequiredColumns = {
        "delivery_id", "delivery_partner", "package_type", "vehicle_type",
        "delivery_mode", "region", "weather", "distance_km",
        "package_weight_kg", "delivery_time_hours", "expected_time_hours",
        "delayed", "delivery_rating", "delivery_cost"
    },
    ExistingColumns = Table.ColumnNames(TrimmedHeaders),
    MissingColumns = List.Difference(RequiredColumns, ExistingColumns),
    HeaderCheck =
        if List.Count(MissingColumns) > 0
        then error "Source headers differ from canonical mapping. Missing: " & Text.Combine(MissingColumns, ", ")
        else TrimmedHeaders,
    Typed = Table.TransformColumnTypes(
        HeaderCheck,
        {
            {"delivery_id", type text},
            {"delivery_partner", type text},
            {"package_type", type text},
            {"vehicle_type", type text},
            {"delivery_mode", type text},
            {"region", type text},
            {"weather", type text},
            {"distance_km", type number},
            {"package_weight_kg", type number},
            {"delivery_time_hours", type number},
            {"expected_time_hours", type number},
            {"delayed", Int64.Type},
            {"delivery_rating", type number},
            {"delivery_cost", Currency.Type}
        },
        "en-US"
    ),
    AddRowId = Table.AddIndexColumn(Typed, "row_id", 1, 1, Int64.Type),
    AddDelayHours = Table.AddColumn(
        AddRowId,
        "delay_hours",
        each [delivery_time_hours] - [expected_time_hours],
        type number
    ),
    AddCalculatedDelayFlag = Table.AddColumn(
        AddDelayHours,
        "calculated_delay_flag",
        each if [delivery_time_hours] > [expected_time_hours] then 1 else 0,
        Int64.Type
    ),
    AddMismatchFlag = Table.AddColumn(
        AddCalculatedDelayFlag,
        "label_measurement_mismatch",
        each if [delayed] <> [calculated_delay_flag] then 1 else 0,
        Int64.Type
    ),
    AddCostPerKm = Table.AddColumn(
        AddMismatchFlag,
        "cost_per_km",
        each if [distance_km] = null or [distance_km] <= 0 then null else [delivery_cost] / [distance_km],
        type number
    )
in
    AddCostPerKm
