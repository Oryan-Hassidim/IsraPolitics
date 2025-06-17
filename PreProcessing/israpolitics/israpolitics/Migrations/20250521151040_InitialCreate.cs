using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace israpolitics.Migrations
{
    /// <inheritdoc />
    public partial class InitialCreate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "names",
                columns: table => new
                {
                    id = table.Column<int>(type: "INTEGER", nullable: false)
                        .Annotation("Sqlite:Autoincrement", true),
                    name = table.Column<string>(type: "TEXT", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_names", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "people",
                columns: table => new
                {
                    id = table.Column<int>(type: "INTEGER", nullable: false),
                    person_id = table.Column<int>(type: "INTEGER", nullable: true),
                    start_date = table.Column<DateOnly>(type: "TEXT", nullable: true),
                    end_date = table.Column<DateOnly>(type: "TEXT", nullable: true),
                    knesset = table.Column<int>(type: "INTEGER", nullable: true),
                    first_name = table.Column<string>(type: "TEXT", nullable: false),
                    surname = table.Column<string>(type: "TEXT", nullable: false),
                    gender = table.Column<bool>(type: "INTEGER", nullable: false),
                    faction_id = table.Column<int>(type: "INTEGER", nullable: true),
                    faction = table.Column<string>(type: "TEXT", nullable: true),
                    party_name = table.Column<string>(type: "TEXT", nullable: true),
                    dob = table.Column<DateOnly>(type: "TEXT", nullable: true),
                    cob = table.Column<string>(type: "TEXT", nullable: true),
                    yod = table.Column<int>(type: "INTEGER", nullable: true),
                    yoi = table.Column<int>(type: "INTEGER", nullable: true),
                    city = table.Column<string>(type: "TEXT", nullable: true),
                    languages = table.Column<string>(type: "TEXT", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_people", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "topic_extras",
                columns: table => new
                {
                    id = table.Column<int>(type: "INTEGER", nullable: false)
                        .Annotation("Sqlite:Autoincrement", true),
                    topic_extra = table.Column<string>(type: "TEXT", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_topic_extras", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "topics",
                columns: table => new
                {
                    id = table.Column<int>(type: "INTEGER", nullable: false)
                        .Annotation("Sqlite:Autoincrement", true),
                    topic = table.Column<string>(type: "TEXT", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_topics", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "knesset_speeches",
                columns: table => new
                {
                    id = table.Column<int>(type: "INTEGER", nullable: false),
                    text = table.Column<string>(type: "TEXT", nullable: true),
                    uuid = table.Column<Guid>(type: "TEXT", nullable: false),
                    knesset = table.Column<int>(type: "INTEGER", nullable: false),
                    session_number = table.Column<long>(type: "INTEGER", nullable: true),
                    date = table.Column<DateOnly>(type: "TEXT", nullable: false),
                    person_id = table.Column<int>(type: "INTEGER", nullable: true),
                    name_id = table.Column<int>(type: "INTEGER", nullable: true),
                    chair = table.Column<bool>(type: "INTEGER", nullable: false),
                    topic_id = table.Column<int>(type: "INTEGER", nullable: true),
                    topic_extra_id = table.Column<int>(type: "INTEGER", nullable: true),
                    qa = table.Column<bool>(type: "INTEGER", nullable: true),
                    query = table.Column<string>(type: "TEXT", nullable: true),
                    only_read = table.Column<bool>(type: "INTEGER", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_knesset_speeches", x => x.id);
                    table.ForeignKey(
                        name: "FK_knesset_speeches_names_name_id",
                        column: x => x.name_id,
                        principalTable: "names",
                        principalColumn: "id");
                    table.ForeignKey(
                        name: "FK_knesset_speeches_topic_extras_topic_extra_id",
                        column: x => x.topic_extra_id,
                        principalTable: "topic_extras",
                        principalColumn: "id");
                    table.ForeignKey(
                        name: "FK_knesset_speeches_topics_topic_id",
                        column: x => x.topic_id,
                        principalTable: "topics",
                        principalColumn: "id");
                });

            migrationBuilder.CreateIndex(
                name: "IX_knesset_speeches_name_id",
                table: "knesset_speeches",
                column: "name_id");

            migrationBuilder.CreateIndex(
                name: "IX_knesset_speeches_topic_extra_id",
                table: "knesset_speeches",
                column: "topic_extra_id");

            migrationBuilder.CreateIndex(
                name: "IX_knesset_speeches_topic_id",
                table: "knesset_speeches",
                column: "topic_id");

            migrationBuilder.CreateIndex(
                name: "IX_names_name",
                table: "names",
                column: "name",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_topic_extras_topic_extra",
                table: "topic_extras",
                column: "topic_extra",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_topics_topic",
                table: "topics",
                column: "topic",
                unique: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "knesset_speeches");

            migrationBuilder.DropTable(
                name: "people");

            migrationBuilder.DropTable(
                name: "names");

            migrationBuilder.DropTable(
                name: "topic_extras");

            migrationBuilder.DropTable(
                name: "topics");
        }
    }
}
