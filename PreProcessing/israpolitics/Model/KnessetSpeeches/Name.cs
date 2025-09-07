using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace israpolitics.Model.KnessetSpeeches;

public class Name
{
    public Name()
    {
    }
    public Name(string? name)
    {
        String = name;
    }

    [Key]
    [Column("id")]
    public int Id { get; set; }
    [Column("name")]
    public string? String { get; set; }
}