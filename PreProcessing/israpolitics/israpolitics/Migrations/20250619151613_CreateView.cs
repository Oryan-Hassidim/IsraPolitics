using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace israpolitics.Migrations;

/// <inheritdoc />
public partial class CreateView : Migration
{
    /// <inheritdoc />
    protected override void Up(MigrationBuilder migrationBuilder)
    {
		migrationBuilder.Sql(@"
			CREATE VIEW IF NOT EXISTS 
			knesset_speeches_view AS
			SELECT 
				k.id,
				n.name,
				k.text,
				k.knesset,
				k.session_number,
				k.date,
				t.topic,
				te.topic_extra,
				k.person_id,
				k.name_id,
				k.chair,
				k.topic_id,
				k.topic_extra_id,
				k.qa,
				k.query,
				k.only_read,
				k.uuid
			FROM knesset_speeches AS k
			LEFT JOIN topics AS t ON k.topic_id = t.id
			LEFT JOIN topic_extras AS te ON k.topic_extra_id = te.id
			LEFT JOIN names AS n ON k.name_id = n.id;");
    }

    /// <inheritdoc />
    protected override void Down(MigrationBuilder migrationBuilder)
    {
		migrationBuilder.Sql("DROP VIEW IF EXISTS knesset_speeches_view");
    }
}
