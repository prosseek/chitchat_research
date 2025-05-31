package core

import grapevineType._
import util.compression.CompressorHelper._
import util.conversion.ByteArrayTool._
import util.conversion.{ByteArrayTool, Splitter}
import util.io.File
import java.io._

import scala.collection.mutable.{Map => MMap}
/**
 * Created by smcho on 8/10/14.
 */

object GrapevineSummary {
  def apply(t: Map[String, Any]) : GrapevineSummary =
    new GrapevineSummary(t, 0, 0)
  def apply(t: (Map[String, Any], Int, Int)) : GrapevineSummary  = new GrapevineSummary(t._1, t._2, t._3)
  def apply(filePath:String) : GrapevineSummary = GrapevineSummary(ContextSummary.loadJsonAll(filePath))
}


/**
 * create the GrapeVineSummary, and the map is already setup with GrapevineType
 * @param jsonMap
 * @param jsonSize
 * @param jsonCompressedSize
 */
class GrapevineSummary(jsonMap: Map[String, Any],
                                jsonSize:Int,
                                jsonCompressedSize:Int) extends ContextSummary(jsonMap, jsonSize, jsonCompressedSize) {
  var map : MMap[String, GrapevineType] = _
  setup(jsonMap)

  // this is the size in bytes
  def getTheorySize(): Int = {
    (0 /: map) { (acc, value) => acc + value._2.getSize } + // sum value size
    (0 /: map.keys) {(acc, value) => acc + value.length}     // sum of keys
    // dataStructure.size     // 1 byte is used for identifying the type
  }

  override def serialize(): Array[Byte] = {
    var ab = Array[Byte]()
    // get the contents

    // KEY_STRING + 0 + SIZE_OF_BYTES + VALUE_AS_BYTE_ARRAY
    map.foreach { case (key, value) =>
      val byteArrayValue = value.toByteArray()
      val id = value.getId()
      ab ++= (stringToByteArray(key) ++ Array[Byte](id.toByte) ++ byteArrayValue)
    }
    ab
  }

  override def getSizes() = {
    val serial = serialize()
    val compressed = compress(serial)

    (getTheorySize(), serial.length, compressed.length)
  }

  override def getSize() = serialize().length // getTheorySize()

  def set(key:String, t:Class[_], v:Any):Unit = {
    val gv = t.newInstance.asInstanceOf[GrapevineType]
    gv.set(v)
    map(key) = gv
  }

  def set(key:String, v:GrapevineType):Unit = {
    map(key) = v
  }

  def contains(key:String) = {
    map.contains(key)
  }

  override def get(key:String) : Any = {
    getValue(key) match {
      case Some(p) => p
      case None => null
    }
  }

  def getValue(key:String) : Option[Any] = {
    if (map.contains(key)) Some(map(key).get)
    else None
  }

  def getMap() = {
    map.toMap
  }

  /**
   * 1. check if key has Grapevine type info
   * 2. check if value is integer/floating point number
   *
   * @param jsonMap
   */
  override def setup(jsonMap: Map[String, Any]): Unit = {

    // setup this as
    super.setup(jsonMap)
    // refresh the map
    map = MMap[String, GrapevineType]()

    jsonMap.foreach { case (key, v) =>
      if (v == null) {
        // do nothing when the input value is null
      }
      else if (v.isInstanceOf[GrapevineType]) {
        set(key, v.asInstanceOf[GrapevineType])
      }
      else {
        val t = GrapevineType.getTypeFromKey(key)
        if (t.nonEmpty) {
          set(key, t.get, v)
        } else {
          // t is empty which means the type info is not in the key
          val t = GrapevineType.getTypeFromValue(v)
          if (t.nonEmpty) set(key, t.get, v)
          else {
            throw new RuntimeException(s"No GrapevineType retrieved from key nor value:${key} - value:${v.getClass.toString}")
          }
        }
      }
    }
  }

  override def load(filePath: String): Unit = {
    super.load(filePath)
    setup(this._jsonMap)
  }

  override def repr() = {
    val sb = new StringBuilder
    map.foreach { case (key, gvData) =>
      sb.append(s"${key} => ${gvData.get}: ${gvData.getTypeName}\n")
    }
    sb.toString
  }
}
