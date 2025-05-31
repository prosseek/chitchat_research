package visitor

import parser.ChitchatBaseVisitor
import parser.ChitchatParser._
import node._

class ChitchatVisitor extends ChitchatBaseVisitor[Node]
  with TypedefProcessor
  with CorrelationProcessor
  with ExpressionProcessor
  with ExpressionsProcessor
  with SituationProcessor
  with SchemaProcessor
  with FunctionProcessor
  with CommandProcessor
  with Function_callProcessor
  with BlockProcessor
  with ValueProcessor
  with ListProcessor
  with ArgsProcessor
  with ParamsProcessor
  with ValuedefProcessor
  with Constant_unitProcessor
  with AbsoluteProcessor
  with SchemeProcessor
  with RepProcessor
  with ChooseProcessor
{
  var prognode: ProgNode = _

  /** Processes defintions, and return a set of nodes
    * {{{
    *   prog: (typedef | correlation | situation | ... )+ ;
    * }}}
    *
    * @param ctx the parse tree
    *
    */
  override  def visitProg(ctx: ProgContext) = {
    prognode = new ProgNode()

    /* ctx has corresponding typedef(), correlation(), ...
       which can be null (when there is no input matching) or corresponding ctx object
       in this example, we iterate over the children to retrieve the item as an object
       and visit them one by one with a visitor.
     */
    val it = ctx.children.iterator()
    while (it.hasNext) {
      val item = it.next()
      val res: Node = visit(item)
      if (res == null)
        throw new RuntimeException(s"Null point returned - wrong element in the source code")
      prognode.add(res)
    }
    prognode
  }

  // prog's children visitors
  override def visitTypedef(ctx: TypedefContext) : TypedefNode = process(ctx, this)
  override def visitCorrelation(ctx: CorrelationContext) : CorrelationNode = process(ctx, this)
  override def visitSituation(ctx: SituationContext) : SituationNode = process(ctx, this)
  override def visitSchema(ctx: SchemaContext) : SchemaNode = process(ctx, this)
  override def visitFunction(ctx: FunctionContext) : FunctionNode = process(ctx, this)
  override def visitCommand(ctx: CommandContext) : CommandNode = process(ctx, this)

  override def visitAssignment(ctx: AssignmentContext) : AssignmentNode =
    AssignmentNode(name = ctx.getText(), id = visit(ctx.id()).asInstanceOf[IdNode],
      expression = visit(ctx.expression()).asInstanceOf[ExpressionNode])
  //override def visitComparison(ctx: ComparisonContext) : ComparisonNode = process(ctx, this)
  override def visitFunction_call(ctx:Function_callContext) : Function_callNode = process(ctx, this)
  override def visitList(ctx:ListContext) : ListNode = process(ctx, this)

  override def visitId(ctx:IdContext) : IdNode = IdNode.make(name = ctx.getText())

  override def visitExpressions(ctx: ExpressionsContext) : ExpressionsNode = process(ctx, this)
  override def visitExpression(ctx: ExpressionContext) : ExpressionNode = process(ctx, this)
  override def visitValue(ctx:ValueContext) : ValueNode = process(ctx, this)

  override def visitParams(ctx:ParamsContext) : ParamsNode = process(ctx, this)
  override def visitArgs(ctx:ArgsContext) : ArgsNode = process(ctx, this)

  override def visitBlock(ctx:BlockContext) : BlockNode = process(ctx, this)
  override def visitValuedef(ctx:ValuedefContext) : ValuedefNode = process(ctx, this)
  override def visitConstant(ctx:ConstantContext) : ConstantNode = ConstantNode(name = ctx.getText())
  override def visitConstant_unit(ctx:Constant_unitContext) : Constant_unitNode = process(ctx, this)
  override def visitAbsolute(ctx:AbsoluteContext) : AbsoluteNode = process(ctx, this)

  override def visitScheme(ctx:SchemeContext) : SchemeNode = process(ctx, this)
  override def visitRep(ctx:RepContext) : RepNode = process(ctx, this)
  override def visitChoose(ctx:ChooseContext) : ChooseNode = process(ctx, this)
}
