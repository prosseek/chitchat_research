package node

abstract class Node(val name:String = "", val id:IdNode = null) {

  def codeGen(progNode:ProgNode, labels:Map[String, String] = null) : String
}
