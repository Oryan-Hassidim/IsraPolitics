namespace CliArgsAttributes;

[AttributeUsage(AttributeTargets.Method)]
public class CliCommandAttribute(string name = "") : Attribute
{
    public string Name { get; } = name;
}

[AttributeUsage(AttributeTargets.Parameter)]
public class CliOptionAttribute(string name = "") : Attribute
{
    public string Name { get; } = name;
    public string[] Aliases { get; set; } = [];
}