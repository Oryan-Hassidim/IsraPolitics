using CliArgsAttributes;
using israpolitics.Process;
using Spectre.Console;
using ZLinq;

namespace Israpolitics;


public class Program
{
    /// <summary>
    /// Queues a job for a specific person and subject.
    /// </summary>
    /// <param name="mkId">ID of the MK</param>
    /// <param name="subject">The subject name to procces.</param>
    /// <returns></returns>
    [CliCommand]
    public static async Task<int> AddJob(int mkId, string subject)
    {
        try
        {
            await Process.Filter(mkId, subject);
            return 0;
        }
        catch (Exception)
        {
            return 1;
        }
    }

    /// <summary>
    /// Queues multiple jobs from a file containing MK IDs and subjects.
    /// </summary>
    /// <param name="filePath"></param>
    /// <returns></returns>
    [CliCommand]
    public static async Task<int> AddJobs(FileInfo filePath)
    {
        var lines = File.ReadLinesAsync(filePath.FullName)
                    .Select((l, i) => (l, i))
                    .Distinct(EqualityComparer<(string, int)>.Create((a, b) => a.Item1 == b.Item1));
        List<(int id, string subject)> _tasks = [];
        await foreach (var (line, i) in lines)
        {
            // Assuming the line is in the format "MkId,Subject"
            var comma = line.IndexOf(',');
            if (comma == -1)
            {
                WriteLine($"Invalid line format in line {i}: {line}");
                continue;
            }
            var idSpan = line.AsSpan(0..comma);
            if (!int.TryParse(idSpan, out int mkId))
            {
                WriteLine($"Invalid MK ID: {idSpan} in line {i}: {line}");
                continue;
            }
            var subject = line.AsSpan(comma + 1).Trim();
            _tasks.Add((mkId, subject.ToString()));
        }
        await Parallel.ForEachAsync(_tasks, async (t, _) => await AddJob(t.id, t.subject));
        return 0;
    }


    /// <summary>
    /// Gets the ID of the MK based on the MK name.
    /// </summary>
    /// <param name="query">The query string to search for the MK name.</param>
    /// <returns></returns>
    [CliCommand]
    public static async Task<int> GetMks(string query)
    {
        var mks = await DbAccess.GetMksAsync(query);
        if (mks.Length == 0)
        {
            // write error message using Spectre.Console
            var panel = new Panel($"No MKs found for query: {query}")
            {
                Border = BoxBorder.Rounded,
                BorderStyle = new Style(Color.Red, decoration: Decoration.Bold),
                Padding = new Padding(1, 1),
                Header = new PanelHeader("Error", Justify.Left)
            };

            AnsiConsole.Write(panel);

            return 1;
        }
        // Display the MKs in a table format
        var table = new Table() { Border = TableBorder.Simple };
        table.AddColumns("ID", "First Name", "Surname", "Knesset Numbers", "Parties");

        foreach (var mk in mks)
        {
            var first = mk.First();
            var knessetNums = mk.Select(m => m.Knesset).Distinct().Join();
            var partyNames = mk.Select(m => m.PartyName).Distinct().Join();
            table.AddRow(mk.Key.ToString()!,
                         first.FirstName.Reverse(),
                         first.Surname.Reverse(),
                         knessetNums,
                         partyNames.Reverse());
        }
        AnsiConsole.Write(table);
        return 0;
    }


    [CliCommand]
    public static Task<int> Step()
    {
        return (Task<int>)Task.CompletedTask;
    }


    public static async Task<int> Main(string[] args)
    {
        WriteLine(Paths.RepositoryRoot);
        // Deserialize the JSON string into a dynamic object

#pragma warning disable CS0162 // Unreachable code detected
        return 0;

        // Uncomment the following line to run the AddEnititiesForTaggingToTable method
        // await AddEnititiesForTaggingToTable.Run();
        // Uncomment the following line to run the CLI entry point
        return await GeneratedCli.CliEntry.Build().Parse(args).InvokeAsync();
        return 0;
#pragma warning restore CS0162 // Unreachable code detected
    }
}
