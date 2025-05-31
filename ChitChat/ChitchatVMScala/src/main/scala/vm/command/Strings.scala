package vm.command

import vm.Machine

trait Strings {
  implicit class Regex(sc: StringContext) {
    def r = new scala.util.matching.Regex(sc.parts.mkString, sc.parts.tail.map(_ => "x"): _*)
  }

  /**
    * Returns current location, the whereami file should be installed
    *
    * @return
    */
  def concat(cmd:Seq[String], registers: Machine) = {
    val stack = registers.stack
    val pop2 = stack.pop().toString
    val pop1 = stack.pop().toString

    stack.push(pop1 + pop2)
  }
  def isstring(cmd:Seq[String], registers: Machine) = {
    val stack = registers.stack
    val pop = stack.pop().toString

    pop match {
      case r"[_a-zA-Z][_a-zA-Z0-9]*" => stack.push(true)
      case _ => stack.push(false)
    }
  }
}
