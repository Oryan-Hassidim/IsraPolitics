using Newtonsoft.Json;
using System.Text;

namespace IsraPolitics;

public static class ChangeEncoding
{
    public static string AddOutputToFileName(string filePath)
    {
        string directory = Path.GetDirectoryName(filePath)!;
        string fileNameWithoutExtension = Path.GetFileNameWithoutExtension(filePath);
        string extension = Path.GetExtension(filePath);
        string newFileName = $"{fileNameWithoutExtension}_output{extension}";
        string newFilePath = Path.Combine(directory, newFileName);
        return newFilePath;
    }

    public static void ChangeEncodingJson(string inputPath)
    {
        string outputPath = AddOutputToFileName(inputPath);

        using var inputFileStream = File.OpenRead(inputPath);
        using var streamReader = new StreamReader(inputFileStream);
        using var reader = new JsonTextReader(streamReader);

        var encoding = CodePagesEncodingProvider.Instance.GetEncoding(1255)!;
        using var outputFileStream = File.OpenWrite(outputPath);
        using var streamWriter = new StreamWriter(outputFileStream, encoding);
        using var writer = new JsonTextWriter(streamWriter);

        long i = 0, p1, p2;
        while (reader.Read())
        {
            writer.WriteToken(reader.TokenType, reader.Value);
            if (i++ % 10000 == 0)
            {
                p1 = inputFileStream.Position;
                p2 = outputFileStream.Position;
                Console.WriteLine($"inputFileStream.Position: {p1}");
                Console.WriteLine($"outputFileStream.Position: {p2}");
            }
        }

        p1 = inputFileStream.Position;
        p2 = outputFileStream.Position;
        Console.WriteLine($"inputFileStream.Position: {p1}");
        Console.WriteLine($"outputFileStream.Position: {p2}");
        Console.WriteLine($"Ratio: {((double)p2) / p1}");

        writer.Flush();
        writer.Close();
        streamWriter.Close();
        outputFileStream.Close();

        reader.Close();
        streamReader.Close();
        inputFileStream.Close();
    }

    public static void ChangeEncodingCsv(string inputPath)
    {
        string outputPath = AddOutputToFileName(inputPath);

        using var inputFileStream = File.OpenRead(inputPath);
        using var reader = new StreamReader(inputFileStream);

        var encoding = CodePagesEncodingProvider.Instance.GetEncoding(1255)!;
        using var outputFileStream = File.OpenWrite(outputPath);
        using var writer = new StreamWriter(outputFileStream, encoding);

        long i = 0;
        while (!reader.EndOfStream)
        {
            writer.WriteLine(reader.ReadLine());
            if (++i % 100_000 == 0)
                Console.WriteLine(i);
        }

        var p1 = inputFileStream.Position;
        var p2 = outputFileStream.Position;
        Console.WriteLine($"inputFileStream.Position: {p1}");
        Console.WriteLine($"outputFileStream.Position: {p2}");
        Console.WriteLine($"Ratio: {((double)p2) / p1}");

        writer.Flush();
        writer.Close();
        outputFileStream.Close();

        reader.Close();
        inputFileStream.Close();
    }
}