package visitor

import node._
import parser.ChitchatParser.AbsoluteContext

trait AbsoluteProcessor {

  /**
    * case class AbsoluteNode (override val name:String,
                    val expression1:ExpressionNode,
                    val op:String,
                    val expression2:ExpressionNode)

    * @param absolute
    * @param o
    * @return
    */
  def process(absolute: AbsoluteContext, o:ChitchatVisitor) :AbsoluteNode = {
    val name = absolute.getText()
    val e1 = o.visit(absolute.expression(0)).asInstanceOf[ExpressionNode]
    val e2 = o.visit(absolute.expression(1)).asInstanceOf[ExpressionNode]
    AbsoluteNode(name = name, expression1 = e1, expression2 = e2)
  }
}
