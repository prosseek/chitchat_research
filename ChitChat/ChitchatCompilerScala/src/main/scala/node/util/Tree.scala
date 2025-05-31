package node.util

import node.CorrelationNode
import scala.collection.mutable.ListBuffer

case class Node(val name:String, val children:ListBuffer[Node])

case class Tree (val correlationNodes:List[CorrelationNode]) {
  val nodes = ListBuffer[Node]()
  // create all the nodes from input
  correlationNodes foreach (makeNode(_))

  def getNode(name:String) : Option[Node] = {
    val result = this.nodes filter {
      node => node.name == name
    }
    if (result.length > 1) throw new RuntimeException(s"more than 1 elements in nodes ${name}")
    if (result.length == 0) None
    else Some(result(0))
  }

  def makeNode(correlationNode: CorrelationNode) = {
    val id = correlationNode.id.name

    val nodeNames = nodes map { _.name }
    if (!nodeNames.contains(id)) {
      nodes += Node(id, ListBuffer[Node]())
    }
    val node: Node = getNode(id).get

    // values will return ValueNode
    // create all nodes
    val children = correlationNode.values map { _.name}

    children foreach {
      child => {
        if (!nodeNames.contains(child)) {
          nodes += Node(child, ListBuffer[Node]())
        }
        node.children += getNode(child).get
      }
    }
  }

  def get(name:String) = {
    def _get(name: String, result: ListBuffer[String]) : Unit = {
      val node = getNode(name)
      if (node.isDefined) {
        val children = node.get.children

        if (children.length == 0) result += name
        else
          children foreach {
            child => {
              val name = child.name
              _get(name, result)
            }
          }
      }
    }
    val result = ListBuffer[String]()
    _get(name, result)
    result.toList
  }
}