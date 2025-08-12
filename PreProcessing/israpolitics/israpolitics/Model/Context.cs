using israpolitics.Model.KnessetSpeeches;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;

namespace israpolitics.Model;

public class Context : DbContext
{
    private readonly string _sqlitePath;
    private readonly bool _readOnly = false;

    // private readonly string _sqlitePath;

    public DbSet<Person> People { get; set; }
    public DbSet<KnessetSpeech> KnessetSpeechesEntries { get; set; }
    public DbSet<Name> Names { get; set; }
    public DbSet<Topic> Topics { get; set; }
    public DbSet<TopicExtra> TopicExtras { get; set; }

    public Context(string sqlitePath, bool readOnly = false) : base()
    {
        _sqlitePath = sqlitePath;
        _readOnly = readOnly;
    }

    public Context() : this(@"C:\Projects\Oryan-Hassidim\IsraPolitics\Data\IsraParlTweet.db", false)
    {
    }

    public Context(string sqlitePath, DbContextOptions<Context> options) : base(options)
    {
        _sqlitePath = sqlitePath;
    }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        if (!optionsBuilder.IsConfigured)
        {
            optionsBuilder.UseSqlite($"Data Source=\"{_sqlitePath}\"{(_readOnly ? ";Mode=ReadOnly" : "")}")
                //.EnableSensitiveDataLogging()
                //.LogTo(WriteLine, LogLevel.Information)
                ;
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
