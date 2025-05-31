package visitor

import parser.ChitchatParser.{CommandContext, FunctionContext}

trait CommandProcessor {
  def process(ctx:CommandContext, o:ChitchatVisitor) = {
    null
  }
}
