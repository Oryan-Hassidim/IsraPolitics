using System.ComponentModel.DataAnnotations.Schema;
using israpolitics.Model.KnessetSpeeches;
using Microsoft.EntityFrameworkCore;

namespace israpolitics.Model;

public class Context : DbContext
{
    // private readonly string _sqlitePath;

    public DbSet<Person> People { get; set; }
    public DbSet<KnessetSpeech> KnessetSpeechesEntries { get; set; }
    public DbSet<Name> Names { get; set; }
    public DbSet<Topic> Topics { get; set; }
    public DbSet<TopicExtra> TopicExtras { get; set; }

    public Context() : base()
    {
    }

    public Context(DbContextOptions<Context> options) : base(options)
    {
    }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        if (!optionsBuilder.IsConfigured)
        {
            optionsBuilder.UseSqlite("Data Source=\"C:\\Projects\\Oryan-Hassidim\\IsraPolitics\\Data\\IsraParlTweet.db\"");
            optionsBuilder.EnableSensitiveDataLogging();
        }
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<KnessetSpeech>().ToTable("knesset_speeches");
        modelBuilder.Entity<KnessetSpeech>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Id).ValueGeneratedNever();
        });

        modelBuilder.Entity<Person>().ToTable("people");
        modelBuilder.Entity<Person>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Id).ValueGeneratedNever();
        });

        modelBuilder.Entity<Name>().ToTable("names");
        modelBuilder.Entity<Name>().HasIndex(e => e.String).IsUnique();

        modelBuilder.Entity<Topic>().ToTable("topics");
        modelBuilder.Entity<Topic>().HasIndex(e => e.String).IsUnique();

        modelBuilder.Entity<TopicExtra>().ToTable("topic_extras");
        modelBuilder.Entity<TopicExtra>().HasIndex(e => e.String).IsUnique();
    }
}
