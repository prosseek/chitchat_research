package core

import grapevineType.BottomType
import org.scalatest.{BeforeAndAfter, FunSuite}

/**
 * Created by smcho on 1/5/15.
 */
class TestCompleteSummary extends FunSuite with BeforeAndAfter {
  val filePath = "contextSummary/src/test/scala/resource/unittest.json"
  val m = Map[String, Any]("number of apples"->10, "age of kids"->4, "speed of a car"->14, "latitude"->(32, 22, 44, 33), "date"->(2014,10,1), "time"->(11,11))
  var c: CompleteSummary = _
  var c2: CompleteSummary = _

  before {
    c = CompleteSummary(m)
    c2 = CompleteSummary(filePath)
  }

  test("test size") {
    assert(c.getSize() == 16)
    assert(c2.getSize() == 24)
  }

  test("test repr") {
    val expect = """{"type":"c", "size":16, "jsonSize":144, "jsonCompSize":117}"""
    val expect2 = """{"type":"c", "size":24, "jsonSize":105, "jsonCompSize":85}"""
    assert(c.repr() == expect)
    assert(c2.repr() == expect2)
  }
}
