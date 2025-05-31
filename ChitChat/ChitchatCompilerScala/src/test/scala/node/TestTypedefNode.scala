package node

import org.scalatest.FunSuite

class TestTypedefNode extends FunSuite {

  /**
    * +type hello extends Range(min=-10, max=10, size=5, signed=true)
    */
  test("simple") {
    val prognode = NodeGenerator.get("./resources/unittest_example/type_simple.txt")
    val a = prognode.getNode[TypedefNode]("hello", prognode.typedefs).get
    assert(a.name == "+typehelloextendsRange(min=-10,max=10,size=5,signed=true)")
    assert(a.id.name == "hello")
    assert(a.assignments.size == 4)
    assert(a.assignments(0).name == "min=-10")
    assert(a.assignments(1).name == "max=10")
    assert(a.assignments(2).name == "size=5")
    assert(a.assignments(3).name == "signed=true")
    assert(a.assignments(0).id.name == "min")
    assert(a.assignments(0).expression.name == "-10")

    assert(a.values.size == 0)
    assert(a.function_call == null)
  }

  /**
    * +type time extends Encoding(hour, minute)
    */
  test("simple2") {
    val prognode = NodeGenerator.get("./resources/unittest_example/type_simple2.txt")
    val a = prognode.getNode[TypedefNode]("time", prognode.typedefs).get
    assert(a.id.name == "time")
    assert(a.assignments.size == 0)
    assert(a.values.size == 2)
    assert(a.function_call == null)
    assert(a.values(0).name == "hour")
    assert(a.values(1).name == "minute")
  }

  /**
    * +type max10 extends String(maxlength(10))
    */
  test("simple3") {
    val prognode = NodeGenerator.get("./resources/unittest_example/type_simple3.txt")
    val a = prognode.getNode[TypedefNode]("max10", prognode.typedefs).get

    assert(a.name == "+typemax10extendsString(maxlength(10))")
    assert(a.id.name == "max10")
    assert(a.assignments.size == 0)
    assert(a.values.size == 0)

    val f = a.function_call
    assert(f.name == "maxlength(10)")
    assert(f.id.name == "maxlength")
    assert(f.args.values.size == 1)
    assert(f.args.values(0).name == "10")
  }

  /**
    *  +type name extends String(length < 10)
    */
  test("simple4") {
    val prognode = NodeGenerator.get("./resources/unittest_example/type_simple4.txt")
    val a = prognode.getNode[TypedefNode]("name", prognode.typedefs).get
    assert(a.id.name == "name")
    assert(a.assignments.size == 0)
    assert(a.values.size == 0)

    // length < 10
    val f = a.comparison
    assert(f.expression1.name == "length")
    assert(f.op == "<")
    assert(f.expression2.name == "10")
  }
}