package visitor

import node._
import parser.ChitchatParser._

/**
  * value: id | constant | list ;
  */
trait ValueProcessor {
  def process(ctx: ValueContext, o:ChitchatVisitor) : ValueNode = {
    if (ctx.constant_unit() != null)
      return ValueNode(name = ctx.getText(), node = o.visit(ctx.constant_unit()))
    else if (ctx.id() != null)
      return ValueNode(name = ctx.getText(), node = o.visit(ctx.id()))
    else if (ctx.list() != null)
      return ValueNode(name = ctx.getText(), node = o.visit(ctx.list()))
    else
      throw new RuntimeException(s"No value node ${ctx.getText()}")
  }
}
