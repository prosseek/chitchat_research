package visitor

import node._
import parser.ChitchatParser.SchemeContext

// scheme: id | rep | choose;

trait SchemeProcessor {
  def process(ctx: SchemeContext, o: ChitchatVisitor): SchemeNode = {
    val name = ctx.getText()
    val node:Node = if (ctx.id() != null) o.visit(ctx.id())
    else if (ctx.rep() != null) o.visit(ctx.rep())
    else if (ctx.choose() != null) o.visit(ctx.choose())
    else throw new RuntimeException(s"scheme processor should be id or rep not ${name}")

    SchemeNode(name = name, node = node)
  }
}
