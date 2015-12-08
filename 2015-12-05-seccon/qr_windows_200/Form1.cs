using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Imaging;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using ZXing;

namespace QrSolver
{
    enum EdgeType
    {
        Left = 0,
        Top = 1,
        Right = 2,
        Bottom = 3
    }

    class EdgeTemplate
    {
        public EdgeType Type { get; private set; }
        public Point[] Points { get; private set; }
        public int Width { get; private set; }
        public int Height { get; private set; }

        public EdgeTemplate(EdgeType type, int width, int height)
        {
            Type = type;
            Width = width;
            Height = height;
            Points = GetPoints(type, width, height);
        }

        private Point[] GetPoints(EdgeType type, int width, int height)
        {
            switch (type)
            {
                case EdgeType.Left: return Sweep(0, 0, 0, 1, height);
                case EdgeType.Top: return Sweep(0, 0, 1, 0, width);
                case EdgeType.Right: return Sweep(width - 1, 0, 0, 1, height);
                case EdgeType.Bottom: return Sweep(0, height - 1, 1, 0, width);
                default: throw new InvalidOperationException();
            }
        }

        private Point[] Sweep(int sx, int sy, int dx, int dy, int size)
        {
            return Enumerable.Range(0, size)
                .Select(i => new Point(sx + dx * i, sy + dy * i))
                .ToArray();
        }
    }

    class Edge
    {
        private Edge() { }

        public Bitmap Source { get; private set; }
        public Color[] Data { get; private set; }
        public EdgeType Type { get; private set; }

        public Edge(Bitmap bitmap, EdgeTemplate template)
        {
            Source = bitmap;
            Type = template.Type;
            Data = template.Points.Select(x => bitmap.GetPixel(x.X, x.Y)).ToArray();
        }

        public static EdgeType Opposite(EdgeType type)
        {
            return (EdgeType)(((int)type + 2) % 4);
        }

        private static bool Matches(EdgeType fst, EdgeType snd)
        {
            return fst == Opposite(snd);
        }

        private static bool Matches(Color[] fst, Color[] snd)
        {
            return Enumerable.Zip(fst, snd, (a, b) => a.Equals(b)).All(x => x);
        }

        public static Point ToDirection(EdgeType type)
        {
            switch (type)
            {
                case EdgeType.Top: return new Point(0, -1);
                case EdgeType.Bottom: return new Point(0, 1);
                case EdgeType.Left: return new Point(-1, 0);
                case EdgeType.Right: return new Point(1, 0);
                default: throw new InvalidOperationException();
            }
        }

        public bool Matches(Edge other)
        {
            return Source != other.Source && Matches(this.Type, other.Type) && Matches(this.Data, other.Data);
        }
    }

    class EdgeCollection
    {
        public List<Edge> Edges { get; set; }

        public EdgeCollection(List<Edge> edges)
        {
            this.Edges = edges;
        }

        public void RemoveBySource(Bitmap bmp)
        {
            Edges = Edges.Where(x => x.Source != bmp).ToList();
        }
    }

    static class Bundle
    {
        public static Bitmap Reconstruct(List<Bitmap> bitmaps, int size)
        {
            for (int i = 0; i < bitmaps.Count; i++)
            {
                var result = ReconstructFromExample(i, bitmaps, size);
                if (result.Cast<Bitmap>().Count(x => x != null) == bitmaps.Count)
                {
                    return MergeResult(result, bitmaps[0].Width, bitmaps[0].Height, size);
                }
            }
            return null;
        }

        public static Bitmap[,] ReconstructFromExample(int ndx, List<Bitmap> bitmaps, int size)
        {
            var example = bitmaps[ndx];
            var width = example.Width;
            var height = example.Height;
            var edgeTypes = Enum.GetValues(typeof(EdgeType)).Cast<EdgeType>();
            var templates = edgeTypes.Select(x => new EdgeTemplate(x, width, height)).ToList();
            var edges = bitmaps.SelectMany(bmp => templates.Select(tmpl => new Edge(bmp, tmpl)))
                .Where(GoodEdge)
                .ToList();

            var result = new Bitmap[size * 2 + 3, size * 2 + 3];
            var edgeCol = new EdgeCollection(edges);
            result[size + 1, size + 1] = example;
            ReconstructFrom(result, templates, size + 1, size + 1, edgeCol);
            return result;
        }

        private static void ReconstructFrom(Bitmap[,] result, List<EdgeTemplate> templates, int x, int y, EdgeCollection edges)
        {
            var current = result[x, y];
            edges.RemoveBySource(current);

            while (TryReconstructFrom(result, templates, x, y, edges)) ;
        }

