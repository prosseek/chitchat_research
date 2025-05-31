package node

import node.codegen.Template
import scala.collection.mutable.{Map => MMap}
case class LogicNode(
                      override val name:String,
                      val expression1:ExpressionNode,
                      val op:String,
                      val expression2:ExpressionNode) extends Node(name = name) with Template {
  def codeGen(progNode:ProgNode, labels:Map[String, String] = null) :String = {
    val template =
      """#{expression1}
        |#{expression2}
        |#{op}
        |
      """.stripMargin

    val map = MMap[String, String]()
    map("expression1") = expression1.codeGen(progNode)
    map("expression2") = expression2.codeGen(progNode)
    map("op") = op match {
      case "||" => "or"
      case "&&" => "and"
      case _ => throw new RuntimeException(s"Error in operator ${op}")
    }
    getTemplateString(template, map.toMap)
  }
}

