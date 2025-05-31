package visitor

import node._
import parser.ChitchatParser.ValuedefContext
import scala.collection.mutable.{Map => MMap}
/**
  * valuedef: VALUE id params '=' block ;
  * ValuedefNode(override val name:String, override val id:IdNode, val map:Map[String, String])
  */
trait ValuedefProcessor {
  def process(ctx: ValuedefContext, o:ChitchatVisitor) : ValuedefNode = {

    val expressions = o.visit(ctx.block()).asInstanceOf[BlockNode].expressions.expressions

    // todo: the params are not checked.
    // we assume all the parameters are the same as map.keySet(), but this may not always be true
    val res = expressions map {
      case expression if (expression.node.isInstanceOf[AssignmentNode]) => {
        val node = expression.node.asInstanceOf[AssignmentNode]
        (node.id.name, node.expression.name)
      }
      case _ => throw new RuntimeException(s"only assignment format is allowed")
    }

    ValuedefNode(name = ctx.getText(),
      id = o.visit(ctx.id()).asInstanceOf[IdNode],
      map = res.toMap)
  }
}
