package core

import org.scalatest.{BeforeAndAfter, FunSuite}
import scala.collection.BitSet

/**
 * Created by smcho on 7/4/14.
 */
class TestTables extends FunSuite with BeforeAndAfter {

  var tbls: Tables = _

  before {
    tbls = Tables(List(3), List(3),0)
  }

  ignore("debug print") {
    val tbls = new Tables(List(10,5,3), List(3,2,2),0)
    println(tbls.debug())
  }

  //
  ignore ("Simple") {
    //val tbls = Tables()
  }
  ignore ("Check membership") {
    val bs = BitSet(10, 20, 30)
    var points = List(10,20)
    assert(Tables.checkMembership(bs, points))

    points = List(10,20,40)
    assert(Tables.checkMembership(bs, points) == false)
  }
  ignore ("Check m/k setup and size retrieval") {
    val tbls = Tables(m=List(10,5,4,3), keys=List(3,2,2,2), 0)
    assert(tbls.getM(0) == 10)
    assert(tbls.getM(1) == 5)
    assert(tbls.getM(2) == 4)
    assert(tbls.getM(3) == 3)
    assert(tbls.getM(100) == 3)

    assert(tbls.getK(0) == 3)
    assert(tbls.getK(1) == 2)
    assert(tbls.getK(2) == 2)
    assert(tbls.getK(3) == 2)
    assert(tbls.getK(100) == 2)
  }

  ignore("get test level 0") {
    tbls.set(bit = 0, level = 0, key="Hello")
    // there is one element, so the result should be clear
    assert(tbls.get(level = 0, key="Hello") == (false, true))
    tbls.set(bit = 1, level = 0, key="HelloWorld")
    // there is one element, so the result should be clear
    assert(tbls.get(level = 0, key="HelloWorld") == (true, false))
  }

  test("Set tests") {
    tbls.set(bit = 0, level = 5, key="Hello")
    tbls.debug()
    assert(tbls.get(5, key = "Hello") == (false, true))
  }
}
