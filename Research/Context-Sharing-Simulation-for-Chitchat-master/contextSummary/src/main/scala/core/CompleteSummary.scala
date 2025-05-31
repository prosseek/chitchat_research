package core

import grapevineType.BottomType._
import util.compression.CompressorHelper._
import util.conversion.ByteArrayTool._
import util.conversion.BitSetTool._
import util.conversion.Util

import scala.collection.mutable

object CompleteSummary {
  def apply(t: Map[String, Any]) : CompleteSummary =
    new CompleteSummary(t, 0, 0)
  def apply(t: (Map[String, Any], Int, Int)) : CompleteSummary  = new CompleteSummary(t._1, t._2, t._3)
  def apply(filePath:String) : CompleteSummary = CompleteSummary(ContextSummary.loadJsonAll(filePath))
}

/**
 * Created by smcho on 1/5/15.
 */
case class CompleteSummary(jsonMap: Map[String, Any],
                      jsonSize:Int = 0,
                      jsonCompressedSize:Int = 0) extends GrapevineSummary(jsonMap, jsonSize, jsonCompressedSize) {

  override def repr(): String = {
    s"""{"type":"c", "size":${getSize()}, "jsonSize":${getJsonSize()}, "jsonCompSize":${getJsonCompressedSize()}}"""
  }
//  def maxBits(size:Int) = {
//    math.ceil(log2(size)).toInt
//  }
//
  def log2(x : Double) = {
    math.log10(x)/math.log10(2.0)
  }

  // This should be the bit size, not byte
  override def getTheorySize(): Int = {
    val size1 = (0 /: map) { (acc, value) => acc + value._2.getSize }
    //val size2 = Util.getByteSizeFromSize(math.ceil(dataStructure.size * log2(dataStructure.size.toDouble)).toInt)
    val size2 = Util.getByteSizeFromSize(map.size)
    //val size2 = math.ceil(dataStructure.size * log2(dataStructure.size.toDouble)).toInt
    size1 + size2
  }

  override def getSizes() = {
    val serial = serialize()
    val compressed = compress(serial)

    (getTheorySize(), serial.size, compressed.size)
  }

  /* It should not be accessed from the key, but the index */

  override def get(key: String): Any = {
    if (getMap().contains(key)) getMap().get(key).get
    else None
  }

//  def check(key: String): BottomType = {
//    if (getValue(key).isEmpty) Bottom // this is structural check to return Buttom
//    else NoError
//  }

  override def serialize(): Array[Byte] = {

    val size = map.size
    val sizeByteArray = shortToByteArray(size.toShort)

    val bitsForSize = math.ceil(log2(size.toDouble)).toInt
    var ab = Array[Byte]()
    // get the contents
    var bitSet = mutable.BitSet()

    map.zipWithIndex.foreach { case (ds, index) =>
      val bs = intToBitSet(index, shift = index * bitsForSize)
      bitSet ++= bs
      val value = ds._2
      val byteArrayValue = value.toByteArray()
      ab ++= byteArrayValue
    }
    val goalBitSetSize = Util.getByteSizeFromSize(map.size)
    return sizeByteArray ++ bitSetToByteArray(bitSet, goalBitSetSize) ++ ab
  }

  override def getSize(): Int = serialize().size
}