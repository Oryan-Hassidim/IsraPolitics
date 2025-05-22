using israpolitics.Model.KnessetSpeeches;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Conventions;
using System.Buffers;
using System.Text;
using ZLinq;

using static System.String;

namespace israpolitics;

static class TransformDb
{
    static IEnumerable<T> Distinct<T, T1>(this IEnumerable<T> source, Func<T, T1> map)
    {
        var comparer = new EqualityComparer<T, T1>(map);
        return source.Distinct(comparer);
    }

    static Dictionary<string, int> Histogram(ReadOnlySpan<char> text)
    {
        Dictionary<string, int> histogram = [];
        var alternate = histogram.GetAlternateLookup<ReadOnlySpan<char>>();
        foreach (Range word in text.SplitAny(SearchValues.Create(" .,:;!?()[]{}<>\"1234567890\t\r\n'")))
        {
            if (word.End.Value - word.Start.Value < 2) continue;
            alternate[text[word]] = alternate.TryGetValue(text[word], out var count) ? count + 1 : 1;
        }
        return histogram;
    }

    static bool AlmostEqualString(string? str1, string? str2)
    {
        if (IsNullOrEmpty(str1) && IsNullOrEmpty(str2)) return true;
        if (IsNullOrEmpty(str1) || IsNullOrEmpty(str2)) return false;
        if (str1.Length != str2.Length) return false;
        if (str1 == str2) return true;
        if (Math.Abs(str1.Length - str2.Length) > 4) return false;
        if (str1.AsSpan().AsValueEnumerable().Where(c => 'א' <= c && c <= 'ת').Take(100).SequenceEqual(
            str2.AsSpan().AsValueEnumerable().Where(c => 'א' <= c && c <= 'ת').Take(100)))
            return true;
        var hist1 = Histogram(str1.AsSpan()[..Math.Min(150, str1.Length)]);
        var hist2 = Histogram(str2.AsSpan()[..Math.Min(150, str1.Length)]);
        var keys = hist1.Keys.Union(hist2.Keys);
        var dotProduct = 0;
        var norm1 = 0;
        var norm2 = 0;
        foreach (var key in keys)
        {
            var count1 = hist1.TryGetValue(key, out var count) ? count : 0;
            var count2 = hist2.TryGetValue(key, out count) ? count : 0;
            dotProduct += count1 * count2;
            norm1 += count1 * count1;
            norm2 += count2 * count2;
        }
        var similarity = dotProduct / Math.Sqrt(norm1 * norm2);
        if (similarity > 0.85)
            return true;
        return false;
    }

    static bool AlmostEqualsSpeech(KnessetSpeech speech1, KnessetSpeech speech2) =>
        speech1.Date == speech2.Date
        && speech1.PersonId == speech2.PersonId
        && speech1.TopicId == speech2.TopicId
        && speech1.TopicExtraId == speech2.TopicExtraId
        && AlmostEqualString(speech1.Text, speech2.Text);

    class StringAndDate
    {
        public required string? String { get; set; }
        public required DateOnly Date { get; set; }
    }

    class SpeechesComparer : IEqualityComparer<KnessetSpeech>
    {
        public bool Equals(KnessetSpeech? x, KnessetSpeech? y)
        {
            if (x is null && y is null) return true;
            if (x is null || y is null) return false;
            return AlmostEqualsSpeech(x, y);
        }
        public int GetHashCode(KnessetSpeech obj) =>
            HashCode.Combine(
                obj.Date,
                obj.PersonId,
                obj.TopicId);
    }

    class EqualityComparer<T, T1>(Func<T, T1> prop1) : IEqualityComparer<T>
    {
        public bool Equals(T? x, T? y)
        {
            if (x is null && y is null) return true;
            if (x is null || y is null) return false;
            var x1 = prop1(x);
            var y1 = prop1(y);
            if (x1 is null && y1 is null) return true;
            if (x1 is null || y1 is null) return false;
            return x1.Equals(y1);
        }
        public int GetHashCode(T obj) => HashCode.Combine(prop1(obj));
    }

    class EqualityComparer<T, T1, T2>(Func<T, T1> prop1, Func<T, T2> prop2) : IEqualityComparer<T>
    {
        public bool Equals(T? x, T? y)
        {
            if (x is null && y is null) return true;
            if (x is null || y is null) return false;
            var x1 = prop1(x);
            var y1 = prop1(y);
            var x2 = prop2(x);
            var y2 = prop2(y);
            return (x1, y1, x2, y2) switch
            {
                (null, null, null, null) => true,
                (not null, not null, null, null) => x1.Equals(y1),
                (null, null, not null, not null) => x2.Equals(y2),
                (null, _, _, _) or (_, null, _, _) or (_, _, null, _) or (_, _, _, null) => false,
                _ => x1.Equals(y1) && x2.Equals(y2),
            };
        }
        public int GetHashCode(T obj) => HashCode.Combine(prop1(obj), prop2(obj));
    }

