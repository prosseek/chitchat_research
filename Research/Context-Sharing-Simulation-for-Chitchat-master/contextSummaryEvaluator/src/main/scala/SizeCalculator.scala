package smcho

import java.io.{PrintWriter, File}
import scala.sys.process._

import net.liftweb.json.DefaultFormats
import net.liftweb.json._

import core.{CompleteSummary, BloomierFilterSummary, LabeledSummary}

/**
 * Created by smcho on 9/16/15.
 */
class SizeCalculator(val filePath:String, val size:Int = 11, maxValue:Int = 210) {

  val baseDirectory = getBaseDir(filePath)

  def getBaseDir(filePath:String) = {
    var p = new java.io.File(filePath).getCanonicalPath()
    if (!p.endsWith(File.separator)) p += File.separator
    val sp = p.split(File.separator)
    sp.dropRight(1).mkString(File.separator) + File.separator
  }

  def getCompletSize() = {
    val cl = CompleteSummary(filePath)
    cl.getSize()
  }

  def getJsonSize() = {
    val lb = LabeledSummary(filePath)
    val sizes = lb.getSizes()
    Array(lb.getJsonSize(), lb.getJsonCompressedSize())
  }

  def getLabeledSize() = {
    val lb = LabeledSummary(filePath)
    val sizes = lb.getSizes()
    Array(sizes._2, sizes._3)
  }

  def getBfSize(width:Int, complete:Boolean) = {
    val bf = BloomierFilterSummary(filePath)
    bf.setup(m = 0, k = 3, q = 8*width, complete = complete)
    bf.getSize()
  }

  def getResultInJson(jsonFilePath:String) = {

    def iterableToJsonList(i:Iterable[Int]) = {
      val sb = ("[" /: i) { (acc, value) =>
        acc + value.toString + ","
      }
      sb.dropRight(1) + "]"
    }

    val complete = getCompletSize()
    val label = getLabeledSize()
    val json = getJsonSize()

    val bf = new Array[Int](size)
    val bf_complete = new Array[Int](size) // ignore index 0, make it start from 1
    1.until(size+1) foreach {i =>
      bf_complete(i-1) = getBfSize(i, true)
    }
    1.until(size+1) foreach {i =>
      bf(i-1) = getBfSize(i, false)
    }

    val jsonString = s"""{"c":${complete}, "l":${iterableToJsonList(label)}, "j":${iterableToJsonList(json)}, "fbf":${iterableToJsonList(bf)}, "cbf":${iterableToJsonList(bf_complete)}}"""
    val pw = new PrintWriter(new File(jsonFilePath))
    pw.write(jsonString)
    pw.close()
    jsonString
  }

  def getDataFromJsonString(jsonString: String, dataFilePath:String) = {
    case class Results(c: Int, l:List[Int], j:List[Int], fbf:List[Int], cbf:List[Int])
    implicit val formats = DefaultFormats

    val p = parse(jsonString)
    val r = p.values.asInstanceOf[Map[String, List[Int]]]

    val size = r("fbf").size

    val c = Array.fill[Int](size)(r("c").asInstanceOf[BigInt].toInt)
    val fbf = r("fbf")
    val cbf = r("cbf")
    val l = Array.fill[Int](size)(r("l")(0).asInstanceOf[BigInt].toInt)
    val l_compressed = Array.fill[Int](size)(r("l")(1).asInstanceOf[BigInt].toInt)
    val j = Array.fill[Int](size)(r("j")(0).asInstanceOf[BigInt].toInt)
    val j_compressed = Array.fill[Int](size)(r("j")(1).asInstanceOf[BigInt].toInt)

    val sb = new StringBuffer()
    for (i <- 0.until(size)) {
      val column = (i + 1)
      val buffer = s"${column} ${c(i)} ${fbf(i)} ${cbf(i)} ${l(i)} ${l_compressed(i)} ${j(i)} ${j_compressed(i)}\n"
      sb.append(buffer)
    }
    val result = sb.toString

    val pw = new PrintWriter(new File(dataFilePath))
    pw.write(result)
    pw.close()

    result
  }

  def getGnuplotScript(gnuFilePath:String, pngName:String, noKey:Boolean=true) = {
    val template =
      s"""
        |set terminal pngcairo dashed font 'DroidSerif'
        |set output "%s.png"
        |
        |set lmargin 8
        |set xrange [1:%d]
        |set yrange [0:%d]
        |set xtics font ", 15"
        |set ytics font ", 15"
        |set key font ",12"
        |set key top left box
        |set xlabel "Data width in bytes" font ",20"
        |set ylabel "Summary size in bytes" font ",20" offset 1,0
        |%s
        |
        |set style line 1 lw 3 lc rgb '#000000' ps 1.5 pt 3 pi 1
        |set style line 2 lw 3 lc rgb '#000000' ps 2   pt 6
        |set style line 3 lw 3 lc rgb '#000000' ps 2   pt 7
        |set style line 4 lw 3 lc rgb '#000000' ps 1.5 pt 1 pi 5
        |set style line 5 lw 3 lc rgb '#000000' ps 1.5 pt 4 pi 5
        |set style line 6 lw 3 lc rgb '#000000' ps 1.5 pt 8 pi 5
        |set style line 7 lw 3 lc rgb '#000000' ps 1.5 pt 9 pi 5
        |
        |plot "data.txt"  using 1:2  title "Complete"               ls 1 , \\
        |""                    using 1:3  title "FBF"               ls 2 w lp , \\
        |""                    using 1:4  title "CBF"               ls 3 w lp ,  \\
        |""                    using 1:5  title "Labeled"           ls 4 , \\
        |""                    using 1:6  title "Labeled (zipped)"  ls 5 , \\
        |""                    using 1:7  title "Json"              ls 6 , \\
        |""                    using 1:8  title "Json (zipped)"     ls 7
      """.stripMargin

    val result = template.format(pngName, size, maxValue, if (noKey) "set nokey" else "")

    var pw = new PrintWriter(new File(gnuFilePath))
    pw.write(result)
    pw.close()

    val runMeScript =
      s"""
        |p=`pwd`
        |cd ${baseDirectory}
        |/usr/local/bin/gnuplot gnuplot.txt
        |cd $$p
      """.stripMargin

    pw = new PrintWriter(new File(baseDirectory + "/runme.sh"))
    pw.write(runMeScript)
    pw.close()
  }

  def runGnuScript(baseDirectory:String) = {
    var cmd = s"""sh $baseDirectory/runme.sh"""
    println(cmd)
    cmd !
  }
}
