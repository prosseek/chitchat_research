package vm.command

import vm.Machine

import scala.collection.mutable.ListBuffer

trait Expression {

  def xor(cmd:Seq[String], registers:Machine) = {
    val stack = registers.stack
    val val1 = stack.pop().asInstanceOf[Boolean]
    val val2= stack.pop().asInstanceOf[Boolean]
    stack.push(val1 ^ val2)
  }

  def not(cmd:Seq[String], registers:Machine) = {
    val stack = registers.stack
    val val1 = stack.pop().asInstanceOf[Boolean]
    stack.push(!val1)
  }

  //todo
  // The implementation is N and/or operation
  // Modify this to make only 2 input 1 output operation
  // for multiple input operation, make another/new command
  def andOr(cmd:Seq[String], registers:Machine) = {
    val command = cmd(0)
    val count = if (cmd.size < 1) 2 else cmd(1).toInt
    val result = false
    val stack = registers.stack

    val booleans = ListBuffer[Boolean]()
    for (i <- 0 until count) {
      booleans += stack.pop().asInstanceOf[Boolean]
    }
    if (command == "and")
      stack.push(booleans.forall(_ == true))
    else
      stack.push(booleans.exists(_ == true))
  }
  def cmp(cmd:Seq[String], registers:Machine) = {
    val stack = registers.stack
    val val1 = stack.pop()
    val val2= stack.pop()
    stack.push(val1 == val2)
  }
  def icmp(cmd:Seq[String], registers:Machine) = {
    val stack = registers.stack
    val val2 = stack.pop().asInstanceOf[Int]
    val val1 = stack.pop().asInstanceOf[Int]
    var result = false
    cmd(0) match {
      case "less" => if (val1 < val2) result = true
      case "leq" => if (val1 <= val2) result = true
      case "greater" => if (val1 > val2) result = true
      case "geq" => if (val1 >= val2) result = true
    }
    stack.push(result)
  }
  def fcmp(cmd:Seq[String], registers:Machine) = {
    val stack = registers.stack
    val val2 = stack.pop().asInstanceOf[Double]
    val val1= stack.pop().asInstanceOf[Double]
    var result = false
    cmd(0) match  {
      case "fless"    => if (val1 < val2) result = true
      case "fleq"     => if (val1 <= val2) result = true
      case "fgreater" => if (val1 > val2) result = true
      case "fgeq"     => if (val1 >= val2) result = true
    }
    stack.push(result)
  }
  def iarith(cmd:Seq[String], registers:Machine) = {
    val stack = registers.stack
    val (val1, val2) = stack.getBinaryIntValues
    cmd(0) match {
      case "iadd" => stack.push(val1 + val2)
      case "isub" => stack.push(val1 - val2)
      case "imul" => stack.push(val1 * val2)
      case "idiv" => {
        if (val2 == 0) throw new RuntimeException(s"Divide by zero error")
        stack.push(val1 / val2)
      }
    }
  }
  def farith(cmd:Seq[String], registers:Machine) = {
    val stack = registers.stack
    val (val1, val2) = stack.getBinaryDoubleValues
    cmd(0) match {
      case "fadd" => stack.push(val1 + val2)
      case "fsub" => stack.push(val1 - val2)
      case "fmul" => stack.push(val1 * val2)
      case "fdiv" => {
        if (val2 == 0.0) throw new RuntimeException(s"Divide by zero error")
        stack.push(val1 / val2)
      }
    }
  }
}
