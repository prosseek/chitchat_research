package vm.command

import java.nio.file.{Files, Paths}

import vm.Machine

import sys.process._

trait System {
  /**
    * Returns current location, the whereami file should be installed
 *
    * @return
    */
  def here(registers: Machine) = {
    val stack = registers.stack
    val (latitude, longitude) = vm.System.here()
    stack.push(longitude)
    stack.push(latitude)
  }

  def now(registers: Machine) = {
    val stack = registers.stack
    val result = vm.System.now().reverse
    // stack.push(result(0)) // sec
    stack.push(List(result(2), result(1))) // hour, minute
    stack.push(List(result(5) - 2000, result(4), result(3))) // year, month, day
  }
}
