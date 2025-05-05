// Ignore Spelling: Timestamp Enitities

using Azure;
using Azure.Data.Tables;
using israpolitics.Model;
using System.Collections.Frozen;
using System.Net;

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

        Random rand = new(1234);

        var ids = (await File.ReadAllLinesAsync("ids.txt")).Select(int.Parse).ToArray();
        var texts = await File.ReadAllLinesAsync("texts.txt");
        var N = ids.Length;

        var indexes = new HashSet<int>();

        while (indexes.Count < 2000)
        {
            int randomIndex = rand.Next(N);
            indexes.Add(randomIndex);
        }

        var responses = await Task.WhenAll(indexes.Select(s => tableClient.AddEntityAsync(new UnlabeledEntry()
        {
            RowId = ids[s],
            Text = texts[s],
            RowKey = Guid.NewGuid().ToString()
        })));

        foreach (var response in responses)
            if (response.Status != 204)
                Console.WriteLine($"Error: {response.Status}");
    }
}
