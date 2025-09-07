using OpenAI;
using OpenAI.Batch;
using OpenAI.Files;
using System.ClientModel;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Text.Unicode;

namespace israpolitics.Process;


#region Helper Classes

[JsonSerializable(typeof(BatchRequestInputObject))]
[JsonSerializable(typeof(BatchBody))]
[JsonSerializable(typeof(ChatMessage))]
[JsonSerializable(typeof(Batch))]
[JsonSerializable(typeof(BatchCreateRequest))]
[JsonSourceGenerationOptions(
    WriteIndented = false,
    PropertyNamingPolicy = JsonKnownNamingPolicy.SnakeCaseLower,
    DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull)]
internal partial class MyJsonContext : JsonSerializerContext;

public class BatchBody(string model, ChatMessage[] messages)
{
    public string Model { get; set; } = model;
    public ChatMessage[] Messages { get; set; } = messages;
    public int MaxTokens { get; set; } = 10_000;
    public int N { get; set; } = 1;
}

public class BatchRequestInputObject(string customId, BatchBody body)
{
    public string CustomId { get; set; } = customId;
    public BatchBody Body { get; set; } = body;
    public string Method { get; set; } = "POST";
    public string Url { get; set; } = "/v1/chat/completions";
}

public class ChatMessage(string role, string content)
{
    public string Role { get; set; } = role;
    public string Content { get; set; } = content;
}

public class SystemChatMessage(string content) : ChatMessage("system", content);

public class UserChatMessage(string content) : ChatMessage("user", content);

public class AssistantChatMessage(string content) : ChatMessage("assistant", content);

public class Batch
{
    public required string Id { get; set; }
    public required string Object { get; set; } = "batch";
    public required string Endpoint { get; set; }
    public Error? Errors { get; set; }
    public required string InputFileId { get; set; }
    public required string CompletionWindow { get; set; }
    public BatchStatus Status { get; set; }
    public string? OutputFileId { get; set; }
    public string? ErrorFileId { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime? InProgressAt { get; set; }
    public DateTime ExpiresAt { get; set; }
    public DateTime? FinalizingAt { get; set; }
    public DateTime? CompletedAt { get; set; }
    public DateTime? FailedAt { get; set; }
    public DateTime? ExpiredAt { get; set; }
    public DateTime? CancellingAt { get; set; }
    public DateTime? CancelledAt { get; set; }
    public required RequestCounts RequestCounts { get; set; }
    public required Dictionary<string, object>? Metadata { get; set; }
}

public class UnixTimestampConverter : JsonConverter<DateTime>
{
    public override DateTime Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
    {
        long seconds = reader.GetInt64();
        return DateTimeOffset.FromUnixTimeSeconds(seconds).UtcDateTime;
    }

    public override void Write(Utf8JsonWriter writer, DateTime value, JsonSerializerOptions options)
    {
        long unixTime = ((DateTimeOffset)value).ToUnixTimeSeconds();
        writer.WriteNumberValue(unixTime);
    }
}

public class UnixTimestampNullableConverter : JsonConverter<DateTime?>
{
    public override DateTime? Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
    {
        if (reader.TokenType == JsonTokenType.Null)
            return null;
        long seconds = reader.GetInt64();
        return DateTimeOffset.FromUnixTimeSeconds(seconds).UtcDateTime;
    }
    public override void Write(Utf8JsonWriter writer, DateTime? value, JsonSerializerOptions options)
    {
        if (value is null)
        {
            writer.WriteNullValue();
            return;
        }
        long unixTime = ((DateTimeOffset)value).ToUnixTimeSeconds();
        writer.WriteNumberValue(unixTime);
    }
}

[JsonConverter(typeof(JsonStringEnumConverter<BatchStatus>))]
public enum BatchStatus
{
    Validating,
    Failed,
    InProgress,
    Finalizing,
    Completed,
    Expired,
    Cancelling,
    Cancelled,
}

public class Error
{
    public required ErrorData[] Data { get; set; }
    public string Object { get; set; } = "list";
}

public class ErrorData
{
    public required string Code { get; set; }
    public long? Line { get; set; }
    public required string Message { get; set; }
    public required string? Param { get; set; }
}

public class RequestCounts
{
    public int Total { get; set; }
    public int Completed { get; set; }
    public int Failed { get; set; }
}

public class BatchCreateRequest
{
    public string CompletionWindow { get; set; } = "24h";
    public required BatchEndpoint Endpoint { get; set; }
    public required string InputFileId { get; set; }
    public Dictionary<string, string>? Metadata { get; set; }
    public OutputExpiresAfter? OutputExpiresAfter { get; set; }
}


[JsonConverter(typeof(JsonStringEnumConverter<BatchEndpoint>))]
public enum BatchEndpoint
{
    [JsonStringEnumMemberName("/v1/completions")]
    Completions,

    [JsonStringEnumMemberName("/v1/chat/completions")]
    ChatCompletions,

    [JsonStringEnumMemberName("/v1/embeddings")]
    Embeddings,

    [JsonStringEnumMemberName("/v1/responses")]
    Responses
}

public class OutputExpiresAfter
{
    public required string Anchor { get; set; }
    public required int Seconds { get; set; }
}
#endregion

public record IdText(int Id, string Text);

public static class OpenAIBatchJobs
{
    private const string _openAIKeyFilePath = "OpenAI_key.txt";
    private static readonly string _openAIKey;
    private static readonly JsonSerializerOptions _jsonSerializerOptions;

