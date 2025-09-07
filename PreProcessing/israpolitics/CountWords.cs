using israpolitics.Model;

namespace israpolitics;

public static class CountWords
{
    public static void Run()
    {

        Context context = new();
        context.Database.EnsureCreated();

        var file = File.CreateText("word_count.txt");

        int[] randomIds = [];
        int N = randomIds.Length;

        for (int i = 0; i < N; i++)
        {
            var id = randomIds[i];
            file.WriteLine(context.KnessetSpeechesEntries
                .Find(id)?.Text?
                .Count(c => c == ' ' || c == '\n'));
            if (i % 1000 == 0)
                Console.WriteLine($"{100 * i / N}%");
        }

        file.Close();
    }
}