    public static void Run()
    {
        var old_model = new Context(@"C:\Projects\Oryan-Hassidim\IsraPolitics\Data\OldIsraParlTweet.db");
        var model = new Context();
        //model.Database.EnsureDeleted();
        //model.Database.EnsureCreated();

        #region Topics
        var sortedTopics = old_model.KnessetSpeechesEntries
                                    .Where(s => s.Topic != null)
                                    .Select(s => new { Topic = s.Topic!, Date = s.Date })
                                    .Distinct()
                                    .OrderBy(s => s.Date)
                                    .Select(s => s.Topic)
                                    .ToList()
                                    .Distinct(s => s.Id)
                                    .GroupBy(s => s.String!.AsValueEnumerable()
                                                   .Where(c => c is >= 'א' and <= 'ת')
                                                   .JoinToString(""))
                                    .Select((g, i) => new { g, Max = new Topic() { Id = i + 1, String = g.MaxBy(s => s.String!.Length)!.String } })
                                    .ToList();
        var topicsDict = sortedTopics
                         .SelectMany(g => g.g.Select(s => (s.Id, g.Max.Id)))
                         .ToDictionary();

        //model.Topics.AddRange(sortedTopics.Select(s => s.Max));
        //model.SaveChanges();
        //model.Dispose();
        //model = new Context();
        #endregion

        #region TopicExtras
        var sortedTopicsExtra = old_model.KnessetSpeechesEntries
                                     .Where(s => s.TopicExtra != null)
                                     .Select(s => new { TopicExtra = s.TopicExtra!, Date = s.Date })
                                     .Distinct()
                                     .OrderBy(s => s.Date)
                                     .Select(s => s.TopicExtra)
                                     .ToList()
                                     .Distinct(s => s.Id)
                                     .GroupBy(s => s.String!.AsValueEnumerable()
                                                    .Where(c => c is >= 'א' and <= 'ת')
                                                    .JoinToString(""))
                                     .Select((g, i) => new { g, Max = new TopicExtra() { Id = i + 1, String = g.MaxBy(s => s.String!.Length)!.String } })
                                     .ToList();

        var topicsExtraDict = sortedTopicsExtra
                              .SelectMany((g, i) => g.g.Select(s => (s.Id, g.Max.Id)))
                              .ToDictionary();

        //model.TopicExtras.AddRange(sortedTopicsExtra.Select(s => s.Max));
        //model.SaveChanges();
        //model.Dispose();
        //model = new Context();
        #endregion

        #region Pepole, Names
        //model.People.AddRange(old_model.People);
        //model.Names.AddRange(old_model.Names);
        //model.SaveChanges();
        //model.Dispose();
        //model = new Context();
        #endregion

        #region speeches
        var total = (double)4484726;
        var speeches = old_model.KnessetSpeechesEntries
                                .OrderBy(x => x.Date)
                                .ThenBy(x => x.Id)
                                .Include(x => x.Topic)
                                .Include(x => x.TopicExtra);

        var speechComparer = new SpeechesComparer();
        var sets = new Dictionary<int, Dictionary<int, HashSet<KnessetSpeech>>>();
        var empty = new HashSet<KnessetSpeech>();
        int newId = 0;
        DateOnly lastDate = default;
        foreach (var speech in speeches)
        {
            if (lastDate != speech.Date)
            {
                sets.Clear();
                lastDate = speech.Date;
            }

            if (speech.Topic != null)
                speech.TopicId = topicsDict[speech.TopicId!.Value];
            if (speech.TopicExtra != null)
                speech.TopicExtraId = topicsExtraDict[speech.TopicExtraId!.Value];
            speech.Topic = null;
            speech.TopicExtra = null;
            speech.Name = null;

            int key = speech.PersonId is null ? -1 : speech.PersonId.Value;
            if (!sets.TryGetValue(key, out var set))
                sets.Add(key, set = []);
            int len = speech.Text!.Length;
            if (Enumerable.Range(len - 3, 6)
                .Any(l => set.GetValueOrDefault(l, empty).Contains(speech)))
                continue;

            if (!set.TryGetValue(len, out var speechesSet))
                set.Add(len, speechesSet = new HashSet<KnessetSpeech>(speechComparer));

            speechesSet.Add(speech);
            speech.Id = ++newId;
            model.KnessetSpeechesEntries.Add(speech);
            model.SaveChanges();
            if (newId % 1000 == 0)
            {
                model.Dispose();
                model = new Context();
                WriteLine($"Saved {newId} speeches ({newId / total:.3%})");
            }
        }
        model.SaveChanges();
        model.Dispose();
        #endregion
    }
}