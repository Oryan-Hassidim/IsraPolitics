module IsraPolitics

open FSharp.Data
open IsraPolitics
open israpolitics.Model
open israpolitics.Model.KnessetSpeeches
open System

[<Literal>]
let csvSamplePath = @"C:\Projects\Oryan-Hassidim\IsraPolitics\Data\knesset_speeches_sample.csv"
let csvPath = @"C:\Projects\Oryan-Hassidim\IsraPolitics\Data\knesset_speeches.csv"

type KnessetSpeeches = CsvProvider<csvSamplePath>

let nullableBoolParse (s: string) : Nullable<bool> =
    match s with
    | "" -> Nullable<bool>()
    | _ -> Nullable<bool>(bool.Parse s)

[<EntryPoint>]
let main argv =
    let speeches = KnessetSpeeches.Load(csvPath)
    let mutable context = new Context()
    let mutable i = 0
    for speach in speeches.Rows do
        //let entry =
        //    new KnessetSpeech(
        //        speach.Column1,
        //        speach.Text,
        //        speach.Uuid,
        //        int64 speach.Knesset,
        //        int64 speach.Session_number,
        //        DateOnly.FromDateTime speach.Date,
        //        int speach.Person_id,
        //        speach.Name,
        //        speach.Chair,
        //        speach.Topic,
        //        speach.Topic_extra,
        //        nullableBoolParse speach.Qa,
        //        speach.Query,
        //        speach.Only_read
        //    )
        //context.KnessetSpeechesEntries.Add(entry) |> ignore
        i <- i + 1
        if i % 1_000 = 0 then
            context.SaveChanges() |> ignore
            Console.WriteLine(i)
        if i % 10_000 = 0 then
            context.Dispose()
            context <- new Context()
    context.SaveChanges() |> ignore
    0
