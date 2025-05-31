package smcho

import java.io.{File, PrintWriter}

import scala.collection.mutable.{Map => mm, Set => mSet}
import net.liftweb.json._

/**
 * Created by smcho on 8/28/15.
 */

object Storage {
  var hostSizes:String = _
  var storage: Storage = null
  var summaries: Iterable[Summary] = _

  var summariesMap: mm[String, Summary] = _
  var hostToContextMessagesMap = mm[Int, mSet[ContextMessage]]()
  var hostToTuplesMap = mm[Int, mSet[(Int, Int, Double, String, Int)]]()

  def reset() = {
    storage = null
    summaries = null
    summariesMap = mm[String, Summary]()
    hostToContextMessagesMap = mm[Int, mSet[ContextMessage]]()
    hostToTuplesMap = mm[Int, mSet[(Int, Int, Double, String, Int)]]()
  }

  def apply(directory:String, hostSizes:String) = {
    if (storage == null) storage = new Storage(directory, hostSizes)
    storage
  }
}

class Storage(val directory:String, val hostSizes:String) {

  implicit val formats = DefaultFormats

  Storage.hostSizes = hostSizes
  Storage.summariesMap = Summary.loadContexts(directory, hostSizes)
  Storage.summaries = Storage.summariesMap.values
  ContextMessage.summariesMap = Storage.summariesMap

  def summaries = Storage.summaries
  def summariesMap = Storage.summariesMap

  override def toString = {
    s"""summary has ${Storage.summaries.size} items, map has ${Storage.summaries.size} items"""
  }

  def save(path:String) = {
    val f = new PrintWriter(new File(path))
    f.write(repr())
    f.close()
  }

  def repr() = {

    def getJsonFromSummaries() = {

      val keys = Storage.summariesMap.keys.toList.sorted
      val sb = new StringBuilder()

      keys foreach {key =>
        val value = Storage.summariesMap(key).repr()
        sb ++= s"${value}, "
      }
      sb.toString.dropRight(1)
    }

    def getJsonFromHostToContextMessagesMap() = {

      def dictToJson(m:Tuple2[Int, mSet[ContextMessage]]) = {
        def setToJson(set:mSet[ContextMessage]) = {
          val sb = (new StringBuilder() /: set ) { (acc, value) =>
            acc ++= value.repr + ","
          }
          "[" ++ sb.toString.dropRight(1) ++ "]"
        }
        s""""${m._1}":${setToJson(m._2)}"""
      }

      val sb = (new StringBuilder() /: Storage.hostToContextMessagesMap ) { (acc, value) =>
        acc ++= dictToJson(value) + ","
      }
      sb.toString.dropRight(1)
    }

    def getJsonFromHostToTuplesMap() = {

      def dictToJson(key:Int, value:mSet[(Int, Int, Double, String, Int)]) = {

        def setToJson(set:mSet[(Int, Int, Double, String, Int)]) = {

          def getJsonList(value:(Int, Int, Double, String, Int)) = """[%d,%d,%5.2f,"%s",%d]""".format(value._1, value._2, value._3, value._4, value._5)

          val sb = new StringBuilder()
          var selfString:String = ""
          set foreach { elem =>
            if (elem._1 == 0 && elem._2 == 0) selfString = getJsonList(elem)
            else {
              sb ++= s"${getJsonList(elem)},"
            }
          }
          "[" ++ selfString ++ "," ++ sb.toString.dropRight(1) ++ "]"
        }

        s""""${key}":${setToJson(value)},"""
      }

      val sb = new StringBuilder()
      val keys = Storage.hostToTuplesMap.keys.toList.sorted

      keys foreach { key =>
        val res = dictToJson(key, Storage.hostToTuplesMap(key))
        sb ++= res
      }
      sb.toString.dropRight(1)
    }

    val result = s"""{"summaries":[${getJsonFromSummaries()}],\n"hostToTuplesMap":{${getJsonFromHostToTuplesMap()}}}"""
    pretty(render(parse(result)))

  }

  def add(host:Int, c:ContextMessage) = {

    // hostToContextMessagesMap process
    if (!Storage.hostToContextMessagesMap.contains(host)) {
      Storage.hostToContextMessagesMap(host) = mSet[ContextMessage]()
    }
    val set = Storage.hostToContextMessagesMap(host)
    set += c
    Storage.hostToContextMessagesMap(host) = set

    // hostToTuplesMap process
    if (!Storage.hostToTuplesMap.contains(host)) {
      Storage.hostToTuplesMap(host) = mSet[(Int, Int, Double, String, Int)]()
    }
    NameTypes.split(c.nameTypesString) foreach {
      nameType =>
        val tupleSet = Storage.hostToTuplesMap(host) //
        tupleSet.add(c.host1, c.host2, c.time, nameType, NameType(nameType, Storage.summariesMap).size())
    }
  }

  def getContexts(host:Int) = {
    Storage.hostToContextMessagesMap.getOrElse(host, mSet[ContextMessage]()).toList
  }

  def getTuples(host:Int) = {
    Storage.hostToTuplesMap.getOrElse(host, mSet[(Int, Int, Double, String, Int)]()).toList
  }
}
