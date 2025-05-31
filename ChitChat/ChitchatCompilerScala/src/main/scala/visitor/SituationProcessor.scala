package visitor

import node.{ExpressionNode, IdNode, ParamsNode, SituationNode}
import org.antlr.v4.runtime.ParserRuleContext
import parser.ChitchatParser.SituationContext

trait SituationProcessor {
  /**
    *
    * ==== Grammar ====
    * {{{
    *   situation: SITUATION id parenparams? '=' constraints ;
    *   parenparams: '(' params ')' ;
    *   params: (primary_expresion ','?)* ;
    *   constraints: absolute_constraint | range_constraint ;
    *   absolute_constraint: '|' id '-' id '|' comparison_operator unit_value  ;
    *   range_constraint: unit_value comparison_operator id comparison_operator unit_value ;
    * }}}
    *
    * @param ctx the parse tree
    *     */
  // def process(ctx:SituationContext, o:ChitchatVisitor) : SituationNode = {
  def process(ctx:SituationContext, o:ChitchatVisitor) : SituationNode = {
    val name = ctx.getText()
    val id = o.visit(ctx.id()).asInstanceOf[IdNode]
    val ps = o.visit(ctx.params()).asInstanceOf[ParamsNode]
    val expression = o.visit(ctx.expression()).asInstanceOf[ExpressionNode]
    SituationNode(name = name, id = id, params = ps, expression = expression)
  }
}
