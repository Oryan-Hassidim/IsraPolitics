using CsvHelper;

using var Context = new Context();

var ids = (await File.ReadAllLinesAsync(@"C:\Users\oryan\Desktop\filtered_ids.txt", Encoding.UTF8)).Select(int.Parse);

var query = from speech in Context.KnessetSpeechesEntries
            where ids.Contains(speech.Id)
            orderby speech.Date
            select new
            { speech.Id, speech.Date, Topic = speech.Topic!.String, speech.Text };

using (var csv = new CsvWriter(new StreamWriter(@"C:\Users\oryan\Desktop\filtered_speeches.csv", false, Encoding.UTF8), CultureInfo.InvariantCulture))
{
    await csv.WriteRecordsAsync(query);
}

//await AddEnititiesForTaggingToTable.Run();