package node

import parser.ChitchatParser

import scala.collection.mutable.ListBuffer

// the name of prognode is the script path
case class ProgNode(override val name:String = "") extends Node(name = name) {
  val typedefs = ListBuffer[TypedefNode]()
  val correlations = ListBuffer[CorrelationNode]()
  val situations = ListBuffer[SituationNode]()
  val schemas = ListBuffer[SchemaNode]()
  val valuedefs = ListBuffer[ValuedefNode]()
  val functions = ListBuffer[FunctionNode]()
  val commands = ListBuffer[CommandNode]()

  // value node has predefined values
  ValuedefNode.predefined foreach {
    valuedefNode => {
      add(valuedefNode)
      valuedefNode.predefined = true
    }
  }

  // in expression node, parameters or local variables should
  // be translated into $bp - N.
  // context should be recorded to process this
  var context: FunctionNode = _

  /**
    * Read nodes into fields
    *
    * @param input
    * @return
    */
  def add(input:Node) = {
    input match {
      case TypedefNode(name, id, annotation, base_name) => typedefs += input.asInstanceOf[TypedefNode]
      case CorrelationNode(name, id) =>                    correlations += input.asInstanceOf[CorrelationNode]
      case SituationNode(name, id, params, expression) =>                      situations += input.asInstanceOf[SituationNode]
      case SchemaNode(name, id, annotation, expressions) =>                         schemas += input.asInstanceOf[SchemaNode]
      case ValuedefNode(name, id, map) =>                  valuedefs += input.asInstanceOf[ValuedefNode]
      case FunctionNode(name, return_type, id, params, block) =>        functions += input.asInstanceOf[FunctionNode]
      case CommandNode(name) =>                            commands += input.asInstanceOf[CommandNode]
      case _ => throw new RuntimeException(s"wrong node type")
    }
  }

  def getNode[T <: Node](name:String, nodes:ListBuffer[T]) : Option[T] = {
    val result = nodes filter (_.id.name == name)
    if (result.size == 0) return None
    if (result.size > 1) throw new RuntimeException(s"Error, multiple name $name")
    Some(result(0))
  }

  def isValue(value:String) : Option[String] = {
    valuedefs foreach {
      valuedef => if (valuedef.map.keySet.contains(value)) return valuedef.map.get(value)
    }
    None
  }

  def codeGen(progNode:ProgNode, labels:Map[String, String] = null) :String = {
    ""
  }
  def parameterTranslate(name:String) = {
    if (context == null) name
    else context.parameterTranslate(name)
  }
}
