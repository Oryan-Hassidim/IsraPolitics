using Azure;
using Azure.Data.Tables;

namespace IsraPoliticsTagging.Api;

public class DataForTagging : ITableEntity
{
    public int RowId { get; set; }
    // the text for tagging
    public string? Text { get; set; }
    // the label of the level of the association level
    public bool Labeled { get; set; }
    public int? AssociationLevel { get; set; }
    // the label beetwen 0 and 10 how much is positive
    public int? Positive { get; set; }

    public string? PartitionKey { get; set; }
    public string? RowKey { get; set; }
    public DateTimeOffset? Timestamp { get; set; }
    public ETag ETag { get; set; }
}
