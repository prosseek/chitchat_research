package visitor

import node.{ConstantNode, Constant_unitNode}
import parser.ChitchatParser.Constant_unitContext

trait Constant_unitProcessor {
  def process(ctx: Constant_unitContext, o:ChitchatVisitor) : Constant_unitNode = {
    val c = o.visit(ctx.constant()).asInstanceOf[ConstantNode]
    val u = if (ctx.unit() == null) "" else ctx.unit().getText()

    Constant_unitNode(name = ctx.getText(), constant = c, unit = u)
  }
}
