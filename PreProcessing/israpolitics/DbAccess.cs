using israpolitics.Model.KnessetSpeeches;
using Microsoft.EntityFrameworkCore;
using System.Threading.Tasks;

namespace israpolitics;

public static class DbAccess
{
    public static Task<IGrouping<int?,Person>[]> GetMksAsync(string name)
    {
        using var context = new Context();
        return context.People
            .Where(p =>
                name.Split(" ", StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
                .All(w => p.FirstName.Contains(w) || p.Surname.Contains(w)))
            .GroupBy(p => p.PersonId)
            .ToArrayAsync();
    }
}
