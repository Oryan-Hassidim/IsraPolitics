using var Context = new Context();

var query = from speech in Context.KnessetSpeechesEntries
            where speech.PersonId == 482 && speech.Text!.Length > 25
            select new
            { speech.Id, speech.Text };

using (var ids = new StreamWriter("ids.txt", false, Encoding.UTF8))
using (var texts = new StreamWriter("texts.txt", false, Encoding.UTF8))
{
    foreach (var speech in query)
    {
        ids.WriteLine(speech.Id);
        texts.WriteLine(speech.Text.ReplaceLineEndings("  "));
    }
    ids.Flush();
    texts.Flush();
    ids.Close();
    texts.Close();
}

await AddEnititiesForTaggingToTable.Run();