package node

import node.codegen.Template
import scala.collection.mutable.{Map => MMap}

case class ComparisonNode(
                          override val name:String,
                          val expression1:ExpressionNode,
                          val op:String,
                          val expression2:ExpressionNode) extends Node(name = name) with Template {
  def codeGen(progNode:ProgNode, labels:Map[String, String] = null) :String = {
    val e1 = expression1.codeGen(progNode)
    val e2 = expression2.codeGen(progNode)

    val map = MMap[String, String]()
    map("op") = compareCodeGen
    map("e1") = e1
    map("e2") = e2
    val template =
      s"""#{e1}
         |#{e2}
         |#{op}
      """.stripMargin
    val res = getTemplateString(template, map.toMap)
    res
  }

  def compareCodeGen() :String = {
    op match {
      case "==" => "cmp"
      case ">=" => "geq"
      case "<=" => "leq"
      case ">" => "greater"
      case "<" => "less"
      case _ => throw new RuntimeException(s"Wrong operator ${op}")
    }
  }
}

