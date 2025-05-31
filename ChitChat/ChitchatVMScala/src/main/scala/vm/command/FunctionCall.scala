package vm.command

import vm.Machine

import scala.collection.mutable.ListBuffer

trait FunctionCall {
  def link(stack:vm.Stack) = {
    stack.push(stack.bp)
    stack.bp = (stack.sp - 1) // TOS is sp - 1, and it's also bp
  }

  /**
    * Invoke function in cmd(1) with parameters from a parameter
    *
    * @param cmd
    * @param registers
    */
  def function_call(cmd:Seq[String], registers:Machine) = {
    val interpreted = registers.registerValueToString(cmd(1))
    val function_location = interpreted.toInt
    val params = cmd.slice(2, cmd.size)
    val stack = registers.stack

    params foreach {
      p => stack.pushFromParameter(registers.registerValueToString(p))
    }

    val newCommand = List(cmd(0).toString, interpreted, params.length.toString)
    function_call_stack(newCommand, registers)
  }

  /**
    * Invoke function in cmd(1) with parameters in a stack
    *
    * @param cmd
    * @param registers
    */
  def function_call_stack(cmd:Seq[String], registers:Machine) = {
    val function_location = cmd(1).toInt

    val iterpreted = registers.registerValueToString(cmd(2))
    val param_count = iterpreted.toInt
    val stack = registers.stack

    // get all the parameters from stack
    val params = ListBuffer[String]()
    for (i <- 0 until param_count) {
      params += stack.pop().toString()
    }
    // We need to insert the return value before all the parameters
    // 1. reserve return value
    stack.push(0)
    // 2. push the parameters
    params.reverse foreach {
      p => stack.pushFromParameter(registers.registerValueToString(p))
    }
    // 3. link
    link(stack)
    // 4. push next ip
    stack.push(registers.ip + 1)
    // 5. jmp to the location
    registers.ip = function_location - 1 // later 1 is added
  }

  def return_from_function(cmd:Seq[String], registers:Machine) = {
    val stack = registers.stack
    val interpreted = registers.registerValueToString(cmd(1))

    val number_of_params = interpreted.toInt

    // 1. copy the return value in temp to the RV
    val rv = stack.bp - (number_of_params + 1)
    stack.stack(rv) = stack.pop
    // 2. get return address
    val return_address = stack.pop.asInstanceOf[Int]
    // 3. retore bp
    stack.bp = stack.pop().asInstanceOf[Int]
    // 4. pop number_of_params times
    for (i <- 0 until number_of_params)
      stack.pop()
    return_address - 1
  }
}
