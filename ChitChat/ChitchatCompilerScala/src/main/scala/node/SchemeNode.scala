package node

import node.codegen.Template
import scala.collection.mutable.{Map => MMap}
/*
  scheme: id | rep | option;
 */
case class SchemeNode(override val name:String,
                      val node:Node) extends Node(name = name) with Template {

  def isId() = {
    node.isInstanceOf[IdNode]
  }
  def asId() = {
    if (isId) node.asInstanceOf[IdNode]
    else throw new RuntimeException(s"Not id node")
  }
  def isRep() = {
    node.isInstanceOf[RepNode]
  }
  def asRep() = {
    if (isRep) node.asInstanceOf[RepNode]
    else throw new RuntimeException(s"Not rep node")
  }

  def isChoose() = {
    node.isInstanceOf[ChooseNode]
  }
  def asChoose() = {
    if (isChoose) node.asInstanceOf[ChooseNode]
    else throw new RuntimeException(s"Not choose node")
  }

  def codeGen(progNode:ProgNode, labels:Map[String, String] = null) :String = {
    val endLabel = labels("endLabel")

    if (isId()) {
      asId().schemaCodeGen(progNode, endLabel)
    }
    else if (isChoose()) {
      asChoose().codeGen(progNode, labels)
    }
    else if (isRep()) {
      asRep().headerCodeGen(progNode, labels)
    }
    else throw new RuntimeException(s"node should be id/choose/rep")
  }
}
