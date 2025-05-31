package node

import node.codegen.Template
import scala.collection.mutable.{Map => MMap}

/**
  * === Example1 ===
  * {{{
  * situation partyTime(partyname) = ([date, time] - now) >= 0 _hour
  **
  *read partyname
  *jpeekfalse END
  *f2 partyTime 0
  *END:
  *stop
  *partyTime:
  *read time
  *jpeekfalse END
  *read date
  *jpeekfalse END
  *here
  *distance datetime
  *push 0
  *geq
  *r 0
  *}}}
  *=== Example2 ===
    *{{{
    *   value cityParkCenter(latitude, longitude) = {
    *      latitude = [30, 25, 01, 74]
    *      longitude = [-97, 47, 21, 83]
    *   }
    *   situation nearCityPark() = |[latitude, longitude] - cityParkCenter| <= 5 _km
  *#     f2 nearCityPark 0
    *   END:
    *       stop
    *
    *   nearCityPark:
    *       read latitude
    *       jpeekfalse END
    *       read longitude
    *       jpeekfalse END
    *       push [30, 25, 1, 74]
    *       push [-97, 47, 21, 83]
    *       abs location
    *       push 5000.0
    *       fleq
    *       r 0
    *
*}}}
 *
 */

case class SituationNode (override val name:String,
                          override val id:IdNode,
                          val params:ParamsNode,
                          val expression:ExpressionNode) extends Node(name = name, id = id) with Template {

  /**
    * === why ===
    *  {{{ From the function body (comparison node)
    *   situation partyTime(partyname) = ([date, time] - now) >= 0 _hour
    *
    *  generate this assembly code (
    *
    *    read time
    *    jpeekfalse END
    *    read date
    *    jpeekfalse END
    *    now
    *    distance datetime
    *    push 0
    *    geq
    *    r 0
    *  }}}
    *
    *  or
    *
    *  {{{
    *     situation nearCityPark() = |(latitude, longitude) - cityParkCenter| <= 5 _km
    *
    *    read latitude
    *    jpeekfalse END
    *    read longitude
    *    jpeekfalse END
    *    push [30, 25, 1, 74]
    *    push [-97, 47, 21, 83]
    *    abs location
    *    push 5000
    *    leq
    *    r 0
    *
    *  }}}
    *
    * === Algorithm ===
    *
    *   1. from the 1st parameter - list [ ... ], get the read/jpeekfalse code
    *   2. from the 2nd parameter, find corresponding values
    *      2.1 if value is predefined, do special process
    *   3. identify the correct function (abs location)
    *   4. process the later part after <=
    *   5. process the operator (fleq/geq)
    *   6. return value
    *
    * @param progNode
    * @param endLabel
    * @return
    */
  def getFunctionBody(progNode:ProgNode, endLabel:String) :String = {
    val res = new StringBuilder

    // only comparsion expression is allowed
    if (expression.isComparison) {
      val c = expression.asComparison

      val map = MMap[String, String]()
      val template =
        """
          |#{code_from_list}
          |#{code_from_value}
          |#{push_value}
          |#{compare}
          |r 0
        """.stripMargin

      val e1 = c.expression1
      val listNode: ListNode = if (e1.isAbsolute || e1.isArithmetic)
        if (e1.isAbsolute) e1.asAbsolute.expression1.asValue.asList
        else e1.asArithmetic.expression1.asValue.asList
      else throw new RuntimeException(s"e1 in comparison node is neither absolute nor arithmetic")

      val idNode:IdNode = if (e1.isAbsolute) e1.asAbsolute.expression2.asValue.asId
      else e1.asArithmetic.expression2.asValue.asId

      val e2 = c.expression2

      map("code_from_list") = getCodeFromList(listNode, endLabel)
      map("code_from_value") = getCodeFromId(idNode, progNode)
      map("push_value") = e2.asValue.asConstantUnit.codeGen(progNode)
      map("compare") = c.compareCodeGen

      getTemplateString(template, map.toMap)
    }
    else
      throw new RuntimeException(s"Only comparison is allowed in situation node ${name}")
  }

  def getCodeFromList(l:ListNode, endLabel:String) : String = {
    val s = new StringBuilder
    l.values foreach {
      value => {
        if (value.isId) {
          val id = value.asId.name
          s ++= s"read ${id}\njpeekfalse ${endLabel}\n"
        }
        else
          throw new RuntimeException(s"only id is allowed in situation node's list")
      }
    }
    return s.toString
  }

  // todo: only ([list] - valuedef) format is allowed here, more general case should be supported
  def getCodeFromId(id:IdNode, progNode:ProgNode) : String = {
    // todo: process special case
    // need also special case of "here"
    // todo: make a function to process this case
    if (id.name == "now") {
      s"now\ndistance datetime\n"
    }
    else {
      val vdef = progNode.getNode[ValuedefNode](id.name, progNode.valuedefs)

      var location = false
      if (vdef.isDefined) {
        val s = new StringBuilder
        vdef.get.map foreach {
          case (key, value) => {
            // todo: too simplistic location check
            if (key == "longitude") location = true
            s ++= s"push $value\n"
          }
        }
        if (location) s ++= "abs location"
        s.toString
      }
      else
        throw new RuntimeException(s"only valuedef or predefined valuedef is supported here, you missed the value definition ${id.name}")
    }
  }

  def codeGen(progNode:ProgNode, labels:Map[String, String] = null) :String = {
    val template =
      """
        |#{precode}
        |f2 #{funcname} 0
        |#{label_end}:
        |stop
        |#{funcname}:
        |#{function_body}
      """.stripMargin
    val map = MMap[String, String]()

    map("funcname") = id.name
    val endLabel:String = id.name + "_END"
    map("label_end") = endLabel
    map("precode") = getPrecode(endLabel)
    map("function_body") = getFunctionBody(progNode, endLabel)

    getTemplateString(template, map.toMap)
  }

  /**
    * === Why ===
    *
    *  {{{ From the function parameter (partytime)
    *   situation partyTime(partyname) = ([date, time] - now) >= 0 _hour
    *
    *  generate this assembly code
    *
    *      read partyname
    *      jpeekfalse END
    *  }}}
    *
    * @param endLabel
    * @return
    */
  def getPrecode(endLabel:String) = {
    val res = new StringBuilder()
    val ps = params.ids map {
      id => res ++= s"read ${id.name}\njpeekfalse ${endLabel}\n"
    }
    res.toString
  }
}
