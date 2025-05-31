package visitor

import node._
import parser.ChitchatParser.{ExpressionsContext, SchemaContext, SchemeContext}

import scala.collection.mutable.ListBuffer

/**
  * schema: annotation SCHEMA id '=' '(' (scheme ','?)+ ')' ;
  * case class SchemaNode(override val name:String, override val id:IdNode, val annotation:String, val schemes:List[SchemeNode])
  */
trait SchemaProcessor {
  def process(ctx: SchemaContext, o: ChitchatVisitor): SchemaNode = {

    val it = ctx.children.iterator()
    val schemes = ListBuffer[SchemeNode]()
    while (it.hasNext()) {
      val n = it.next()
      if (n.isInstanceOf[SchemeContext]) {
        val res = o.visit(n.asInstanceOf[SchemeContext]).asInstanceOf[SchemeNode]
        schemes += res
      }
    }

    SchemaNode(name = ctx.getText(),
      annotation = ctx.annotation().getText(),
      id = o.visit(ctx.id()).asInstanceOf[IdNode],
      schemes = schemes.toList)
  }
}
