using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace israpolitics.Model.KnessetSpeeches;

[Table("knesset_speeches")]
public class KnessetSpeech
{
    public KnessetSpeech()
    {
    }

    public KnessetSpeech(int id, string? text, Guid uuid,
        int knesset, long? sessionNumber,
        DateOnly date, int? personId, Name? name,
        bool chair,
        Topic? topic, TopicExtra? topicExtra = null,
        bool? qa = null, string? query=null, bool? onlyRead = null)
    {
        Id = id;
        Text = text;
        Uuid = uuid;
        Knesset = knesset;
        SessionNumber = sessionNumber;
        Date = date;
        PersonId = personId;
        Name = name;
        Chair = chair;
        Topic = topic;
        TopicExtra = topicExtra;
        Qa = qa;
        Query = query;
        OnlyRead = onlyRead;
    }

    [Key]
    [Column("id")]
    public int Id { get; set; }

    [Column("text")]
    public string? Text { get; set; }

    [Column("uuid")]
    public Guid Uuid { get; set; }

    [Column("knesset")]
    public int Knesset { get; set; }

    [Column("session_number")]
    public long? SessionNumber { get; set; }

    [Column("date")]
    public DateOnly Date { get; set; }

    [Column("person_id")]
    public int? PersonId { get; set; }

    [Column("name_id")]
    public int? NameId { get; set; }
    public Name? Name { get; set; }

    [Column("chair")]
    public bool Chair { get; set; }

    [Column("topic_id")]
    public int? TopicId { get; set; }
    public Topic? Topic { get; set; }

    [Column("topic_extra_id")]
    public int? TopicExtraId { get; set; }
    public TopicExtra? TopicExtra { get; set; }

    [Column("qa")]
    public bool? Qa { get; set; }

    [Column("query")]
    public string? Query { get; set; }

    [Column("only_read")]
    public bool? OnlyRead { get; set; }
}
