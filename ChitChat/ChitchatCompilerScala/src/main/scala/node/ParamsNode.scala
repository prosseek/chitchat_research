package node

case class ParamsNode(override val name:String, val ids:List[IdNode]) extends Node(name = name) {
  def codeGen(progNode:ProgNode, labels:Map[String, String] = null) :String = {
    ""
  }
}


