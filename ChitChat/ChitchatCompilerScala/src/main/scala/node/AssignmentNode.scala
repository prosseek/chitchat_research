package node

case class AssignmentNode(override val name:String,
                          override val id:IdNode,
                          val expression:ExpressionNode) extends Node(name = name, id = id)
{
  /**
    * Given key, returns a value from the expression
    *
    * @param key
    */
  def getValueInString(key:String) : String = {
    if (expression.node.isInstanceOf[ValueNode]) {
      val value = expression.node.asInstanceOf[ValueNode]
      if (value.node.isInstanceOf[Constant_unitNode]) {
        val const = value.node.asInstanceOf[Constant_unitNode]
        return const.name
      }
    }
    throw new RuntimeException(s"When use getValue in assignment node, expression should be constant unit ${expression.name}")
  }

  /**
    * assignment: id '=' expression ;
    *
    * @param progNode
    * @return
    */
  def codeGen(progNode:ProgNode, labels:Map[String, String] = null) :String = {
    val idCode = id.codeGen(progNode)
    ""
  }
}

