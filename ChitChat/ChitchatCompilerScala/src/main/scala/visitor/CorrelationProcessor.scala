package visitor

import node._
import parser.ChitchatParser.CorrelationContext

/**
  * ==== Grammar ====
  * // correlation
  * {{{
  *     correlation: CORRELATION id '=' '(' expressions ')' ;
  *     value: id | constant | list ; (only id is used)
  *     function: FUNCTION id params '=' block ;
  * }}}
  *
  */
trait CorrelationProcessor {
  def process(ctx: CorrelationContext, o:ChitchatVisitor) : CorrelationNode = {
    val c = CorrelationNode(name = ctx.getText(), id = o.visit(ctx.id()).asInstanceOf[IdNode])
    val expressions = o.visit(ctx.expressions()).asInstanceOf[ExpressionsNode].expressions

    expressions foreach { expression =>
      val n = expression.node
      if(n.isInstanceOf[ValueNode]) {
        val vnode = n.asInstanceOf[ValueNode]
        c.add(vnode)
      }
      else if (n.isInstanceOf[Function_callNode]) {
        val fcallNode = n.asInstanceOf[Function_callNode]
        c.add(fcallNode)
      }
    }

    c
  }
}
