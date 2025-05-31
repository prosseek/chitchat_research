package node.codegen

import node._
import org.scalatest.FunSuite

class TestTypedefGen extends FunSuite
{
  val prognode = NodeGenerator.get("./resources/unittest_example/type.txt")
  val types = prognode.typedefs.toList

  test ("find range test") {
    /*
        -type hour extends Range(size=5, min=0, max=23, signed=false)
        -type markethour extends hour(min=10, max=18)

        * From the specification
        * markethour -> hour(min=10, max=18) (this has the name) -> Range(size=5, signed=false)
        * => Range(name = "hour", min=10, max=18, size=5, signed=false)
     */
    val tg = new TypedefCodeGen(typedefNode = null, progNode = prognode)
    val result = tg.getAssignMapFromRangeName("markethour", types)
    val map1 = Map[String, String]("name" -> "markethour", "group" -> "Range",
      "min" -> "10", "max" -> "18", "size" -> "5", "signed" -> "false")
    assert(result.toList.sorted == map1.toList.sorted)

    val expected = "new Range(name = \"markethour\", size = 5, min = 10, max = 18, signed=false)"

    //println(tg.rangeMapToString(map1))
    assert(tg.rangeMapToString(map1) == expected)
  }

  test ("gen test range") {
    val node = prognode.getNode[TypedefNode](name = "markethour", nodes = prognode.typedefs).get

    var expect =
      "package chitchat.types\nclass Markethour extends Range ( name = \"markethour\", size = 5, min = 10, max = 18, signed = false )"

    assert(expect == node.codeGen(progNode = prognode))
  }

  test ("gen test float") {
    val node = prognode.getNode[TypedefNode](name = "temperature", nodes = prognode.typedefs).get
    val expect = "package chitchat.types\nclass Temperature extends Float ( name = \"temperature\", min = -50.0, max = 90.0 )"
    assert(expect == node.codeGen(progNode = prognode))
  }

  test("getContentForEncoding test") {

    // hour's min/max is updated from min = 0, max = 23
    // hour (size=5, min=10, max=18, signed=false)
    // minute (size=6, min=0, max=59, signed=false)`

    val tg = new TypedefCodeGen(typedefNode = null, progNode = prognode)
    val res = tg.getContentForEncoding("market time")
    val expected =
      """Array[Range](new Range(name = "hour", size = 5, min = 10, max = 18, signed = false),new Range(name = "minute", size = 6, min = 0, max = 59, signed = false))""".stripMargin
    //println(res)
    assert(res == expected)
  }

  test("getContentForRange test") {
    val tg = new TypedefCodeGen(typedefNode = null, progNode = prognode)
    val res = tg.getContentForRange("markethour")
    val expected = "size = 5, min = 10, max = 18, signed = false"
    assert(res == expected)
  }

  test("getContentForFloat test") {
    val tg = new TypedefCodeGen(typedefNode = null, progNode = prognode)
    val res = tg.getContentForFloat("temperature")
    val expected = "min = -50.0, max = 90.0"
    assert(res == expected)
  }

  test("getContentForString test") {
    val tg = new TypedefCodeGen(typedefNode = null, progNode = prognode)
    var res = tg.getContentForString("max10")
    assert(res == "conditions = List(\"maxlength\", 10)")
    //println(res)
    res = tg.getContentForString("only a b")
    assert(res == "range = List('a', 'b')")
    res = tg.getContentForString("event")
    assert(res == "range = List(0, 122)")
  }

  test ("gen test string max10") {
    val node = prognode.getNode[TypedefNode](name = "max10", nodes = prognode.typedefs).get

    val expect = """package chitchat.types
                   |class Max10 extends String ( name = "max10", conditions = List("maxlength", 10) )""".stripMargin
    assert(expect == node.codeGen(progNode = prognode))
  }

  test ("gen test string only a b") {
    val node = prognode.getNode[TypedefNode](name = "only a b", nodes = prognode.typedefs).get
    val expect = """package chitchat.types
                   |class Only_a_b extends String ( name = "only a b", range = List('a', 'b') )""".stripMargin
    assert(expect == node.codeGen(progNode = prognode))
  }
}
