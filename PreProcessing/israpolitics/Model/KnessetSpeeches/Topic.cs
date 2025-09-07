using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace israpolitics.Model.KnessetSpeeches;

public class Topic
{
    public Topic()
    {
    }

    public Topic(string? topic)
    {
        String = topic;
    }

    [Key]
    [Column("id")]
    public int Id { get; set; }
    [Column("topic")]
    public string? String { get; set; }
}