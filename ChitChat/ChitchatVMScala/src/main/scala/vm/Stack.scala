package vm

import scala.collection.mutable.ListBuffer

class Stack {

  // http://stackoverflow.com/questions/9542126/scala-is-a-string-parseable-as-a-double
  case class ParseOp[T](op: String => T)
  implicit val popDouble = ParseOp[Double](_.toDouble)
  implicit val popInt = ParseOp[Int](_.toInt)
  implicit val popBoolean = ParseOp[Boolean](_.toBoolean)
  def parse[T: ParseOp](s: String) = try { Some(implicitly[ParseOp[T]].op(s)) }
  catch {case _ : Throwable => None}

  var sp = 0
  var bp = 0

  val stack = ListBuffer[Any]()

  /**
    * the code has "command param1 ..." format
    * this function interprets the params and call push
    * to store the value with proper type
    *
    * @param value
    */
  def pushFromParameter(value:String) = {
    def parseValue(value:String) = {
      if (parse[Int](value).isDefined) parse[Int](value).get
      else if (parse[Boolean](value).isDefined) parse[Boolean](value).get
      else if (parse[Double](value).isDefined) parse[Double](value).get
      else value
    }
    push(parseValue(value))
  }

  def push(value:Any) = {
    sp += 1

    // expand the ListBuffer size
    if (stack.length < sp) {
      stack ++= List.fill(sp - stack.length)(0)
    }
    stack(sp - 1) = value
  }

  def pop() = {
    if (sp <= 0) throw new RuntimeException(s"Stack empty - not able to pop")
    sp -= 1
    stack(sp)
    stack.remove(sp)
  }

  def peek() = {
    val value = pop()
    push(value)
    value
  }

  def tos = {
    if (sp > 0) stack(sp - 1)
    else null
  }

  def getBinaryIntValues = {
    val val1:Int = pop().asInstanceOf[Int]
    val val2:Int = pop().asInstanceOf[Int]
    (val1, val2)
  }

  def getBinaryDoubleValues = {
    val val1:Double = pop().asInstanceOf[Double]
    val val2:Double = pop().asInstanceOf[Double]
    (val1, val2)
  }
}
