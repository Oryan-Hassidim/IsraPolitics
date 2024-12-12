using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Reflection;

namespace israpolitics.Model;

public class Person
{
    public Person()
    {
    }

    public Person(int id, int? personId, 
        DateOnly? startDate, DateOnly? endDate, 
        int? knesset, 
        string firstName, string surname,
        bool gender,
        int? factionId, string? faction, string? partyName,
        DateOnly? dob, string? cob,
        int? yod, int? yoi,
        string? city, string? languages)
    {
        Id = id;
        PersonId = personId;
        StartDate = startDate;
        EndDate = endDate;
        Knesset = knesset;
        FirstName = firstName;
        Surname = surname;
        Gender = gender;
        FactionId = factionId;
        Faction = faction;
        PartyName = partyName;
        Dob = dob;
        Cob = cob;
        Yod = yod;
        Yoi = yoi;
        City = city;
        Languages = languages;
    }

    [Key]
    [Column("id")]
    public int Id { get; set; }

    [Column("person_id")]
    public int? PersonId { get; set; }
    [Column("start_date")]
    public DateOnly? StartDate { get; set; }
    [Column("end_date")]
    public DateOnly? EndDate { get; set; }
    [Column("knesset")]
    public int? Knesset { get; set; }
    [Column("first_name")]
    public string FirstName { get; set; }
    [Column("surname")]
    public string Surname { get; set; }
    [Column("gender")]
    public bool Gender { get; set; }
    [Column("faction_id")]
    public int? FactionId { get; set; }
    [Column("faction")]
    public string? Faction { get; set; }
    [Column("party_name")]
    public string? PartyName { get; set; }
    [Column("dob")]
    public DateOnly? Dob { get; set; }
    [Column("cob")]
    public string? Cob { get; set; }
    [Column("yod")]
    public int? Yod { get; set; }
    [Column("yoi")]
    public int? Yoi { get; set; }
    [Column("city")]
    public string? City { get; set; }
    [Column("languages")]
    public string? Languages { get; set; }
}