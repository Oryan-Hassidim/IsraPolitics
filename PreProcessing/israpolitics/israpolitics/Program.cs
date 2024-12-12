
using israpolitics.Model;
using israpolitics.Model.KnessetSpeeches;

//Context context = new();

//context.Database.EnsureCreated();

////KnessetSpeech speech = new()
////{
////    Id = 0,
////    Text = "אבקש מחברי הכנסת לכבד את כבוד נשיא המדינה בקימה. כבוד הנשיא! (חברי הכנסת מקדמים בקימה את פני נשיא המדינה.)",
////    Uuid = Guid.Parse("061775b9-6269-417c-848f-cf14605243c1"),
////    Knesset = 24,
////    SessionNumber = 155,
////    Date = DateOnly.ParseExact("2022-11-06", "yyyy-mm-dd"),
////    PersonId = null,
////    Name = new Name() { String = "מזכיר הכנסת דן מרזוק" },
////    Chair = false,
////    Topic = new Topic() { String = "ישיבה מיוחדת של הכנסת לזכרו של ראש הממשלה ושר הביטחון יצחק רבין, זיכרונו לברכה, במלאת 27 שנים להירצחו" },
////    TopicExtra = null,
////    Qa = false,
////    Query = "some query",
////    OnlyRead = true
////};


//var nameStr = "מזכיר הכנסת דן מרזוק";
//var name = context.Names.FirstOrDefault(n => n.String == nameStr, new(nameStr));


//var topicStr = "ישיבה מיוחדת של הכנסת לזכרו של ראש הממשלה ושר הביטחון יצחק רבין, זיכרונו לברכה, במלאת 27 שנים להירצחו";
//var topic = context.Topics.FirstOrDefault(t => t.String == topicStr, new(topicStr));

//KnessetSpeech speech = new(1, "נא לשבת.",
//    Guid.Parse("11e88450-3720-452e-a9df-f46b4d6d65d0"), 24, null,
//    DateOnly.ParseExact("2022-11-06", "yyyy-mm-dd"),
//    null, name, false,
//    topic);

//var entry = context.KnessetSpeechesEntries.Add(speech);
//context.SaveChanges();

//using (var context = new Context())
//{
//    context.Database.EnsureCreated();
//}

CsvToSqLite.ConvertPeople(@"C:\Projects\Oryan-Hassidim\IsraPolitics\Data\metadata.csv");
CsvToSqLite.ConvertKnessetSpeeches(@"C:\Projects\Oryan-Hassidim\IsraPolitics\Data\knesset_speeches.csv");