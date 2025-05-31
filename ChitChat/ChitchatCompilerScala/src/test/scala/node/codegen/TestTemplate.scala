package node.codegen

import org.scalatest.FunSuite
import scala.collection.mutable.{Map => MMap}
class TestTemplate extends FunSuite with Template {

  test("simple") {
    val template = "#{a}"
    val map = Map[String, String]("a" -> "push $bp - 2")
    val res = getTemplateString(template, map)
    println(res)
  }

  test("simple2") {
    val e1 = "push $bp - 2"
    val e2 = "push \"apple\""
    val map = MMap[String, String]()
    map("e1") = e1
    map("e2") = e2
    map("op") = "XOR"
    val template =
      s"""#{e1}
          |#{e2}
          |#{op}
      """.stripMargin
    val res = getTemplateString(template, map.toMap)
    println(res)
  }
}
