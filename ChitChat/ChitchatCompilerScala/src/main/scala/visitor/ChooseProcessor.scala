package visitor

import node._
import parser.ChitchatParser._

import scala.collection.mutable.ListBuffer

trait ChooseProcessor {
  def process(ctx: ChooseContext, o: ChitchatVisitor): ChooseNode = {
    val name = ctx.getText()

    val res = ListBuffer[IdNode]()
    val it = ctx.children.iterator()

    while(it.hasNext()) {
      val n = it.next()
      if (n.isInstanceOf[IdContext]) {
        res += o.visit(n.asInstanceOf[IdContext]).asInstanceOf[IdNode]
      }
    }
    ChooseNode(name = name, ids = res.toList)
  }
}
