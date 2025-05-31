package node

import node.codegen.Template
import scala.collection.mutable.{Map => MMap}

// value: id | constant | list ;
case class ValueNode (override val name:String, val node:Node) extends Node(name = name) with Template {

  def isList = {
    node.isInstanceOf[ListNode]
  }
  def asList : ListNode = {
    if (isList) node.asInstanceOf[ListNode]
    else throw new RuntimeException(s"expression node is not list node")
  }

  def isId = {
    node.isInstanceOf[IdNode]
  }
  def asId : IdNode = {
    if (isId) node.asInstanceOf[IdNode]
    else throw new RuntimeException(s"expression node is not id node")
  }

  def isConstantUnit = {
    node.isInstanceOf[Constant_unitNode]
  }
  def asConstantUnit : Constant_unitNode = {
    if (isConstantUnit) node.asInstanceOf[Constant_unitNode]
    else throw new RuntimeException(s"expression node is not constant unit node")
  }

  def codeGen(progNode:ProgNode, labels:Map[String, String] = null) :String = {
    node match {
      case IdNode(name) => node.codeGen(progNode, null)
      case Constant_unitNode(name, constant, unit) => node.codeGen(progNode, null)
      case _ => "WHY?"
    }
  }
}

