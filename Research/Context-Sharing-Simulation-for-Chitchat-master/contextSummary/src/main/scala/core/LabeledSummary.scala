package core

import grapevineType.BottomType._
import grapevineType.GrapevineType
import util.conversion.Util
import util.conversion.ByteArrayTool._
import util.compression.CompressorHelper._
/**
 * Created by smcho on 8/10/14.
 */

object LabeledSummary {
  def apply(t: Map[String, Any]) : LabeledSummary =
    new LabeledSummary(t, 0, 0)
  def apply(t: (Map[String, Any], Int, Int)) : LabeledSummary  = new LabeledSummary(t._1, t._2, t._3)
  def apply(filePath:String) : LabeledSummary = LabeledSummary(ContextSummary.loadJsonAll(filePath))
}

case class LabeledSummary(jsonMap: Map[String, Any],
                     jsonSize:Int,
                     jsonCompressedSize:Int) extends GrapevineSummary(jsonMap, jsonSize, jsonCompressedSize) {



//  def getCompleteSize(): Int = {
//    def log2(x : Double) = {
//      math.log10(x)/math.log10(2.0)
//    }
//    val size1 = (0 /: dataStructure) { (acc, value) => acc + value._2.getSize }
//    val size2 = Util.getByteSizeFromSize(math.ceil(dataStructure.size * log2(dataStructure.size.toDouble)).toInt)
//    size1 + size2
//  }

  override def repr(): String = {
    s"""{"type":"l", "size":${getSize()}, "jsonSize":${getJsonSize()}, "jsonCompSize":${getJsonCompressedSize()}}"""
  }
}