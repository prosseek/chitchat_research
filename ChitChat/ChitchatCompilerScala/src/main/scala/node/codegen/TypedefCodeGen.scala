package node.codegen

import node._

import scala.collection.mutable.{ListBuffer, Map => MMap}

class TypedefCodeGen(val typedefNode:TypedefNode, val progNode:ProgNode)
  extends Template
  with AssignMapResolver {

  val typeNodes = progNode.typedefs.toList
  private def getTypeNodeFromName(typeNodeName:String) = {
    val typeNode = typeNodes find (_.id.name == typeNodeName)
    if (typeNode.isEmpty) throw new RuntimeException(s"No node type ${typeNodeName} found")
    typeNode.get
  }

  /**
    * Given a map with assignment elements, return a string that interpolates it.
    *
    * ==== Example ====
    * {{{
    *   new Range(name = "y", size = 7, min = -64, max = 63, signed = true)
    * }}}
    *
    * @param map
    * @return
    */
  def rangeMapToString(map:Map[String, String]) = {
    val range_template =
      s"""new #{group}(name = "#{name}", size = #{size}, min = #{min}, max = #{max}, signed=#{signed})""".stripMargin

    getTemplateString(range_template, map)
  }

  /**
    * get the '''contents''' for encoding type group
    *
    * ==== Example Encoding ====
    * {{{
    *   -type hour extends Range(size=5, min=0, max=23, signed=false)
    *   -type minute extends Range(size=6, min=0, max=59, signed=false)
    *   +type time extends Encoding(hour, minute)
    *   -type markethour extends hour(min=10, max=18)
    *   +type "market time" extends time(markethour)
    * }}}
    *
    * ==== Algorithm ====
    *
    *  1. From "market time", we know we can use the market hour from time(markethour)
    *     markethour has superclass hour
    *  2. From time, we get the encoding `time -> Encoding(hour, minute)`
    *    `hour` & `minute` is returned. So, we know this encoding has two ranges.
    *  3. We know that `hour` in step 2 should be replaced by the (markethour -> hour) history in step 1
    *     So remove the hour
    *  4. Merge 1 & 2 & 3 to leave only
    *     1. time (step 2 & 3)
    *     2. markethour -> hour (step1)
    *  5. We resolve to get assignments for `markethour` which overwrites the setup of `hour` & `minute`
    *
    * {{{
    *    class Market_time extends Encoding(
    *    name = "market time",
    *    Array[Range](
    *      new Range(name = "hour",   size = 5, min = 10, max = 18, signed = false),
    *      new Range(name = "minute", size = 6, min =  0, max = 59, signed = false)))
    * }}}
    *
    * @param typeNodeName
    * @return
    */
  def getContentForEncoding(typeNodeName:String) = {
    val typeNode = getTypeNodeFromName(typeNodeName)
    val historyList = ListBuffer[List[TypedefNode]]()

    /*
      market time's value => markethour only
      find all the history of "markethour" => "hour"
     */
    if (typeNode.values.length > 0) {
      typeNode.values foreach (value =>
        historyList += getHistory(value.name, typeNodes))
    }

    // get all of the ranges in the encoding
    // "market time" => (hour, encoding)
    val rangeNamesWithoutHistory = ListBuffer(getRangeNamesFromEncoding(typeNodeName, typeNodes):_*)
    historyList foreach {
      history => {
        // history = markethour - hour
        // 2. hour <-- this is removed as last item is the same as hour
        // 3. minute
        rangeNamesWithoutHistory -= history.last.id.name
      }
    }

    // hour is removed and minute is left
    // historyList adds the hour to get these two items in the history
    // 1. markethour - hour
    // 2. minute
    rangeNamesWithoutHistory foreach {
      rangeName => {
        val typeNode = getTypeNodeFromName(rangeName)
        historyList += List[TypedefNode](typeNode)
      }
    }

    // we need to fill in the map
    // the subclass values will override the super class values
    val rangeContentStrings = historyList map {
      history => {
        val map = getAssignMapFromHistory(history)
        map("name") = history.last.id.name
        val template = s"""new Range(name = "#{name}", size = #{size}, min = #{min}, max = #{max}, signed = #{signed})"""
        getTemplateString(template, map.toMap)
      }
    }
    rangeContentStrings.mkString("Array[Range](", ",", ")")
  }

  /**
    * ==== Example Range ====
    * {{{
    *  groupString:Range, typeNodeName:"market time"
    *
    *  --> class Markethour extends Range ( name = "markethour", size = 5, min = 10, max = 18, signed = false )
    * }}}
    *
    * @param typeNodeName
    * @return
    */
  def getContentForRange(typeNodeName:String) = {
    val template = s"size = #{size}, min = #{min}, max = #{max}, signed = #{signed}"
    val map = getAssignMapFromRangeName(typeNodeName, typeNodes)
    getTemplateString(template, map)
  }

  /**
    * ==== Example ====
    * {{{
    *   +type temperature extends Float(min=-50.0, max=90.0)
    * }}}
    *
    * @param typeNodeName
    * @return
    */
  def getContentForFloat(typeNodeName:String) = {
    val template = s"min = #{min}, max = #{max}"
    val map = getAssignMapFromFloatName(typeNodeName, typeNodes)
    getTemplateString(template, map)
  }

  /**
    * ==== Example ====
    * {{{
    *     class FTest2 extends String (name = "f", conditions = List(97, 'b'))
    * }}}
    *
    * @param typeNodeName
    * @return
    */
  def getContentForString(typeNodeName:String) = {
    val map = getMapFromStringName(typeNodeName, typeNodes)

    var template = ""
    if (map.get("type").get == "assign")
    {
      template = s"range = List(#{min}, #{max})"
    }
    else {
      template = s"""conditions = List("#{function_name}", #{value})"""
    }
    getTemplateString(template, map)
  }

  /**
    * Returns a type class content from groupString & typeNodeName
    *
    * @param groupString
    * @param typeNodeName
    * @return
    */
  def getContent(groupString:String, typeNodeName:String) : String = {
    if (groupString == "Range") {
      getContentForRange(typeNodeName)
    }
    else if (groupString == "Encoding") {
      getContentForEncoding(typeNodeName)
    }
    else if (groupString == "Float") {
      getContentForFloat(typeNodeName)
    }
    else if (groupString == "String") {
      getContentForString(typeNodeName)
    }
    else {
      throw new RuntimeException(s"wrong thype string ${groupString}")
    }
  }

  /** Given type node name as a string returns the Scala source code
    * The contents are generated from `getContent` method.
    *
    * @return
    */
  def generate() = {
    val typeNodeName:String = typedefNode.id.name
    val plugin_template =
      s"""package chitchat.types
          |class #{class_name} extends #{type_group_name} ( name = "#{name}", #{contents} )""".stripMargin

    // get the type name
    val typeGroup = getTypeGroupName(typeNodeName, typeNodes)
    val typeGroupName = typeGroup.base_name
    val contentString = getContent(typeGroupName, typeNodeName)

    val map = Map[String, String](
      "class_name" -> getClassName(typeNodeName),
      "type_group_name" -> typeGroupName,
      "name" -> typeNodeName,
      "contents" -> contentString)
    getTemplateString(plugin_template, map)
  }
}
