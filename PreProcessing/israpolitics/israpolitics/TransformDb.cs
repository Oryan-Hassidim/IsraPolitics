using israpolitics.Model.KnessetSpeeches;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Conventions;
using System.Buffers;
using System.Diagnostics;
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

    public static bool AlmostEqualString(string? str1, string? str2)
    {
        if (IsNullOrEmpty(str1) && IsNullOrEmpty(str2)) return true;
        if (IsNullOrEmpty(str1) || IsNullOrEmpty(str2)) return false;
        var s1 = str1.AsSpan().Trim();
        var s2 = str2.AsSpan().Trim();
        if (Math.Abs(s1.Length - s2.Length) > 3) return false;
        if (s1 == s2) return true;
        if (s1.AsValueEnumerable().Where(c => 'א' <= c && c <= 'ת').Take(400).SequenceEqual(
            s2.AsValueEnumerable().Where(c => 'א' <= c && c <= 'ת').Take(400)))
            return true;
        var len = Math.Min(400, Math.Min(s1.Length, s2.Length));
        var hist1 = Histogram(s1[..len]);
        var hist2 = Histogram(s2[..len]);
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
        if (similarity > 0.9)
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
        var old_model = new Context(@"C:\Projects\Oryan-Hassidim\IsraPolitics\Data\IsraParlTweet.v2.db", readOnly: true);
        var model = new Context();// @"C:\Projects\Oryan-Hassidim\IsraPolitics\Data\IsraParlTweet2.db");
        try
        {
            WriteLine("Deleting old database...");
            model.Database.EnsureDeleted();
            WriteLine("Creating new database...");
            model.Database.EnsureCreated();

            #region Topics, TopicExtras, People, Names
            WriteLine("Transforming Topics...");
            model.Topics.AddRange(old_model.Topics);
            WriteLine("Transforming TopicExtras...");
            model.TopicExtras.AddRange(old_model.TopicExtras);
            WriteLine("Transforming People...");
            model.People.AddRange(old_model.People);
            WriteLine("Transforming Names...");
            model.Names.AddRange(old_model.Names);
            model.SaveChanges();
            model.Dispose();
            WriteLine("Completed");
            model = new Context();
            #endregion

            #region speeches
            WriteLine("Transforming Speeches...");
            var total = (double)2380777;
            var speeches = old_model.KnessetSpeechesEntries
                                    .AsNoTracking()
                                    .OrderBy(x => x.Id)
                                    .IgnoreAutoIncludes();

            var speechComparer = new SpeechesComparer();
            var sets = new Dictionary<int, Dictionary<int, HashSet<KnessetSpeech>>>();
            var empty = new HashSet<KnessetSpeech>();
            int newId = 0, counter = 0;
            DateOnly lastDate = default;
            foreach (var speech in speeches)
            {
                counter++;
                if (lastDate != speech.Date)
                {
                    sets.Clear();
                    lastDate = speech.Date;
                }
                speech.Text = speech.Text!.ReplaceLineEndings(" ").Trim();

                int key = speech.PersonId is null ? -1 : speech.PersonId.Value;
                if (!sets.TryGetValue(key, out var set))
                    sets.Add(key, set = []);
                int len = speech.Text!.Length;
                KnessetSpeech? copy = null;
                if (Enumerable.Range(len - 3, 7)
                              .Select(l => set.GetValueOrDefault(l, empty))
                              .Any(s => s.TryGetValue(speech, out copy)))
                {
                    continue;
                }

                if (!set.TryGetValue(len, out var speechesSet))
                    set.Add(len, speechesSet = new HashSet<KnessetSpeech>(speechComparer));

                speechesSet.Add(speech);
                speech.Id = ++newId;
                speech.Name = null;
                speech.Topic = null;
                speech.TopicExtra = null;

                model.KnessetSpeechesEntries.Add(speech);
                if (newId % 10_000 == 0)
                {
                    model.SaveChanges();
                    model.Dispose();
                    //GC.Collect();
                    //GC.WaitForPendingFinalizers();
                    //GC.Collect();
                    model = new Context();
                    SetCursorPosition(0, CursorTop - 1);
                    WriteLine($"Saved {newId} speeches ({counter / total:P3})");
                }
            }
            model.SaveChanges();
            model.Dispose();
            SetCursorPosition(0, CursorTop - 1);
            WriteLine($"Saved {newId} speeches ({counter / total:P3})");
            #endregion
        }
        finally
        {
            old_model.Dispose();
            model.Dispose();
        }
    }
}