// Ignore Spelling: Timestamp Enitities

using Azure;
using Azure.Data.Tables;
using israpolitics.Model;
using System.Linq;

namespace israpolitics;

public class UnlabeledEntry : ITableEntity
{
    public int Id { get; set; }
    public required string Prompt { get; set; } = string.Empty;
    public required string Text { get; set; }
    public int ModelScore { get; set; }
    public List<int> ManualScore { get; set; } = [];
    public string PartitionKey { get; set; } = "TaggingData";
    public string RowKey { get; set; } = Guid.CreateVersion7().ToString("D");
    public DateTimeOffset? Timestamp { get; set; }
    public ETag ETag { get; set; }
}

public class AddEnititiesForTaggingToTable
{
    private const string _tableName = "DataForTagging";
    private readonly TableClient _tableClient;

    public AddEnititiesForTaggingToTable()
    {
        string connectionString = File.ReadAllText("TableConnectionString.txt");
        _tableClient = new(connectionString, _tableName);
    }

    public async Task AddAsync(int id, string prompt, int modelScore, string text)
    {
        await _tableClient.CreateIfNotExistsAsync();
        var response = await _tableClient.AddEntityAsync(new UnlabeledEntry
        {
            Id = id,
            Prompt = prompt,
            ModelScore = modelScore,
            Text = text
        });
        if (response.IsError)
            throw new Exception($"Failed to add entity: {response.ReasonPhrase}");
    }
}
