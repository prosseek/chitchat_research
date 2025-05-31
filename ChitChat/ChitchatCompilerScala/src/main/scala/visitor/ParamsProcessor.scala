package visitor

import node._
import parser.ChitchatParser._

import scala.collection.mutable.ListBuffer

trait ParamsProcessor {
  def process(ctx: ParamsContext, o:ChitchatVisitor) : ParamsNode = {
    val ids = ListBuffer[IdNode]()
    val it = ctx.children.iterator()

    while (it.hasNext()) {
      val item = it.next()
      if (item.isInstanceOf[IdContext]) {
        ids += o.visit(item.asInstanceOf[IdContext]).asInstanceOf[IdNode]
      }
    }
    ParamsNode(name = ctx.getText(), ids = ids.toList)
  }
}
