using System.Text;

namespace IsraPolitics;
public class Encodings
{
    public Encoding UTF8 { get; } = Encoding.UTF8;
    public Encoding Windows1255 { get; } = CodePagesEncodingProvider.Instance.GetEncoding(1255)!;
}
