package core

import grapevineType.BottomType
import org.scalatest._

/**
 * Created by smcho on 8/10/14.
 */
class TestLabeledSummary extends FunSuite with BeforeAndAfter {
  var t: LabeledSummary = _
  var t2: LabeledSummary = _

  val filePath = "contextSummary/src/test/scala/resource/unittest.json"
  val m = Map[String, Any]("number of apples"->10, "age of kids"->4, "speed of a car"->14, "latitude"->(32, 22, 44, 33), "date"->(2014,10,1), "time"->(11,11))

  before {
    t = LabeledSummary(m)
    t2 = LabeledSummary(filePath)
  }
//  test ("Get size test") {
//    val totalItem = m.size
//    val keySize = (0 /: m.keys) {(acc, value) => acc + value.size}
//    val valueSize = 2 + 2 + ("test".size + 1)
//    assert(t.getSizes()._1 == keySize + valueSize)
//  }

  test ("test toString") {
    val expected = """{"type":"l", "size":80, "jsonSize":144, "jsonCompSize":117}"""
    assert(t.repr() == expected)

    val expected2 = """{"type":"l", "size":52, "jsonSize":105, "jsonCompSize":85}"""
    assert(t2.repr() == expected2)
  }
}
