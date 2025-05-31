package node

case class ArgsNode(override val name:String, val values:List[ValueNode]) extends Node(name = name) {
  def codeGen(progNode:ProgNode, labels:Map[String, String] = null) :String = {
    ""
  }
}


