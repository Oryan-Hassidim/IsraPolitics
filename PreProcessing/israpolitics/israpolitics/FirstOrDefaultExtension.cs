using Microsoft.EntityFrameworkCore;
using System.Linq.Expressions;

public static class FirstOrDefaultExtension
{
    public static T FirstOrDefault<T>(
        this DbSet<T> dbSet,
        Expression<Func<T, bool>> predicate,
        T defaultValue)
        where T : class
    {
        return dbSet.FirstOrDefault(predicate) ?? defaultValue;
    }
}