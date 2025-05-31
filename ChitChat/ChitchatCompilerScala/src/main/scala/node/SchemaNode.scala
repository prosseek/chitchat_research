package node

import node.codegen.Template

import scala.collection.mutable.{Map => MMap}

/**
  * schema: annotation SCHEMA id '=' '(' (scheme ','?)+ ')' ;
  * scheme: id | rep;
  * rep: '(' (id ','?)+ ')' '+';
  *
  * @param name
  * @param id
  * @param annotation
  * @param schemes
  */
case class SchemaNode(override val name:String,
                      override val id:IdNode,
                      val annotation:String,
                      val schemes:List[SchemeNode]) extends Node(name = name, id = id) with Template {

  def codeGen(progNode:ProgNode, labels:Map[String, String] = null) :String = {
    val name = id.name
    val end = s"${name}_END"

    val template =
      """function_call #{name}
        |stop
        |
        |#{name}:
        |#{content}
        |#{end}:
        |return 0
        |
        |#{rep_content}
      """.stripMargin
    val map = MMap[String, String]()

    map("name") = name
    map("end") = end

    val labels = Map[String, String]("endLabel" -> end)

    map("content") = getContent(progNode, labels)
    map("rep_content") = getRepContent(progNode, labels)

    getTemplateString(template, map.toMap)
  }

  def getContent(progNode:ProgNode, labels:Map[String, String]) = {
    val res = new StringBuilder
    schemes foreach {
      scheme => {
        res ++= scheme.codeGen(progNode, labels)
      }
    }
    res.toString
  }

  def getRepContent(progNode:ProgNode, labels:Map[String, String]) = {
    val res = new StringBuilder
    schemes foreach {
      scheme => {
        if (scheme.isRep()) {
          val node = scheme.asRep()
          res ++= node.codeGen(progNode, labels)
        }
      }
    }
    res.toString
  }
}
