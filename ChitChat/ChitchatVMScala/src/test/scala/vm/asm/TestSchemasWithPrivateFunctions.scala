package vm.asm

import api.API
import file.Assembler
import org.scalatest.FunSuite
import vm.ChitchatVM

class TestSchemasWithPrivateFunctions extends FunSuite {

  val testsourcesDir = "./src/test/resources/schema_example_for_system_functions/"

  test ("simple") {
    val simpleJson =
      """|{
         |  "a": "James",
         |  "b": "John",
         |  "c": "hello"
         |}""".stripMargin

    val fbf = API.create_fbf_summary(simpleJson, Q = 4)
    val r = Assembler(testsourcesDir + "simple.asm")
    val code = r.assemble()

    val vm = new ChitchatVM(fbf)
    val res = vm.eval(code, null)
    val expected = """Map(b -> John, a -> James, c -> hello)"""
    assert(res.toString == expected)
  }

  test ("classic test - or") {
    // (name , event |advertisement , time ?)
    val case1 =
     """|{
        |  "name": "X",
        |  "a": "James",
        |  "b": "Lets see",
        |  "c": "why",
        |  "d": "Hello"
        |}""".stripMargin
    "".stripMargin
    val fbfcase1 = API.create_fbf_summary(case1, Q = 4)

    val r = Assembler(testsourcesDir + "classic_or.asm")
    val code = r.assemble()

    var vm = new ChitchatVM(fbfcase1)
    var res = vm.eval(code, null)
    assert(res.toString == "Map(a -> James, name -> X)")

    val case2 =
     """|{
        |  "name": "X",
        |  "b": "Lets see",
        |  "c": "why",
        |  "d": "Hello"
        |}""".stripMargin
    "".stripMargin
    val fbfcase2 = API.create_fbf_summary(case2, Q = 4)
    vm = new ChitchatVM(fbfcase2)
    res = vm.eval(code, null)
    assert(res.toString == "Map(b -> Lets see, name -> X)")

    val case3 =
     """|{
        |  "name": "X",
        |  "c": "why",
        |  "d": "Hello"
        |}""".stripMargin
    "".stripMargin
    val fbfcase3 = API.create_fbf_summary(case3, Q = 4)
    vm = new ChitchatVM(fbfcase3)
    res = vm.eval(code, null)
    assert(res.toString == "Map(name -> X, c -> why)")
  }

  test ("classic test - or - there is nothing matched") {
    val case4 =
     """|{
        |  "name": "X",
        |  "e": "Hello"
        |}""".stripMargin
    "".stripMargin
    val fbfcase4 = API.create_fbf_summary(case4, Q = 4)
    val r = Assembler(testsourcesDir + "classic_or.asm")
    val code = r.assemble()

    val vm = new ChitchatVM(fbfcase4)
    val res = vm.eval(code, null)
    assert(res == false)
  }


  test ("classic test - or (a, b?) | c") {
    // (name , event |advertisement , time ?)
    val case1 =
      """|{
        |  "a": "James",
        |  "b": "Lets see",
        |  "c": "why"
        |}""".stripMargin
    "".stripMargin
    val fbfcase1 = API.create_fbf_summary(case1, Q = 4)

    val r = Assembler(testsourcesDir + "classic_or_function_call.asm")
    val code = r.assemble()

    var vm = new ChitchatVM(fbfcase1)
    var res = vm.eval(code, null)
    assert(res.toString == "Map(c -> why)")
  }

  test ("classic test - or (a, b?) | c - but no c") {
    // (name , event |advertisement , time ?)
    val case1 =
      """|{
        |  "a": "James",
        |  "b": "Lets see",
        |  "d": "why"
        |}""".stripMargin
    "".stripMargin
    val fbfcase1 = API.create_fbf_summary(case1, Q = 4)

    val r = Assembler(testsourcesDir + "classic_or_function_call.asm")
    val code = r.assemble()

    var vm = new ChitchatVM(fbfcase1)
    var res = vm.eval(code, null)
    //println(res)
    assert(res.toString == "Map(b -> Lets see, a -> James)")
  }

  test ("classic test - option") {
    // (name , time ?)
    val case1 =
     """|{
        |  "name": "James",
        |  "time": [10, 11]
        |}""".stripMargin

    val fbfcase1 = API.create_fbf_summary(case1, Q = 4)

    val r = Assembler(testsourcesDir + "classic_option.asm")
    val code = r.assemble()

    var vm = new ChitchatVM(fbfcase1)
    var res = vm.eval(code, null)
    assert(res.toString == "Map(name -> James, time -> List(10, 11))")

    val case2 =
     """|{
        |  "name": "James"
        |}""".stripMargin

    val fbfcase2 = API.create_fbf_summary(case2, Q = 4)
    vm = new ChitchatVM(fbfcase2)
    res = vm.eval(code, null)
    assert(res.toString == "Map(name -> James)")
  }

  test ("classic test - repetition") {
    val case1 =
     """|{
        |  "sensor0": "x",
        |  "value0" : "100"
        |}""".stripMargin

    val fbfcase1 = API.create_fbf_summary(case1, Q = 4)

    val r = Assembler(testsourcesDir + "classic_rep.asm")
    val code = r.assemble()

    var vm = new ChitchatVM(fbfcase1)
    var res = vm.eval(code, null)
    //println(res)
    assert(res.toString == "Map(sensor0 -> x, value0 -> 100)")

    val case2 =
     """|{
        |  "sensor0": "x",
        |  "value0" : "100",
        |  "sensor1": "y",
        |  "value1" : "200"
        |}""".stripMargin

    val fbfcase2 = API.create_fbf_summary(case2, Q = 4)
    vm = new ChitchatVM(fbfcase2)
    res = vm.eval(code, null)
    //println(res)
    assert(res.toString == "Map(sensor1 -> y, value1 -> 200, sensor0 -> x, value0 -> 100)")
  }
}