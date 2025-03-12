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

        var indexes = tableClient.QueryAsync<UnlabeledEntry>().ToBlockingEnumerable().Select(x => x.RowId).ToHashSet();

        //HashSet<int> indexes = [];
        Random rand = new(1234);
        var N = 4_484_726;
        using var context = new Context();

        for (int i = 0; i < 1_000; i++)
        {
            var id = rand.Next(1, N + 1);
            if (indexes.Contains(id))
            {
                i--;
                continue;
            }
            var entry = context.KnessetSpeechesEntries.Find(id);
            if (entry is null)
            {
                i--;
                continue;
            }
            indexes.Add(id);
            if (entry.Text?.Length < 50)
            {
                i--;
                continue;
            }
            var unlabeledEntry = new UnlabeledEntry()
            {
                RowId = id,
                Text = entry.Text,
                RowKey = Guid.NewGuid().ToString()
            };
            await tableClient.AddEntityAsync(unlabeledEntry);
        }
    }
}
