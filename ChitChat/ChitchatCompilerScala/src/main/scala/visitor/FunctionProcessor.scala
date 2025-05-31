package visitor

import node._
import parser.ChitchatParser.FunctionContext

/**
  * function: FUNCTION return_type id params '=' block ;
  *
  *
  * case class FunctionNode(override val name:String,
                        val return_type:String,
                        override val id:String,
                        val params:Seq[ValueNode],
                        val block:BlockNode)
  */
trait FunctionProcessor {
  def process(ctx:FunctionContext, o:ChitchatVisitor) = {
    val name = ctx.getText()
    val return_type = ctx.return_type().getText()
    val id = o.visit(ctx.id()).asInstanceOf[IdNode]

    // val ids:List[IdNode]
    val ids = o.visit(ctx.params()).asInstanceOf[ParamsNode].ids
    val params = ids map {id => id.name}
    val block = o.visit(ctx.block()).asInstanceOf[BlockNode]
    FunctionNode(name = name, return_type = return_type, id = id, params = params, block = block)
  }
}
