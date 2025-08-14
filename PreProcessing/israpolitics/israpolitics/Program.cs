

using CliArgsAttributes;
using SQLitePCL;
using System.Text.RegularExpressions;
using System.Windows.Markup;
using ZLinq;

namespace Israpolitics;

public class Program
{
    /// <summary>
    /// Queues a job for a specific person and subject.
    /// </summary>
    /// <param name="MkId">ID of the MK</param>
    /// <param name="subject">The subject name to procces.</param>
    /// <returns></returns>
    [CliCommand]
    public static Task<int> AddJob(int MkId, string subject)
    {
        return Task.FromResult(0);
    }

    /// <summary>
    /// 
    /// </summary>
    /// <param name="filePath"></param>
    /// <returns></returns>
    [CliCommand]
    public static Task<int> AddJobs(FileInfo filePath)
    {
        foreach (var (line,i) in File.ReadLines(filePath.FullName).Select((l,i) =>(l,i))
        {
            // Assuming the line is in the format "MkId,Subject"
            var comma = line.IndexOf(',');
            if (comma == -1)
            {
                Console.WriteLine($"Invalid line format: {line}");
                continue;
            }
            var idSpan = line.AsSpan(0..comma);
            if (!int.TryParse(idSpan, out int mkId))
            {
                Console.WriteLine($"Invalid MK ID: {idSpan} in line: {line}");
                continue;
            }-
            string subject = vals[1].ToString().Trim();
            AddJob(mkId, )
        }
        return Task.FromResult(0);
    }


    /// <summary>
    /// Gets the ID of the MK based on the MK name.
    /// </summary>
    /// <param name="query">The query string to search for the MK name.</param>
    /// <returns></returns>
    [CliCommand]
    public static Task<int> GetMkID(string query)
    {
        return Task.FromResult(0);
    }


    [CliCommand]
    public static Task<int> Step()
    {
        return Task.CompletedTask;
    }


    public static async Task<int> Main(string[] args)
    {
        // Uncomment the following line to run the AddEnititiesForTaggingToTable method
        // await AddEnititiesForTaggingToTable.Run();
        // Uncomment the following line to run the CLI entry point
        return await GeneratedCli.CliEntry.Build().Parse(args).InvokeAsync();
#pragma warning disable CS0162 // Unreachable code detected
        return 0;
#pragma warning restore CS0162 // Unreachable code detected
    }
}
