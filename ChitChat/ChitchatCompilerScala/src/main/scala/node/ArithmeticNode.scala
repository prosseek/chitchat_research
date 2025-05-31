package node

import node.codegen.Template

case class ArithmeticNode(override val name:String,
                              val expression1:ExpressionNode,
                              val op:String,
                              val expression2:ExpressionNode) extends Node(name = name) with Template {
  def codeGen(progNode:ProgNode, labels:Map[String, String] = null) :String = {
    ""
  }
}