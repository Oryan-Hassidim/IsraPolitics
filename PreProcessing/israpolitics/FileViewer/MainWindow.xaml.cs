using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.IO;
using System;
using System.Buffers;

namespace FileViewer
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        const int VIEW_CHARACTERS = 10_000;

        public MainWindow()
        {
            InitializeComponent();
        }

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            FileNameTextBox.Text = @"C:\Projects\Oryan-Hassidim\IsraPolitics\Data\knesset_speeches.csv";
        }

        //private FileStream? _fileStream;
        private StreamReader? _reader;
        private Encoding _encoding = Encoding.UTF8; // CodePagesEncodingProvider.Instance.GetEncoding(1255)!;
        private char[] _buffer = new char[VIEW_CHARACTERS];

        private void FileNameTextBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (_reader != null)
            {
                _reader.Close();
                _reader.Dispose();
                _reader = null;
            }
            if (File.Exists(FileNameTextBox.Text))
            {
                _reader = new StreamReader(FileNameTextBox.Text, _encoding);
                Slider.Maximum = _reader.BaseStream.Length;
                Slider.Value = 0;
                UpdateContent();
            }
            else
            {
                Slider.Maximum = 0;
                Slider.Value = 0;
                UpdateContent();
            }
        }

        SearchValues<char> _lineSeperators = SearchValues.Create("\r\n");

        private void UpdateContent()
        {
            Document.Blocks.Clear();
            if (_reader == null) return;
            _reader.BaseStream.Seek((long)Slider.Value, SeekOrigin.Begin);
            int read = _reader.Read(_buffer, 0, VIEW_CHARACTERS);
            ReadOnlySpan<char> span = _buffer.AsSpan(0, read);
            foreach (var range in span.SplitAny(_lineSeperators))
            {
                if (range.End.Value - range.Start.Value < 2) continue;
                var paragraph = new Paragraph(new Run(span[range].ToString()));
                Document.Blocks.Add(paragraph);
            }
        }
        // 1716097218
        private void Slider_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            UpdateContent();
        }
    }
}