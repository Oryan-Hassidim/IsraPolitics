using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace israpolitics.Model.KnessetSpeeches;

public class TopicExtra
{
    public TopicExtra()
    {
    }

    public TopicExtra(string? text)
    {
        String = text;
    }

    [Key]
    [Column("id")]
    public int Id { get; set; }
    [Column("topic_extra")]
    public string? String { get; set; }
}