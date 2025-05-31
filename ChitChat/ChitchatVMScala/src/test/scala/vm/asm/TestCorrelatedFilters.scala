package vm.asm

import api.API
import file.Assembler
import org.scalatest.FunSuite
import vm.ChitchatVM

class TestCorrelatedFilters extends FunSuite {
  val simpleJson =
    """|{
       |  "string": "James",
       |  "age": 10,
       |  "longitude": [11,12,13,14],
       |  "latitude": [1,2,3,4],
       |  "date": [10,3,17],
       |  "time": [12,14]
       |}""".stripMargin

  val testsourcesDir = "./src/test/resources/filter_example/"
  val fbf = API.create_fbf_summary(simpleJson, Q = 4)

  test("correlated test") {
    val r = Assembler(testsourcesDir + "correlated_correct.asm")
    val code = r.assemble()

    val vm = new ChitchatVM(fbf)
    val res = vm.eval(code, null)
    assert(res == true)
  }
  test("correlated wrong test") {
    val r = Assembler(testsourcesDir + "correlated_wrong.asm")
    val code = r.assemble()

    val vm = new ChitchatVM(fbf)
    val res = vm.eval(code, null)
    assert(res == false)
  }

  test("correlated function test") {
    val e1 =
      """|{
        |  "producename": "apple",
        |  "price_i": 500
        |}""".stripMargin
    val fbf = API.create_fbf_summary(e1, Q = 4)
    val r = Assembler(testsourcesDir + "correlated_function.asm")
    val code = r.assemble()

    val vm = new ChitchatVM(fbf)
    val res = vm.eval(code, null)
    assert(res == true)
  }
}
