package node

import node.codegen.Template

/*
  expression: function_call | value | assignment
          | '(' expression ')'
          | expression comparison_operator expression  // comparsion
          | expression logic_operator expression ;     // logic
 */

case class ExpressionNode(override val name:String, val node:Node) extends Node(name = name) with Template {

  def isValue = node.isInstanceOf[ValueNode]
  def asValue : ValueNode = {
    if (isValue) node.asInstanceOf[ValueNode]
    else throw new RuntimeException(s"expression node is not value node")
  }

  def isFunctionCall = node.isInstanceOf[Function_callNode]
  def asFunctionCall : Function_callNode = {
    if (isFunctionCall) node.asInstanceOf[Function_callNode]
    else throw new RuntimeException(s"expression node is not function call node")
  }

  def isAssignment = node.isInstanceOf[AssignmentNode]
  def asAssignment : AssignmentNode = {
    if (isAssignment) node.asInstanceOf[AssignmentNode]
    else throw new RuntimeException(s"expression node is not assignment node")
  }

  def isAbsolute = node.isInstanceOf[AbsoluteNode]
  def asAbsolute : AbsoluteNode = {
    if (isAbsolute) node.asInstanceOf[AbsoluteNode]
    else throw new RuntimeException(s"expression node is not absolute node")
  }

  def isArithmetic = node.isInstanceOf[ArithmeticNode]
  def asArithmetic : ArithmeticNode = {
    if (isArithmetic) node.asInstanceOf[ArithmeticNode]
    else throw new RuntimeException(s"expression node is not arithmetic node")
  }

  def isComparison = node.isInstanceOf[ComparisonNode]
  def asComparison : ComparisonNode = {
    if (isComparison) node.asInstanceOf[ComparisonNode]
    else throw new RuntimeException(s"expression node is not comparison node")
  }

  def isLogic = node.isInstanceOf[LogicNode]
  def asLogic : LogicNode = {
    if (isLogic) node.asInstanceOf[LogicNode]
    else throw new RuntimeException(s"expression node is not logic node")
  }

  def codeGen(progNode:ProgNode, labels:Map[String, String] = null) :String = {
    node match {
      case Function_callNode(name, id, constants) => node.codeGen(progNode)
      case AssignmentNode(name, id, expression) => node.codeGen(progNode)
      case ValueNode(name, node) => node.codeGen(progNode)
      case ComparisonNode(name, expression1, op, expression2) => node.codeGen(progNode)
      case LogicNode(name, expression1, op, expression2) => node.codeGen(progNode)
      case ArithmeticNode(name, expression1, op, expression2) => node.codeGen(progNode)
      case AbsoluteNode(name, expression1, expression2) => node.codeGen(progNode)
      case _ => throw new RuntimeException(s"Wrong Expression Node ${node}")
    }
  }
}

