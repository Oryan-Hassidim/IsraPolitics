// Ignore Spelling: Timestamp

using Azure;
using Azure.Data.Tables;

namespace IsraPoliticsTagging.Api;

public class UnlabeledEntry : ITableEntity
{
    public int RowId { get; set; }
    public string? Text { get; set; }
    public bool Labeled { get; set; } = false;
    public string? PartitionKey { get; set; } = "TaggingData";
    public string? RowKey { get; set; }
    public DateTimeOffset? Timestamp { get; set; }
    public ETag ETag { get; set; }
}

public class UpdateLabels : ITableEntity
{
    public int RowId { get; set; }
    public bool Labeled { get; set; } = true;
    public int? AssociationLevel { get; set; }
    public int? Positive { get; set; }
    public string? PartitionKey { get; set; } = "TaggingData";
    public string? RowKey { get; set; }
    public DateTimeOffset? Timestamp { get; set; }
    public ETag ETag { get; set; }
}