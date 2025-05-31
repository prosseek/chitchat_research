package node

// function_call: ID '(' expressions ')' ;
case class Function_callNode(override val name:String, override val id:IdNode, val args:ArgsNode)
  extends Node(name = name, id = id) {

  def codeGen(progNode:ProgNode, labels:Map[String, String] = null) :String = {
    s"function_call_stack ${id.name} ${args.values.size}\n"
  }
}