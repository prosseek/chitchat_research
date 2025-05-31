package node

import org.scalatest.FunSuite

class TestFunctionNode extends FunSuite {

  val prognode = NodeGenerator.get("./resources/unittest_example/function_simple.txt")
  val bs = prognode.getNode[FunctionNode]("priceMatch", prognode.functions).get

  test ("simple") {

    assert(bs.params.size == 2)
    assert(bs.id.name == "priceMatch")

    // function bool priceMatch(produceName, price)
    assert(bs.params(0) == "produceName")
    assert(bs.params(1) == "price")
    assert(bs.return_type == "bool")
  }

  test("code gen") {
    val res = bs.codeGen(prognode)
    println(res)
  }
}