package vm.asm

import api.API
import file.Assembler
import org.scalatest.FunSuite
import vm.ChitchatVM

class TestSituationalFilters extends FunSuite
{
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

  test("situational filter near_citypark test") {
    val r = Assembler(testsourcesDir + "situational_near_citypark.asm")
    val code = r.assemble()

    val vm = new ChitchatVM(fbf)
    val res = vm.eval(code, null)
    assert(res == false)
  }
  test("situational filter partytime test") {
    val r = Assembler(testsourcesDir + "situational_partytime.asm")
    val code = r.assemble()

    val vm = new ChitchatVM(fbf)
    val res = vm.eval(code, null)
    assert(res == false)
  }
}
