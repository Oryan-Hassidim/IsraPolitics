using CsvHelper.Configuration;
using Microsoft.EntityFrameworkCore;
using System.ClientModel;
//using System.Linq;

namespace israpolitics.Process;

public class Process
{
    private const string _filterFileName = "filter.txt";
    private const string _rankFileName = "rank.txt";

    private record CsvRow(int Id, DateOnly Date, string Topic, string Text, int Rank);

    public static async Task Filter(int mkId, string subject)
    {
        var dirPath = Path.Combine(Paths.JobsDirectory, mkId.ToString(), subject);
        if (Directory.Exists(dirPath))
            throw new InvalidOperationException($"Job for {mkId} {subject} already exists.");
        using var context = new Context();
        var query = context.KnessetSpeechesEntries
                           .AsNoTracking()
                           .Where(s => s.PersonId == mkId && s.Text != null)
                           .Select(s => new IdText(s.Id, s.Text!))
                           .AsAsyncEnumerable();
        var prompt = File.ReadAllText(Path.Combine(Paths.PromptsDirectory, subject, _filterFileName));
        var batchId = await OpenAIBatchJobs.CreateBatchJob(prompt, $"filter~{mkId}~{subject}", query, "gpt-4.1-mini");
        var dir = Directory.CreateDirectory(dirPath);
        await File.WriteAllTextAsync(Path.Combine(dir.FullName, _filterFileName), batchId);
    }

    public static async Task<bool> TryRankAsync(int mkId, string subject)
    {
        var dir = Directory.CreateDirectory(Path.Combine(Paths.JobsDirectory, mkId.ToString(), subject));
        var batchIdFile = Path.Combine(dir.FullName, _filterFileName);
        if (!File.Exists(batchIdFile)) return false;

        var batchId = await File.ReadAllTextAsync(batchIdFile);
        if (string.IsNullOrWhiteSpace(batchId)) return false;

        var batch = await OpenAIBatchJobs.GetBatchAsync(batchId);
        if (batch is null)
        {
            Console.Error.WriteLine($"Batch {batchId} does not exist.");
            return false;
        }
        if (batch.Status != BatchStatus.Completed)
        {
            Console.Error.WriteLine($"Batch {batchId} status: {batch.Status} ({batch.RequestCounts.Completed / batch.RequestCounts.Total: 0.00%})");
            return false;
        }
        using var context = new Context();
        var speeches = context.KnessetSpeechesEntries.AsNoTracking();
        var filterPrompt = await File.ReadAllTextAsync(Path.Combine(Paths.PromptsDirectory, subject, _filterFileName));
        AddEnititiesForTaggingToTable addEntities = new();

        var texts = OpenAIBatchJobs.ReadBatchResponseAsync(batch)
                                   .SelectAsync(async it =>
                                   {
                                       var id = it.Id;
                                       var speech = await speeches.FirstAsync(s => s.Id == it.Id && s.Text != null);
                                       var text = speech.Text!;
                                       if (!int.TryParse(it.Text, out int score))
                                       {
                                           Console.Error.WriteLine($"Invalid score for ID {id}: {it.Text}");
                                           return null;
                                       }
                                       var probability = score switch
                                       {
                                           1 => 0.01,
                                           2 => 0.02,
                                           3 => 0.01,
                                           _ => -1
                                       };
                                       if (probability < 0)
                                       {
                                           Console.Error.WriteLine($"Invalid score for ID {id}: {score}");
                                           return null;
                                       }
                                       if (Random.Shared.NextDouble() < probability)
                                           await addEntities.AddAsync(id, filterPrompt, score, text);
                                       return new
                                       {
                                           Id = id,
                                           Text = text,
                                           Score = score
                                       };
                                   })
                                   .Where(it => it is not null && it.Score >= 4)
                                   .Select(s => new IdText(s!.Id, s!.Text));
        File.Delete(batchIdFile);
        var prompt = File.ReadAllText(Path.Combine(Paths.PromptsDirectory, subject, "rank.txt"));
        batchId = await OpenAIBatchJobs.CreateBatchJob(prompt, $"rank~{mkId}~{subject}", texts, "gpt-4.1");
        if (string.IsNullOrWhiteSpace(batchId))
        {
            WriteLine($"Failed to create batch job for ranking {mkId} {subject}");
            return false;
        }
        await File.WriteAllTextAsync(Path.Combine(dir.FullName, "rank.txt"), batchId);
        return true;
    }

