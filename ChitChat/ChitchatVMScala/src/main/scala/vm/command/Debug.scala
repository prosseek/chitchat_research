package vm.command

import vm.Machine

trait Debug {
  def debug(cmd:Seq[String], registers: Machine) = {
    val stack = registers.stack
    println("hit debug0")
  }
  def debug1(cmd:Seq[String], registers: Machine) = {
    val stack = registers.stack
    println("hit debug1")
  }
  def debug2(cmd:Seq[String], registers: Machine) = {
    val stack = registers.stack
    println("hit debug2")
  }
  def debug3(cmd:Seq[String], registers: Machine) = {
    val stack = registers.stack
    println("hit debug3")
  }
}
