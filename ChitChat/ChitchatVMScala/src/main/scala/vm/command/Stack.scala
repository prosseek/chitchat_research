package vm.command

import vm.Machine

trait Stack {
  def dup(cmd:Seq[String], registers:Machine) = {
    val stack = registers.stack
    val b = stack.pop()
    stack.push(b)
    stack.push(b)
  }

  def swap(cmd:Seq[String], registers:Machine) = {
    val stack = registers.stack
    val t = stack.pop()
    val b = stack.pop()
    stack.push(t)
    stack.push(b)
  }

  def push(cmd:Seq[String], registers:Machine) = {
    val stack = registers.stack
    // in encoding, the value should only be intgers
    if (cmd(1).contains(":")) {
      val result = cmd(1).split(":").map(_.trim).map(_.toInt).toList
      stack.push(result)
    }
    else
      stack.pushFromParameter(registers.registerValueToString(cmd(1)))
  }
  def pop(cmd:Seq[String], registers:Machine) = {
    val stack = registers.stack
    val res = stack.pop()
    if (cmd.length >= 2) {
      registers.storeToRegister(cmd(1), res)
    }
  }
  def loadStore(cmd:Seq[String], registers:Machine) = {
    val command = cmd(0)
    val register_value = registers.registerValueToString(cmd(1))
    var address = register_value.toInt
    val stack = registers.stack

    // ex) load bp - 3
    if (cmd.length == 4) {
      val operator = cmd(2)
      val offset = registers.registerValueToString(cmd(3))

      operator match {
        case "+" => address += offset.toInt
        case "-" => address -= offset.toInt
        case _ => throw new RuntimeException(s"only +/- operator allowed not ${operator}")
      }
    }
    if (command == "store") {
      val value = stack.pop()
      stack.stack(address) = value
    }
    else {
      val value = stack.stack(address)
      stack.push(value)
    }
  }
}
