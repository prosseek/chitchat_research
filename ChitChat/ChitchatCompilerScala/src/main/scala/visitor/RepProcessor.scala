package visitor

import node._
import parser.ChitchatParser._
import scala.collection.mutable.ListBuffer
/**
  * class RepNode(override val name:String, val ids:List[IdNode]) extends Node(name = name) {
  * rep: '(' (id ','?)+ ')' '+';
  */
trait RepProcessor {
  def process(ctx: RepContext, o: ChitchatVisitor): RepNode = {
    val name = ctx.getText()

    val res = ListBuffer[IdNode]()
    val it = ctx.children.iterator()

    while(it.hasNext()) {
      val n = it.next()
      if (n.isInstanceOf[IdContext]) {
        res += o.visit(n.asInstanceOf[IdContext]).asInstanceOf[IdNode]
      }
    }
    RepNode(name = name, ids = res.toList)
  }
}
