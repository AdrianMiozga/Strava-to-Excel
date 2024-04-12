let
    Path = Excel.CurrentWorkbook(){[Name = "Path"]}[Content]{0}[Path],
    Source = Csv.Document(
        File.Contents(Path & "data.csv"), [
            Delimiter = ";",
            Columns = 1,
            Encoding = 1250,
            QuoteStyle = QuoteStyle.None
        ]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {{"Distance", Int64.Type}})
in
    #"Changed Type"
