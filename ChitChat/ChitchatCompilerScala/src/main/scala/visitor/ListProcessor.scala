package visitor

import node._
import parser.ChitchatParser._

import scala.collection.mutable.ListBuffer

/**
  * list: '[' (value ','?)+ ']' ;
  */
trait ListProcessor {
  def process(ctx: ListContext, o:ChitchatVisitor) : ListNode = {
    val result = ListBuffer[ValueNode]()
    val it = ctx.children.iterator()
    while(it.hasNext()) {
      val item = it.next()
      if (item.isInstanceOf[ValueContext]) {
        // todo: not fully tested
        result += o.visit(item.asInstanceOf[ValueContext]).asInstanceOf[ValueNode]
      }
    }
    ListNode(name = ctx.getText(), values = result.toList)
  }
}
