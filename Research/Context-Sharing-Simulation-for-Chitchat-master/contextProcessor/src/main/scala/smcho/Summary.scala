package smcho

import java.io.File
import scala.collection.mutable.{Map => mm, ListBuffer}
import net.liftweb.json.Serialization.{write => jsonWrite}

import util.io.{File => uFile}
import core.{BloomierFilterSummary, LabeledSummary, ContextSummary}

import java.io.FileInputStream
import java.util.Properties
import scala.collection.JavaConversions._

class Summary(var name:String, val filePath:String) {

  val confFilePath = Summary.getConfigurationFilePath(filePath)
  val conf = util.file.readers.readProperty(confFilePath)
  val labeledSummary = LabeledSummary(filePath)
  val bloomierSummary = bloomier(labeledSummary)

  val sizeLabeled = labeledSummary.getSize()
  var sizeBloomier = bloomierSummary.getSize()
  var sizeJson = labeledSummary.getJsonSize()
  var fileName = filePath.split("/").takeRight(1)(0)

  private def bloomier(labeledSummary: LabeledSummary) = {
    val bf = BloomierFilterSummary(labeledSummary)
    //val m : Int = math.ceil(labeledSummary.getKeys().length * 1.5).toInt
    bf.setup(labeledSummary.getMap(),
        m = conf("m").asInstanceOf[Int],
        k = conf("k").asInstanceOf[Int],
        q = conf("q").asInstanceOf[Int],
        complete = if (conf("complete").asInstanceOf[Int] == 1) true else false)
    bf
  }

  def size(summaryType: String) = {
    summaryType match {
      case "b" => sizeBloomier
      case "l" => sizeLabeled
      case "j" => labeledSummary.getJsonSize()
      case _ => throw new Exception(s"Format error ${summaryType}")
    }
  }
  def sizes = (sizeJson, sizeLabeled, sizeBloomier)
  def keys = labeledSummary.getKeys()

//  def copy(newSummaryType: String = "b") = {
//    new Summary(name=name, filePath=filePath, defaultSummaryType=newSummaryType)
//  }

  def repr() = s"""{"name":"${name}", "sizes":[${sizes._1},${sizes._2},${sizes._3}], "fileName":"${fileName}"}"""
  override def toString() = s"${name}|[${sizes._1},${sizes._2},${sizes._3}]"
}

object Summary {
  def summariesToJsonString(summaries:mm[String, Summary]) = {
    var sb = new StringBuilder()
    sb ++= "[\n"
    summaries foreach {
      case (key, value) => sb ++= (s"""{"${key}":${value.repr},\n""")
    }
    sb.toString.dropRight(2) + "\n]"
  }

  def getConfigurationFilePath(filePath:String) = {
    val confFilePath = filePath.replace(".json", ".conf")
    if (new File(confFilePath).exists) confFilePath
    else throw new Exception(s"No configuration file ${confFilePath}")
  }

  def loadContext(directory: String, name: String, othername: String) = {
    val absoluteDirectory = new File(".").getAbsoluteFile() + "/" + directory
    var filePath = absoluteDirectory + "/" + name + ".json"

    if (!(new File(filePath).exists())) {
      val otherFilePath = absoluteDirectory + "/" + othername + ".json"
      if (!new File(otherFilePath).exists)
        throw new Exception(s"Neither ${filePath} nor ${otherFilePath} exists")
      else
        filePath = otherFilePath
    }
    new Summary(name = name, filePath = filePath)
  }

  def loadContexts(directory: String) = {
    val summariesMap = mm[String, Summary]();
    // executed in one simulator, the "." is inside the one simulator directory, so there should be some changes
    // such as symbolic links should be added.
    val absoluteDirectory = new File(".").getAbsoluteFile() + "/" + directory

    val files = new java.io.File(absoluteDirectory).listFiles.filter(_.getName.endsWith(".json")) // context is in txt format

    for (file <- files if !file.getName().replace(".json","").matches("default.*$")) {
      val fileName = file.toString
      val key = uFile.getBasename(fileName).replace(".json","")

      val groupId = NameParser.getGroupIdIgnoringSummaryType(key)
      summariesMap(key) = Summary.loadContext(directory = directory, name = key, othername = s"default${groupId}")
    }
    summariesMap
  }

  def loadContexts(directory: String, hostSizes:String) : mm[String, Summary] = {
    loadContexts(directory, NameType.hostSizesStringToList(hostSizes))
  }
  /**
   * g1c0 ... gNcX : N is the number of groups, X-1 is the number of hosts
   * @param directory
   * @param hostSizes
   * @return
   */
  def loadContexts(directory: String, hostSizes:Iterable[Int]) : mm[String, Summary] = {
    val summariesMap = loadContexts(directory)
    val absoluteDirectory = new File(".").getAbsoluteFile() + "/" + directory

    var sum = 0
    hostSizes.zipWithIndex foreach {
      case (count, index) => {
        for (i <- 0 until count) {
          val name = s"g${index+1}c${sum}"
          val defaultName = s"default${index+1}"
          sum += 1
          if (!summariesMap.contains(name)) {
            summariesMap(name) = loadContext(directory = directory, name = name, othername = defaultName)
          }
        }
      }
    }
    summariesMap
  }
}