package node

object ValuedefNode {
  def predefined() = {
    val now = ValuedefNode(name = "now",
      id = IdNode.make("now"),
      Map[String, String]("now" -> "now"))
    List[ValuedefNode](now)
  }
}

case class ValuedefNode(override val name:String,
                        override val id:IdNode,
                        val map:Map[String, String]) extends Node(name = name, id = id) {
  var predefined = false

  def codeGen(progNode:ProgNode, labels:Map[String, String] = null) :String = {
    ""
  }
}