    public static async Task<bool> TryFinishAsync(int mkId, string subject)
    {
        var dir = Directory.CreateDirectory(Path.Combine(Paths.JobsDirectory, mkId.ToString(), subject));
        var rankFile = Path.Combine(dir.FullName, _rankFileName);
        if (!File.Exists(rankFile)) return false;
        var batchId = await File.ReadAllTextAsync(rankFile);
        if (string.IsNullOrWhiteSpace(batchId)) return false;
        var batch = await OpenAIBatchJobs.GetBatchAsync(batchId);
        if (batch is null)
        {
            WriteLine($"Batch {batchId} does not exist.");
            return false;
        }
        if (batch.Status != BatchStatus.Completed)
        {
            WriteLine($"Batch {batchId} status: {batch.Status} ({batch.RequestCounts.Completed / batch.RequestCounts.Total: 0.00%})");
            return false;
        }
        using var context = new Context();
        var speeches = context.KnessetSpeechesEntries.AsNoTracking().Include(s => s.Topic);
        var rankPrompt = await File.ReadAllTextAsync(Path.Combine(Paths.PromptsDirectory, subject, _rankFileName));
        AddEnititiesForTaggingToTable addEntities = new();
        var clientDataFile = Path.Combine(Paths.ClientDataDirectory, mkId.ToString(), $"{subject}.csv");
        using var writer = File.CreateText(clientDataFile);
        using CsvHelper.CsvWriter csvWriter = new(writer, CultureInfo.GetCultureInfo("he-il"));
        csvWriter.WriteHeader<CsvRow>();

        await foreach (var it in OpenAIBatchJobs.ReadBatchResponseAsync(batch))
        {
            var id = it.Id;
            var speech = await speeches.FirstAsync(s => s.Id == id && s.Text != null);
            var text = speech.Text!;
            if (!int.TryParse(it.Text, out int score))
            {
                Console.Error.WriteLine($"Invalid score for ID {id}: {it.Text}");
                continue;
            }
            var probability = score switch
            {
                1 or 5 => 0.005,
                2 or 3 or 4 => 0.01,
                _ => -1,
            };
            if (Random.Shared.NextDouble() < probability)
                await addEntities.AddAsync(id, rankPrompt, score, text);
            csvWriter.WriteRecord<CsvRow>(new(id, speech.Date, speech.Topic.String, speech.Text!, score));
        }
        File.Delete(rankFile);
        return true;
    }

    public static async Task Step()
    {
        static (int MkId, string Subject)? ExtractPersonIdAndSubject(string f)
        {
            var parts = f.Split(Path.DirectorySeparatorChar);
            if (parts.Length < 3) return null;
            if (!int.TryParse(parts[^3], out int id)) return null;
            var subject = parts[^2];
            if (string.IsNullOrWhiteSpace(subject)) return null;
            return (id, subject);
        }

        var filters = Directory.EnumerateFiles(Paths.JobsDirectory, _filterFileName, SearchOption.AllDirectories)
            .Select(ExtractPersonIdAndSubject)
            .WhereNotNull()
            .Select();
        var ranks = Directory.EnumerateFiles(Paths.JobsDirectory, _rankFileName, SearchOption.AllDirectories)
            .Select(ExtractPersonIdAndSubject)
            .WhereNotNull();
        var tasks = new List<(int id, string subject)>();
        foreach (var personDir in Directory.EnumerateDirectories(Paths.JobsDirectory))
        {
            var personIdStr = Path.GetFileName(personDir);
            if (!int.TryParse(personIdStr, out int personId))
            {
                WriteLine($"Invalid person ID: {personIdStr}");
                continue;
            }
            foreach (var subjectDir in Directory.EnumerateDirectories(personDir))
            {
                var subject = Path.GetFileName(subjectDir);
                if (string.IsNullOrWhiteSpace(subject))
                {
                    WriteLine($"Invalid subject directory: {subjectDir}");
                    continue;
                }
                var ranked = await TryRankAsync(personId, subject);
                if (ranked)
                {
                    WriteLine($"Started ranking for {personId} {subject}");
                    continue;
                }
                var finished = await TryFinishAsync(personId, subject);
                if (finished)
                {
                    WriteLine($"Finished processing for {personId} {subject}");
                    continue;
                }
            }
        }
    }

}