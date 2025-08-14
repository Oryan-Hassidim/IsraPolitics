// Ignore Spelling: Timestamp Enitities

using Azure;
using Azure.Data.Tables;
using israpolitics.Model;
using System.Linq;

namespace israpolitics;

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

public static class AddEnititiesForTaggingToTable
{
    public static async Task Run()
    {
        // Define the connection string and table name
        string connectionString = await File.ReadAllTextAsync("TableConnectionString.txt");
        string tableName = "DataForTagging";
        
        // Create a new table client
        TableClient tableClient = new(connectionString, tableName);
        await tableClient.CreateIfNotExistsAsync();

        
    }
}
