import scala.io.Source
import net.liftweb.json._

// Map(
// j -> List(174, 129),
// cbf -> List(252, 125, 113, 115, 114, 112, 115, 114, 118, 117, 114),
// l -> List(141, 121),
// fbf -> List(98, 93, 95, 96, 98, 99, 107, 106, 110, 112, 112),
// c -> 89)



/**
 * Created by smcho on 9/17/15.
 */
class SizeComparator(val filePath:String, val q:Int = -1, jsonCompressed:Boolean = false) {

  val powerMapFbf16 = Map(
    "s1" -> 7.32 ,
    "s2" -> 6.41 ,
    "s3" -> 17.85,
    "s4" -> 9.07 ,
    "s5" -> 20.63,
    "s6" -> 16.94,
    "c1" -> 21.31,
    "c2" -> 0.37)

  val powerMapFbf64 = Map(
    "s1" -> 0.35,
    "s2" -> 0.98,
    "s3" -> 1.05,
    "s4" -> 0.33,
    "s5" -> 1.33,
    "s6" -> 1.69,
    "c1" -> 1.25,
    "c2" -> 0.36)

  implicit val formats = DefaultFormats

  val source = Source.fromFile(filePath).mkString("")
  val res = parse(source)
  val json = res.values.asInstanceOf[Map[String, Any]]

  implicit def bigInt2Int(i: BigInt): Int = i.toInt

  def getName() = {
    // contextSummaryEvaluator/resources/jsonContexts/c1//results.json
    filePath.split("/").takeRight(3)(0)
  }

  def getFbfSize(width:Int) = {
    json("fbf").asInstanceOf[List[BigInt]](width-1).toInt
  }

  def getCompleteSize() = {
    json("c").asInstanceOf[BigInt].toInt
  }
  def getJsonSize(jsonCompressed:Boolean) = {
    val j = json("j").asInstanceOf[List[BigInt]]
    if (jsonCompressed) j(1) else j(0)
  }
  def getMinFbf() = {
    val fbf = json("fbf").asInstanceOf[List[BigInt]]
    (Int.MaxValue /: fbf) { (acc, value) => if (acc < value) acc else value}
  }
  def getMinCbf() = {
    val cbf = json("cbf").asInstanceOf[List[BigInt]]
    (Int.MaxValue /: cbf) { (acc, value) => if (acc < value) acc else value}
  }
  def getReductionRateFbfFromJson(jsonCompressed:Boolean, q:Int = q) = {
    val minFbf = if (q == -1) getMinFbf() else getFbfSize(q);
    val json = getJsonSize(jsonCompressed)
    (1.0 - minFbf.toDouble/json.toDouble)*100.0
  }
  def getReductionRateCbfFromJson(jsonCompressed:Boolean) = {
    val minFbf = getMinCbf();
    val json = getJsonSize(jsonCompressed)
    (1.0 - minFbf.toDouble/json.toDouble)*100.0
  }
  def getIncreaseRateFbfFromComplete() = {
    val minFbf = getMinFbf();
    val complete = getCompleteSize()
    (minFbf.toDouble/complete.toDouble - 1.0)*100.0
  }
  def getIncreaseRateCbfFromComplete() = {
    val minFbf = getMinCbf();
    val complete = getCompleteSize()
    (minFbf.toDouble/complete.toDouble - 1.0)*100.0
  }
  def getColumnData(jsonCompressed:Boolean) = {
    (getReductionRateFbfFromJson(jsonCompressed),
     getReductionRateCbfFromJson(jsonCompressed),
     getIncreaseRateFbfFromComplete(),
     getIncreaseRateCbfFromComplete())
  }
  def getColumnFormat(jsonCompressed:Boolean) = {
    // s3 & 32.74 & 18.58 && 4.11 & 26.03 \\
    val values = getColumnData(jsonCompressed)
    "%s & %5.2f & %5.2f && %5.2f & %5.2f \\\\ \n".format(getName(),
      values._1, values._2, values._3, values._4)
  }
  def getSizeConsumptionFormat(jsonCompressed:Boolean) = {
    val power16 = powerMapFbf16(getName())
    val power64 = powerMapFbf64(getName())
    val size = getJsonSize(jsonCompressed)
    val rrFbf16 = getReductionRateFbfFromJson(jsonCompressed, 2) // 2 => 2*8 = 16
    val rrFbf64 = getReductionRateFbfFromJson(jsonCompressed, 8) // 8 => 8*8 = 64
    "%s & %d && %5.2f & %5.2f && %5.2f & %5.2f \\\\ \n".format(getName(),
      size, rrFbf16, power16, rrFbf64, power64)
  }
}
