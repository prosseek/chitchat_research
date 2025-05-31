package smcho

import core.GrapevineSummary

import scala.collection.mutable.ListBuffer

import scala.collection.mutable.{Set => mSet}

object SimpleShareLogic {
  def apply() = new SimpleShareLogic()
}

/**
 * This module is dynamically loaded
 * You must invoke setStorage to store the storage field after the instatiation
 *
 * Created by smcho on 8/24/15.
 */
class SimpleShareLogic extends ShareLogic {
  var storage = Storage.storage

  // ex) 3:4:5 to indicate group1 has 3 elements, group 2 has 4 elements, and group 3 has 5 elemtns
  var hostSizes:String = storage.hostSizes

  def getContextTuples(host:Int) = {
    storage.getTuples(host).toList
  }

  def findContextTuple(host:Int) : Option[(Int, Int, Double, String, Int)] = {
    // nameTypeString is without the type
    val nameTypeString = NameType.hostIdToContextName(host, hostSizes)
    val m = storage.getTuples(host)

    m foreach { e =>
      val (fr, to, t, name, size) = e
      if (name.contains(nameTypeString)) return Some(e)
    }
    None
  }

  def findContextTuple(name:String) : Option[(Int, Int, Double, String, Int)] = {
    val host = NameType.contextNameToHostId(name)

    findContextTuple(host)
  }

  def getContextNamesToSendAll(host: Int, limit:Int, initialSummaryType:String) = {
    val setOfContexts = getContextTuples(host)

    val sb = new StringBuilder()
    // maybe I can do some analysis based on the information
    setOfContexts foreach {
      case (host1, host2, time, nameType, size) =>
        sb.append(nameType + ":")
    }
    val total = sb.toString.dropRight(1)
    NameTypes.nameSort(total)
  }

  def tuplesToNameTypes(tuples: Seq[(Int, Int, Double, String, Int)]) = {

    if (tuples.size == 0) ""
    else {
      val sb = new StringBuffer()
      tuples foreach {
        case (host1, host2, time, name, size) =>
          sb.append(name + ":")
      }
      val total = sb.toString.dropRight(1)
      NameTypes.nameSort(total)
    }
  }

  def getContextNamesToSend(host: Int, limit:Int, key:String, value:String) = {

    val result = ListBuffer[(Int, Int, Double, String, Int)]()
    // 1. add itself
    //result += findContextTuple(host).get

    // 2. Get the similiar contexts
    if (!(key == null && value == null)) {
      result ++= getSimilarContexts(host, key, value)
    }

    // 3. get all the contexts chronologically
    val r = getContextsSorted(host, excludes=result)
    val r2 = addContextTupleUptoLimit(limit, r)

    tuplesToNameTypes(r2)
  }

  /**
   * We need initialSummaryType as we need to decide what is the summary type for the first time
   * in exchanging summaries
   *
   * @param host
   * @param limit
   * @param initialSummaryType
   * @return
   */
  override def get(host: Int, limit:Int, initialSummaryType:String, key:String, value:String): String = {
    // SimpleShareLogic blindingly aggregates all the available contexts and share
    // 1. get the whole tuple that it contains
    val setOfContexts = getContextTuples(host)

    // For the first context sharing
    if (setOfContexts.size == 0) {
      val nameTypeString = NameType.hostIdToContextName(host, hostSizes) + initialSummaryType
      val cm = ContextMessage(nameTypeString)
      storage.add(host, cm)
      nameTypeString
    } else {
      getContextNamesToSend(host, limit, key, value)
    }
  }

  override def get(host: Int, limit:Int, initialSummaryType:String): String = {
    get(host, limit, initialSummaryType, null, null)
  }

  def addContextTupleUptoLimit(limit:Int, contextTuples:Seq[(Int, Int, Double, String, Int)]) : Seq[(Int, Int, Double, String, Int)] = {

    var sum = 0
    val result = ListBuffer[(Int, Int, Double, String, Int)]()

    contextTuples foreach {
      case (f, to, time, nameType, size) => {
        sum += size
        if (sum > limit) return result
        else
          result += ((f, to, time, nameType, size))
      }
    }
    result
  }

  def getSimilarContexts(host:Int, key:String, value:String) = {
    val result = ListBuffer[(Int, Int, Double, String, Int)]()
    val m = storage.getTuples(host)
    m foreach {
      case (f, to, time, nameType, size) => {
        val summaryType = nameType.takeRight(1)
        val summaryName = nameType.dropRight(1)

        val s = storage.summariesMap(summaryName)
        var gs:GrapevineSummary = null

        summaryType match {
          case "b" => gs = s.bloomierSummary
          case "l" => gs = s.labeledSummary
          case "j" => gs = s.labeledSummary
        }

        if (gs.get(key) != null) {
          val v = gs.get(key).asInstanceOf[String].toLowerCase()
          if (v.contains(value.toLowerCase()) || value.toLowerCase().contains(v)) {
            result += ((f, to, time, nameType, size))
          }
        }
      }
    }
    result
  }

  def containsContext(needle:(Int, Int, Double, String, Int), hayStack:Seq[(Int, Int, Double, String, Int)]): Boolean = {
    hayStack foreach {
      case (f, to, time, nameType, size) => if (nameType.contains(needle._4)) return true
    }
    false
  }

  def getContextsSorted(host:Int, excludes:Seq[(Int, Int, Double, String, Int)]) = {
    val sortedTuple = storage.getTuples(host).sortBy(-_._3)

    if (excludes == null) sortedTuple
    else {
      val result = ListBuffer[(Int, Int, Double, String, Int)]()
      sortedTuple foreach { e => if (!containsContext(e, excludes)) result += e}
      result
    }
  }
}
