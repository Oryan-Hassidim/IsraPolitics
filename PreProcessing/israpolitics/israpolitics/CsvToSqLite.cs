using CsvHelper;
using israpolitics.Model;
using israpolitics.Model.KnessetSpeeches;
using System.Text;
using System.Text.RegularExpressions;

namespace IsraPolitics;

public static class CsvToSqLite
{
    //private static bool? GetNullableBool(ReadOnlySpan<char> input)
    //{
    //    if (input.IsEmpty) return null;
    //    return bool.Parse(input);
    //}
    //private static int? GetNullableIntBeforeDot(ReadOnlySpan<char> input)
    //{
    //    if (input.IsEmpty) return null;
    //    return GetIntBeforeDot(input);
    //}
    //private static long? GetNullableLongBeforeDot(ReadOnlySpan<char> input)
    //{
    //    if (input.IsEmpty) return null;
    //    return GetLongBeforeDot(input);
    //}
    //private static int? GetIntBeforeDot(ReadOnlySpan<char> input)
    //{
    //    int dotIndex = input.IndexOf('.');
    //    if (dotIndex != -1)
    //        return int.Parse(input[..dotIndex]);
    //    throw new FormatException("Invalid number format");
    //}
    //private static long GetLongBeforeDot(ReadOnlySpan<char> input)
    //{
    //    int dotIndex = input.IndexOf('.');
    //    if (dotIndex != -1)
    //        return long.Parse(input[..dotIndex]);
    //    throw new FormatException("Invalid number format");
    //}
    // private static T? ParseNullable<T>(Func<string, T> parser, string? value) where T : struct
    // {
    //     if (string.IsNullOrEmpty(value)) return null;
    //     return parser(value);
    // }
    // private static List<string> ParseCsvLine(ReadOnlySpan<char> line, List<string>? list = null)
    // {
    //     list ??= [];
    //     StringBuilder sb = new();
    //     while (true)
    //     {
    //         int comma = line.IndexOf(',');
    //         if (comma == -1)
    //         {
    //             list.Add(line.ToString());
    //             break;
    //         }
    //         int quote = line.IndexOf('"');
    //         if (quote == -1 || comma < quote)
    //         {
    //             list.Add(line[0..comma].ToString());
    //             line = line[(comma + 1)..];
    //             continue;
    //         }
    //         // find the closing quote without escaping
    //         line = line[1..];
    //         bool @continue = true;
    //         while (@continue)
    //         {
    //             int interest = line.IndexOf('"');
    //             if (interest == -1)
    //                 throw new FormatException("Unterminated quote");
    //             if (interest == line.Length - 1)
    //             {
    //                 sb.Append(line[0..interest]);
    //                 line = line[(interest + 1)..];
    //                 @continue = false;
    //             }
    //             else if (line[interest + 1] == ',')
    //             {
    //                 sb.Append(line[0..interest]);
    //                 line = line[(interest + 2)..];
    //                 @continue = false;
    //             }
    //             else if (line[interest + 1] == '"')
    //             {
    //                 sb.Append(line[0..(interest + 1)]);
    //                 line = line[(interest + 2)..];
    //             }
    //             else throw new FormatException();
    //         }
    //         list.Add(sb.ToString());
    //         sb.Clear();
    //     }
    //     return list;
    // }

    private static string? MapEmptyStringToNull(this string? input)
    {
        return string.IsNullOrEmpty(input) ? null : input;
    }

    //private static T? GetOptionalField<T>(this CsvReader reader, int index) where T : class
    //{
    //    var field = reader.GetField<string?>(index);
    //    return string.IsNullOrEmpty(field) ? null : reader.GetField<T>(index);
    //}


    private static T? GetOptionalField<T>(this CsvReader reader, int index) where T : struct
    {
        var field = reader.GetField<string?>(index);
        return string.IsNullOrEmpty(field) ? null : reader.GetField<T>(index);
    }

    public static DateOnly DateOnly(this DateTime dateTime)
    {
        return new DateOnly(dateTime.Year, dateTime.Month, dateTime.Day);
    }

