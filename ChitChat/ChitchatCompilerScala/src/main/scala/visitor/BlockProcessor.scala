package visitor

import node._
import parser.ChitchatParser.BlockContext

/*
  block: '{' expressions '}';
 */
trait BlockProcessor {
  def process(blockContext: BlockContext, o:ChitchatVisitor) :BlockNode = {
    val e = o.visit(blockContext.expressions()).asInstanceOf[ExpressionsNode]

    BlockNode(name = blockContext.getText(), expressions = e)
  }
}
