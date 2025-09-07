namespace israpolitics;

public static class Helpers
{
    public static async IAsyncEnumerable<string> GetLinesAsync(this Stream stream)
    {
        using var reader = new StreamReader(stream);
        string? line;
        while ((line = await reader.ReadLineAsync()) != null)
        {
            yield return line;
        }
    }

    public static string Join<T>(this IEnumerable<T> source, string separator = ", ")
    {
        if (source == null || !source.Any())
            return string.Empty;
        return string.Join(separator, source);
    }
    public static string Reverse(this string str)
    {
        if (string.IsNullOrEmpty(str))
            return str;
        return string.Concat(Enumerable.Reverse(str));
    }

    public static async IAsyncEnumerable<TResult> SelectAsync<TSource, TResult>(
        this IAsyncEnumerable<TSource> source,
        Func<TSource, Task<TResult>> selector)
    {
        ArgumentNullException.ThrowIfNull(source);
        ArgumentNullException.ThrowIfNull(selector);
        await foreach (var item in source)
            yield return await selector(item);
    }

    public static IEnumerable<T> WhereNotNull<T>(this IEnumerable<T?> source) where T : struct
    {
        return source.Where(item => item is not null).Select(item => item!.Value);
    }
    public static IEnumerable<T> WhereNotNull<T>(this IEnumerable<T?> source) where T : class
    {
        return source.Where(item => item is not null).Select(item => item!);
    }
}
