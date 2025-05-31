package visitor

import node._
import parser.ChitchatParser._

import scala.collection.mutable.ListBuffer

trait ArgsProcessor {
  def process(ctx: ArgsContext, o:ChitchatVisitor) : ArgsNode = {
    val values = ListBuffer[ValueNode]()
    val it = ctx.children.iterator()

    while (it.hasNext()) {
      val item = it.next()
      if (item.isInstanceOf[ValueContext]) {
        values += o.visit(item.asInstanceOf[ValueContext]).asInstanceOf[ValueNode]
      }
    }
    ArgsNode(name = ctx.getText(), values = values.toList)
  }
}
