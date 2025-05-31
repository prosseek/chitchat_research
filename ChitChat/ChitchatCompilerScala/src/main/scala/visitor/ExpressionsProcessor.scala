package visitor

import node._
import parser.ChitchatParser._

import scala.collection.mutable.ListBuffer

trait ExpressionsProcessor {
  def process(ctx: ExpressionsContext, o:ChitchatVisitor) : ExpressionsNode = {
    val expressions = ListBuffer[ExpressionNode]()
    val it = ctx.children.iterator()

    while (it.hasNext()) {
      val item = it.next()
      if (item.isInstanceOf[ExpressionContext]) {
        expressions += o.visit(item.asInstanceOf[ExpressionContext]).asInstanceOf[ExpressionNode]
      }
    }
    ExpressionsNode(name = ctx.getText(), expressions = expressions.toList)
  }
}
