using israpolitics;
using israpolitics.Model;
using static System.Console;

var set = new HashSet<int>(10_000);
using var file = File.OpenWrite("bezalel_10000.txt");
using var writer = new StreamWriter(file);
using var context = new Context();
int max = context.KnessetSpeechesEntries.Count();
int counter = 0;

Write($"{counter:D5}/{10_000:D5}");

while (counter < 10_000)
{
    int id = Random.Shared.Next(1, max + 1);
    if (set.Contains(id)) continue;
    set.Add(id);
    string? text = context.KnessetSpeechesEntries.Find(id)?.Text;
    if (text is null) continue;
    if (text.Length < 40) continue;
    writer.WriteLine(text.ReplaceLineEndings("  "));
    counter++;
    // clear the line
    if (counter % 100 == 0)
    {
        SetCursorPosition(0, CursorTop);
        Write($"{counter:D5}/{10_000:D5}");
    }
}

await writer.FlushAsync();
await file.FlushAsync();
writer.Close();