package vm

import summary.Summary

class ChitchatVM(val summary:Summary = null)
            extends command.Macro
            with command.Stack
            with command.FunctionCall
            with command.Jump
            with command.Expression
            with command.ATN
            with command.Strings
            with command.Debug
            with command.System {
  // stack
  val stack = new Stack()
  val summaryMap = collection.mutable.Map[String, Any]()
  val registers = new Machine(stack=stack, summaryMap = summaryMap)

  def process(cmd: Seq[String]) = {
    cmd(0) match {
      // stack command
      case "swap" => swap(cmd, registers)
      case "dup" => dup(cmd, registers)
      case "push" => push(cmd, registers)
      case "pop" => pop(cmd, registers)
      case x if (x == "load" || x == "store") => loadStore(cmd = cmd, registers = registers)
      // macro level
      // todo: Everything now is integer version, for float version
      // we need to make the same implementation with different type (double)
      case "inrange" => inrange(cmd=cmd, registers=registers)
      case "here" => here(registers)
      // function_call 123 "p1" "p2" "p3" <- 123 is the location of a function
      case x if (x == "f" || x == "function_call") => function_call(cmd, registers)
      case x if (x == "function_call_stack" || x == "f2") => function_call_stack(cmd, registers)
      // return 5 <- number of params
      case x if (x == "return" || x == "r")  => registers.ip = return_from_function(cmd = cmd, registers = registers)
      // all elements exists in summary
      case x if (x == "allexists" || x == "a") => allexists(cmd = cmd, summary = summary, registers = registers)

      // summary
      case "read" => read(cmd, registers, summary)
      // control
      // unconditional jump
      case "jmp" => jmp(cmd, registers)
      // load from stack and jump if it is false
      case x if (x == "jfalse" || x == "jtrue") => jtruefalse(cmd, registers)
      case x if (x == "jpeekfalse" || x == "jpf" || x == "jpeektrue" || x == "jpt") => jpeektruefalse(cmd, registers)
      case x if (x == "abs" || x == "distance") => distance(cmd = cmd, registers = registers)
      // and 3 => all of the 3 values in the stack should be "true"
      case x if (x == "and" || x == "or") => andOr(cmd, registers)
      case "cmp" => cmp(cmd, registers)

      // string
      case "concat" => concat(cmd, registers)
      case "isstring" => isstring(cmd, registers)
      // Work as integer
      // X (val2) < Y (val1)
      case x if (x == "less" || x == "leq" || x == "greater" || x == "geq") => icmp(cmd, registers)
      case x if (x == "fless" || x == "fleq" || x == "fgreater" || x == "fgeq") => fcmp(cmd, registers)
      case x if (x == "iadd" || x == "isub" || x == "imul" || x == "idiv") => iarith(cmd, registers)
      case x if (x == "fadd" || x == "fsub" || x == "fmul" || x == "fdiv") => farith(cmd, registers)
      // utility - print
      case "print" => {
        println(registers.registerValueToString(cmd(1)))
      }
      // ATN
      case "push_summary" => push_summary(cmd, registers)
      case "register" => register(cmd, registers)

      // DEBUGGING
      case "debug"  => debug(cmd, registers)
      case "debug1" => debug1(cmd, registers)
      case "debug2" => debug2(cmd, registers)
      case "debug3" => debug3(cmd, registers)
    }
    registers.ip += 1 // next command including the jmp command
  }

  def evalCommand(command:String, summary:Summary) = {
    val e = split(command)
    process(e)
  }

  /**
    * Run the commands in code sequence.
    * It stops when
    *  1. the command is "stop"
    *  2. the ip points outside the code sequence.
    *
    * @param code
    * @param summary2
    * @return
    */
  def eval(code:Seq[String], summary2:Summary = null) = {
    // initial condition
    registers.ip = 0
    var proceed = true

    // make progress5
    while (proceed) {
      if (registers.ip >= code.length)
        proceed = false
      else {
        val c = code(registers.ip)
        if (c.startsWith("stop"))
          proceed = false
        else evalCommand(c, if (summary2 == null) summary else summary2)
      }
    }
    stack.tos
  }
  /**
    * breaks down the input string
    *  1. When the input has string, it keeps the string
    *  2. Otherwise, split the input by the spaces
    *
    * ==== Example ====
    * {{{
    *   (A) (B) means the input is sepparated into A/B
    *   print [a, b, c, d] -> (print) (a:b:c:d)
    *   print "hello, world" -> (print) (hello, world)
    *   mov a b c -> (mov)(a)(b)(c)
    * }}}
    *
    * @param code
    */
  def split(code:String): List[String] = {

    // 1. find the command
    val splittedCode = code.trim.split("\\s+").toList
    val command = splittedCode(0)

    if (splittedCode.size <= 1) {
      return splittedCode
    }

    // when there are more than two inputs
    // 2. check if this is a string
    val params = code.replace(command, "").trim

    if (params.startsWith("\"")) {
      // string format
      return List(command, params.replaceAll("\"", ""))
    }
    else if (params.startsWith("[")) {
      val step1 = params.replace("[","").replace("]","")
      val result = step1.split(",").toList.mkString(":")
      return List(command, result)
    }
    else {
      return code.split("\\s+").toList
    }
  }
}