    static OpenAIBatchJobs()
    {
        _openAIKey = File.Exists(_openAIKeyFilePath)
            ? File.ReadAllText(_openAIKeyFilePath)
            : throw new FileNotFoundException("OpenAI key file not found.", _openAIKeyFilePath);
        _jsonSerializerOptions = new JsonSerializerOptions
        {
            TypeInfoResolver = MyJsonContext.Default,
            Encoder = System.Text.Encodings.Web.JavaScriptEncoder.Create(UnicodeRanges.BasicLatin, UnicodeRanges.Hebrew),
            AllowTrailingCommas = true,
            PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
        };
        _jsonSerializerOptions.Converters.Add(new JsonStringEnumConverter(JsonNamingPolicy.SnakeCaseLower, allowIntegerValues: false));
        _jsonSerializerOptions.Converters.Add(new UnixTimestampConverter());
        _jsonSerializerOptions.Converters.Add(new UnixTimestampNullableConverter());
    }

    public static async Task<string> CreateBatchJob(string systemPrompt, string job, IAsyncEnumerable<IdText> texts, string model)
    {
        var client = new OpenAIClient(_openAIKey);
        var tempFile = Path.GetTempFileName();
        using (var stream = new FileStream(tempFile, FileMode.Create, FileAccess.Write, FileShare.None))
        {
            var systemMessage = new SystemChatMessage(systemPrompt);
            var userMessage = new UserChatMessage("");
            ChatMessage[] messages = [systemMessage, userMessage];
            var batch = new BatchRequestInputObject("custom_id", new BatchBody(model, messages));
            var newLine = "\n"u8.ToArray();


            await foreach (var (id, text) in texts)
            {
                userMessage.Content = text;
                batch.CustomId = $"{id}";
                await JsonSerializer.SerializeAsync(stream, batch, _jsonSerializerOptions);
                stream.Write(newLine);
            }

            await stream.FlushAsync();
            stream.Close();
        }

        var fileReult = await client.GetOpenAIFileClient().UploadFileAsync(tempFile, FileUploadPurpose.Batch);
        if (fileReult.Value is null)
        {
            Console.Error.WriteLine($"Error uploading file.");
            throw new Exception($"Failed to upload file");
        }
        var fileId = fileReult.Value.Id;

        var batchClient = new BatchClient(_openAIKey);
        BinaryContent content;
        CreateBatchOperation? operation;
        var batchRequest = new BatchCreateRequest()
        {
            InputFileId = fileId,
            Endpoint = BatchEndpoint.ChatCompletions,
            Metadata = new()
            {
                { "job", job },
            },
        };

        JsonContent jsonContent = JsonContent.Create(batchRequest, options: _jsonSerializerOptions);
        content = BinaryContent.Create(jsonContent.ReadAsStream());
        operation = await batchClient.CreateBatchAsync(content, false);
        File.Delete(tempFile);
        return operation.BatchId;
    }

    public static async Task<Batch?> GetBatchAsync(string batchId)
    {
        var batchClient = new BatchClient(_openAIKey);
        var res = await batchClient.GetBatchAsync(batchId, null);
        if (res is null)
        {
            Console.Error.WriteLine($"Error getting batch with ID {batchId}.");
            throw new Exception($"Failed to get batch with ID {batchId}");
        }
        return res.GetRawResponse().Content.ToObjectFromJson<Batch>(_jsonSerializerOptions);
    }

    public static async IAsyncEnumerable<IdText> ReadBatchResponseAsync(Batch batch)
    {
        if (batch.OutputFileId is null)
        {
            Console.Error.WriteLine($"Batch {batch.Id} has no output file.");
            throw new Exception($"Batch {batch.Id} has no output file.");
        }
        var client = new OpenAIClient(_openAIKey);
        var fileClient = client.GetOpenAIFileClient();
        var fileResponse = await fileClient.DownloadFileAsync(batch.OutputFileId);
        if (fileResponse is null)
        {
            Console.Error.WriteLine($"Error downloading output file for batch {batch.Id}.");
            throw new Exception($"Failed to download output file for batch {batch.Id}");
        }


        using var stream = fileResponse.Value.ToStream();
        using var reader = new StreamReader(stream, Encoding.UTF8);
        string? line;
        while ((line = await reader.ReadLineAsync()) is not null)
        {
            var doc = JsonDocument.Parse(line).RootElement;
            if (doc.TryGetProperty("error", out var errorElement) && errorElement.ValueKind != JsonValueKind.Null)
            {
                Console.Error.WriteLine($"Error in batch response: {errorElement}");
                continue;
            }
            if (!int.TryParse(doc.GetProperty("custom_id").GetString(), out var id))
            {
                Console.Error.WriteLine($"Invalid custom_id in batch response: {doc.GetProperty("custom_id").GetString()}");
                continue;
            }
            var text = doc.GetProperty("response").GetProperty("body").GetProperty("choices")[0].GetProperty("message").GetProperty("content").GetString();
            if (text is null)
            {
                Console.Error.WriteLine($"No content in batch response for id {id}.");
                continue;
            }
            yield return new IdText(id, text);
        }
        reader.Close();
        stream.Close();
    }
}