        private static bool TryReconstructFrom(Bitmap[,] result, List<EdgeTemplate> templates, int x, int y, EdgeCollection edges)
        {
            var current = result[x, y];
            var currentEdges = templates.Select(tmpl => new Edge(current, tmpl));
            foreach (var edge in edges.Edges)
            {
                foreach (var curr in currentEdges)
                {
                    var dir = Edge.ToDirection(curr.Type);
                    var x2 = x + dir.X;
                    var y2 = y + dir.Y;
                    if (result[x2, y2] == null && curr.Matches(edge) && MatchesInPosition(result, templates, edge.Source, x2, y2))
                    {
                        result[x2, y2] = edge.Source;
                        ReconstructFrom(result, templates, x2, y2, edges);
                        return true;
                    }
                }
            }
            return false;
        }

        private static bool MatchesInPosition(Bitmap[,] result, List<EdgeTemplate> templates, Bitmap newBmp, int x, int y)
        {
            foreach (var template in templates)
            {
                var dir = Edge.ToDirection(template.Type);
                var x2 = dir.X + x;
                var y2 = dir.Y + y;
                if (result[x2, y2] != null)
                {
                    var reverseTemplate = new EdgeTemplate(Edge.Opposite(template.Type), template.Width, template.Height);
                    var edge = new Edge(newBmp, template);
                    var reverseEdge = new Edge(result[x2, y2], reverseTemplate);
                    if (!reverseEdge.Matches(edge)) { return false; }
                }
            }
            return true;
        }

        private static bool GoodEdge(Edge edg)
        {
            return edg.Data.Any(x => x.R < 10 && x.G < 10 && x.B < 10);
        }

        private static Bitmap MergeResult(Bitmap[,] results, int sx, int sy, int n)
        {
            var ix = results.GetLength(0);
            var iy = results.GetLength(1);

            int stx = 9999;
            int sty = 9999;

            for (int x = 0; x < ix; x++)
            {
                for (int y = 0; y < iy; y++)
                {
                    if (results[x, y] != null)
                    {
                        stx = Math.Min(x, stx);
                        sty = Math.Min(y, sty);
                    }
                }
            }

            var result = new Bitmap(n * sx, n * sy);
            using (var g = Graphics.FromImage(result))
            {
                for (int x = 0; x < n; x++)
                {
                    for (int y = 0; y < n; y++)
                    {
                        g.DrawImage(results[stx + x, sty + y], x * sx, y * sy);
                    }
                }
            }
            return result;
        }
    }

    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        public Bitmap CaptureApplication(string procName)
        {
            var proc = Process.GetProcessesByName(procName)[0];
            var rect = new User32.Rect();
            User32.GetWindowRect(proc.MainWindowHandle, ref rect);

            var width = rect.right - rect.left;
            var height = rect.bottom - rect.top;

            var bmp = new Bitmap(width, height, PixelFormat.Format32bppArgb);
            using (Graphics graphics = Graphics.FromImage(bmp))
            {
                graphics.CopyFromScreen(rect.left, rect.top, 0, 0, new Size(width, height), CopyPixelOperation.SourceCopy);
            }

            return bmp;
        }

        private class User32
        {
            [StructLayout(LayoutKind.Sequential)]
            public struct Rect
            {
                public int left;
                public int top;
                public int right;
                public int bottom;
            }

            [DllImport("user32.dll")]
            public static extern IntPtr GetWindowRect(IntPtr hWnd, ref Rect rect);
        }

        private List<Bitmap> Split(
            int sx, int sy, // start of first chunk
            int wx, int wy, // size of each chunk
            int mx, int my, // margin for each chunk
            int n, // number of chunks vertical/horizontal
            Bitmap data) // data to be split
        {
            var results = new List<Bitmap>();
            for (int x = 0; x < n; x++)
            {
                for (int y = 0; y < n; y++)
                {
                    var next = new Bitmap(wx, wy);
                    using (var g = Graphics.FromImage(next))
                    {
                        g.DrawImage(data, 0, 0, new Rectangle(sx + x * (wx + mx), sy + y * (wy + my), wx, wy), GraphicsUnit.Pixel);
                    }
                    next.Save("test" + x.ToString() + y.ToString() + ".bmp");

                    results.Add(next);
                }
            }

            return results;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Thread.Sleep(3000);

            while (true)
            {
                using (var bmp = CaptureApplication("QRpuzzle"))
                {
                    var chunks = Split(
                        18, 77,
                        160, 167,
                        6, 13,
                        3,
                        bmp);
                    var result = Bundle.Reconstruct(chunks, 3);

                    IBarcodeReader reader = new BarcodeReader { PossibleFormats = new[] { BarcodeFormat.QR_CODE }, TryHarder = true };

                    result.Save("Test2.png");
                    var code = reader.Decode(result);

                    SendKeys.Send(code.Text);
                    Thread.Sleep(500);
                }
            }
        }
    }
}
