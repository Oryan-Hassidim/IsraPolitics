namespace israpolitics;

public class Paths
{
    private static string? _repositoryRoot;
    public static string RepositoryRoot
    {
        get => _repositoryRoot ??=
        Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "..", "..", "..", ".."));
    }

    public static string DataDirectory => Path.Combine(RepositoryRoot, "Data");
    public static string JobsDirectory => Path.Combine(RepositoryRoot, "Jobs");
    public static string PromptsDirectory => Path.Combine(RepositoryRoot, "Prompts");
    public static string ClientDirectory => Path.Combine(RepositoryRoot, "Client");
    public static string ClientDataDirectory => Path.Combine(ClientDirectory, "client_data");
}
