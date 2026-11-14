/*
LogiFlow Power Query staging query
Source: public Last-Mile-Delivery-Project / Delivery_Logistics.csv
Exact raw headers are based on the source notebook's displayed df.head().
Paste into Power Query Advanced Editor and confirm the source file is accessible.
*/
let
    SourceUrl = "https://raw.githubusercontent.com/dikagra123/Last-Mile-Delivery-Project/main/Delivery_Logistics.csv",
    RawCsv = Csv.Document(
        Web.Contents(SourceUrl),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(RawCsv, [PromoteAllScalars = true]),
    TrimmedHeaders = Table.TransformColumnNames(PromotedHeaders, each Text.Trim(_)),

    ExpectedRawColumns = {
        "delivery_id", "delivery_partner", "package_type", "vehicle_type",
        "delivery_mode", "region", "weather_condition", "distance_km",
        "package_weight_kg", "delivery_time_hours", "expected_time_hours",
        "delayed", "delivery_status", "delivery_rating", "delivery_cost"
    },
    MissingColumns = List.Difference(ExpectedRawColumns, Table.ColumnNames(TrimmedHeaders)),
    CheckedHeaders =
        if List.Count(MissingColumns) > 0
        then error "Unexpected source headers. Missing: " & Text.Combine(MissingColumns, ", ")
        else TrimmedHeaders,

    // Duration strings such as 1970-01-01 00:00:00.000000008 encode 8 nanoseconds.
    // The source analysis treats the trailing nanosecond integer as the hour value.
    ToSourceHours = (value as any) as nullable number =>
        let
            raw = if value = null then null else Text.From(value),
            suffix = if raw = null then null else Text.AfterDelimiter(raw, ".", {0, RelativePosition.FromEnd}),
            parsed = if suffix = null then null else try Number.FromText(suffix, "en-US") otherwise null
        in
            parsed,

    ConvertActualHours = Table.TransformColumns(
        CheckedHeaders,
        {{"delivery_time_hours", each ToSourceHours(_), type number}}
    ),
    ConvertExpectedHours = Table.TransformColumns(
        ConvertActualHours,
        {{"expected_time_hours", each ToSourceHours(_), type number}}
    ),
    NormalizeText = Table.TransformColumns(
        ConvertExpectedHours,
        {
            {"delivery_partner", each Text.Lower(Text.Trim(Text.From(_))), type text},
            {"package_type", each Text.Lower(Text.Trim(Text.From(_))), type text},
            {"vehicle_type", each Text.Lower(Text.Trim(Text.From(_))), type text},
            {"delivery_mode", each Text.Lower(Text.Trim(Text.From(_))), type text},
            {"region", each Text.Lower(Text.Trim(Text.From(_))), type text},
            {"weather_condition", each Text.Lower(Text.Trim(Text.From(_))), type text},
            {"delayed", each Text.Lower(Text.Trim(Text.From(_))), type text},
            {"delivery_status", each Text.Lower(Text.Trim(Text.From(_))), type text}
        }
    ),
    RenameColumns = Table.RenameColumns(
        NormalizeText,
        {{"weather_condition", "weather"}}
    ),
    AddDelayFlag = Table.AddColumn(
        RenameColumns,
        "delayed_flag",
        each if [delayed] = "yes" then 1 else if [delayed] = "no" then 0 else null,
        Int64.Type
    ),
    RemoveRawDelayText = Table.RemoveColumns(AddDelayFlag, {"delayed"}),
    RenameDelayFlag = Table.RenameColumns(RemoveRawDelayText, {{"delayed_flag", "delayed"}}),
    TypeNumerics = Table.TransformColumnTypes(
        RenameDelayFlag,
        {
            {"distance_km", type number},
            {"package_weight_kg", type number},
            {"delivery_rating", Int64.Type},
            {"delivery_cost", Currency.Type},
            {"delayed", Int64.Type}
        },
        "en-US"
    ),
    // Remove exact duplicate source rows before generating row_id.
    RemoveExactDuplicates = Table.Distinct(TypeNumerics),
    // delivery_id is not unique in the source. Generate a surrogate row key.
    AddRowId = Table.AddIndexColumn(RemoveExactDuplicates, "row_id", 1, 1, Int64.Type),
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
    ),
    AddDistanceBucket = Table.AddColumn(
        AddCostPerKm,
        "distance_bucket",
        each
            if [distance_km] = null then "Unknown"
            else if [distance_km] <= 50 then "0-50 km"
            else if [distance_km] <= 100 then "51-100 km"
            else if [distance_km] <= 200 then "101-200 km"
            else "200+ km",
        type text
    ),
    AddDelayBand = Table.AddColumn(
        AddDistanceBucket,
        "delay_band",
        each
            if [delay_hours] <= 0 then "On time / Early"
            else if [delay_hours] <= 2 then "0-2 hours"
            else if [delay_hours] <= 6 then "2-6 hours"
            else if [delay_hours] <= 12 then "6-12 hours"
            else "12+ hours",
        type text
    ),
    Final = AddDelayBand
in
    Final