    public static void ConvertKnessetSpeeches(string csvInput, string? sqLiteOutput = null)
    {
        var flag = true;

        using var fileStream = File.Open(csvInput, FileMode.Open);
        using var textReader = new StreamReader(fileStream);
        using var reader = new CsvReader(textReader, CultureInfo.InvariantCulture);
        reader.Read();
        reader.ReadHeader();

        Dictionary<string, int> names = [];
        Dictionary<string, int> topics = [];
        Dictionary<string, int> topicExtras = [];


        while (flag)
        {
            using var context = new Context();
            long i = 0;
            while (reader.Read() && i < 1_000L)
            {
                var nameStr = reader.GetField<string>(7)!;
                var topicStr = reader.GetField<string>(9)!;
                var topicExtraStr = reader.GetField<string?>(10).MapEmptyStringToNull();

                int topicExtraId = -1;
                if (!names.TryGetValue(nameStr, out int nameId))
                {
                    var name = new Name() { Id = names.Count + 1, String = nameStr };
                    context.Names.Add(name);
                    names[nameStr] = name.Id;
                    nameId = name.Id;
                }
                if (!topics.TryGetValue(topicStr, out int topicId))
                {
                    var topic = new Topic() { Id = topics.Count + 1, String = topicStr };
                    context.Topics.Add(topic);
                    topics[topicStr] = topic.Id;
                    topicId = topic.Id;
                }
                if (topicExtraStr is not null && !topicExtras.TryGetValue(topicExtraStr, out topicExtraId))
                {
                    var topicExtra = new TopicExtra() { Id = topicExtras.Count + 1, String = topicExtraStr };
                    context.TopicExtras.Add(topicExtra);
                    topicExtras[topicExtraStr] = topicExtra.Id;
                    topicExtraId = topicExtra.Id;
                }

                var entry = new KnessetSpeech()
                {
                    Id = reader.GetField<int>(0),
                    Text = reader.GetField<string>(1),
                    Uuid = reader.GetField<Guid>(2),
                    Knesset = (int)reader.GetField<decimal>(3),
                    SessionNumber = (long?)reader.GetField<decimal?>(4),
                    Date = reader.GetField<DateOnly>(5),
                    PersonId = (int?)reader.GetOptionalField<decimal>(6),
                    NameId = nameId,
                    Chair = reader.GetField<bool>(8),
                    TopicId = topicId,
                    TopicExtraId = topicExtraId == -1 ? null : topicExtraId,
                    Qa = reader.GetOptionalField<bool>(11),
                    Query = reader.GetField<string?>(12).MapEmptyStringToNull(),
                    OnlyRead = reader.GetOptionalField<bool>(13)
                };
                i++;
                context.KnessetSpeechesEntries.Add(entry);
            }
            Console.WriteLine(((double)fileStream.Position) / fileStream.Length);
            context.SaveChanges();
            if (textReader.EndOfStream) flag = false;
            Console.WriteLine($"File Position: {((double)fileStream.Position) / fileStream.Length}");
        }
    }

    public static void ConvertPeople(string csvInput, string? sqLiteOutput = null)
    {
        using var fileStream = File.Open(csvInput, FileMode.Open);
        using var textReader = new StreamReader(fileStream);
        using var reader = new CsvReader(textReader, CultureInfo.InvariantCulture);
        // accept 14/10/1885 and 1970-11-13 00:00:00
        reader.Context.TypeConverterOptionsCache.GetOptions<DateTime>().Formats = new[] { "dd/MM/yyyy", "yyyy-MM-dd HH:mm:ss" };
        reader.Read();
        reader.ReadHeader();
        using var context = new Context();
        context.Database.EnsureCreated();
        while (reader.Read())
        {
            var entry = new Person(
                id: reader.GetField<int>(0),
                personId: (int?)reader.GetOptionalField<decimal>(4),
                startDate: reader.GetOptionalField<DateOnly>(1),
                endDate: reader.GetOptionalField<DateOnly>(2),
                knesset: (int?)reader.GetOptionalField<decimal>(3),
                firstName: reader.GetField<string>(5)!,
                surname: reader.GetField<string>(6)!,
                gender: reader.GetField<string>(7)!.Contains("זכר"),
                factionId: (int?)reader.GetOptionalField<decimal>(9),
                faction: reader.GetField<string>(8).MapEmptyStringToNull(),
                partyName: reader.GetField<string>(10),
                dob: reader.GetOptionalField<DateTime>(11)?.DateOnly(),
                cob: reader.GetField<string>(12).MapEmptyStringToNull(),
                yod: (int?)reader.GetOptionalField<decimal>(13),
                yoi: (int?)reader.GetOptionalField<decimal>(14),
                city: reader.GetField<string>(15).MapEmptyStringToNull(),
                languages: reader.GetField<string>(16).MapEmptyStringToNull()
                );
            context.People.Add(entry);
        }
        context.SaveChanges();

    }
}

//public static partial class Helpers
//{
//    // regex pattern for matching a CSV line
//    [GeneratedRegex(@"(?<=^|,)(|[^""][^,]*|""(""""|[^""])*"")(?=$|,)")]
//    public static partial Regex CsvLinePattern { get; }
//}