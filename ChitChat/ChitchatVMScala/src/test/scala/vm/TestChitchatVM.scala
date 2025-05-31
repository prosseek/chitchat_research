package vm

import org.scalatest.FunSuite

class TestChitchatVM extends FunSuite {

  test("test split") {
    val vm = new ChitchatVM

    assert(vm.split("print   A B C ").toString == "List(print, A, B, C)")
    assert(vm.split("print \"Hello, world?? good?\"").toString == "List(print, Hello, world?? good?)")
  }

  test("test split for list") {
    val vm = new ChitchatVM

    assert(vm.split("print [1,2,3,4]").toString == "List(print, 1:2:3:4)")
  }

}
