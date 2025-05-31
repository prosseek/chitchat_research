package visitor

import node._
import parser.ChitchatParser.ExpressionContext

import scala.collection.mutable.ListBuffer

trait ExpressionProcessor  {
  /**
    * From the expression grammar create ExpressionNode
    * {{{
    *     expression: function_call | value | assignment | comparison ;
    * }}}
    *
    */

  def process(ctx: ExpressionContext, o:ChitchatVisitor) : ExpressionNode = {
    var result:Node = null

    if (ctx.getText().startsWith("(")) {
      result = o.visit(ctx.expression(0)).asInstanceOf[ExpressionNode]
    }
    else if (ctx.expression().size != 0) {
      val e1 = ctx.expression(0)
      val e2 = ctx.expression(1)

      if (ctx.comparison_operator() != null) {
        result = ComparisonNode(name=ctx.getText(),
          op = ctx.comparison_operator().getText(),
          expression1 = o.visit(e1).asInstanceOf[ExpressionNode],
          expression2 = o.visit(e2).asInstanceOf[ExpressionNode])
      }
      if (ctx.logic_operator() != null) {
        result = LogicNode(name=ctx.getText(),
          op = ctx.logic_operator().getText(),
          expression1 = o.visit(e1).asInstanceOf[ExpressionNode],
          expression2 = o.visit(e2).asInstanceOf[ExpressionNode])
      }
      if (ctx.arithmetic_operator() != null) {
        result = ArithmeticNode(name=ctx.getText(),
          op = ctx.arithmetic_operator().getText(),
          expression1 = o.visit(e1).asInstanceOf[ExpressionNode],
          expression2 = o.visit(e2).asInstanceOf[ExpressionNode])
      }
    }
    else if (ctx.absolute() != null) {
      result = o.visit(ctx.absolute())
    }
    else if (ctx.assignment() != null) {
      result = o.visit(ctx.assignment())
    }
    else if (ctx.function_call() != null) {
      result = o.visit(ctx.function_call())
    }
    else if (ctx.value() != null) {
      result = o.visit(ctx.value())
    }
    else if (ctx.absolute() != null) {
      result = o.visit(ctx.absolute())
    }
    else {
      throw new RuntimeException(s"Error expression wrong ${ctx.getText()}")
    }
    ExpressionNode(name = ctx.getText(), node = result)
  }
}
