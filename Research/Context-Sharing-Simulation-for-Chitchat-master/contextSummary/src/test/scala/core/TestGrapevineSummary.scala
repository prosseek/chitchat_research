package core

import grapevineType.BottomType._
import grapevineType.ByteType
import org.scalatest._


/**
 * Created by smcho on 8/10/14.
 */

class TestGrapevineSummary extends FunSuite with BeforeAndAfter  {
  var t: GrapevineSummary = _
  var t2: GrapevineSummary = _
  val m = Map[String, Any]("number of apples"->10, "age of kids"->4, "speed of a car"->14, "latitude"->(32, 22, 44, 33), "date"->(2014,10,1), "time"->(11,11))

  before {
    t = GrapevineSummary(m)
    val filePath = "contextSummary/src/test/scala/resource/unittest.json"
    t2 = GrapevineSummary(filePath)
  }

  test("test serialize") {
    assert(t2.serialize().length == 52)
  }

  test ("test toString") {
    val result =
      """date => (2014,10,1): DateType
        |speed of a car => 14: SpeedType
        |latitude => (32,22,44,33): LatitudeType
        |number of apples => 10: ByteType
        |age of kids => 4: AgeType
        |time => (11,11): TimeType
        |""".stripMargin
    assert(t.toString() == result)
  }

  test ("test size") {
    assert(t.getSizes() == (68,80,80))
    assert(t.getSize() == 80)

    // "contextSummary/src/test/scala/resource/unittest.json"
    println(t2.getSizes() == (44,52,52))
    assert(t2.getSize() == 52)
  }

  test ("Test contains") {
    assert(t.contains("age of kids"))
    assert(!t.contains("hello"))
  }

  test ("Test set") {
    t.set("age of kids", ByteType(4))
    assert(t.get("age of kids") == 4)
    t.set("x", ByteType(14))
    assert(t.get("x") == 14)
  }

  test ("Test set2") {
    t.set("age of kids", classOf[ByteType], 4)
    assert(t.get("age of kids") == 4)
  }

  test ("Test get") {
    assert(t.get("number of apples") == m("number of apples"))
    assert(t.get("age of kids") == m("age of kids"))
    assert(t.get("speed of a car") == m("speed of a car"))
    assert(t.get("latitude") == m("latitude"))
    assert(t.get("date") == m("date"))
    assert(t.get("time") == m("time"))
    assert(t.get("latitude of the world") == null)
  }

  test ("Test create from key") {
    //    "age" -> classOf[AgeType],
    //    "speed" -> classOf[SpeedType],
    //    "number" -> classOf[ByteType],
    //    "latitude" -> classOf[LatitudeType],
    //    "longitude" -> classOf[LongitudeType],
    //    "date" -> classOf[DateType],
    //    "time" -> classOf[TimeType]

    // getValue returns the Grapevine type data
    // get of Grapevine type data returns the data object
    assert(t.getValue("number of apples").get == m("number of apples"))
    assert(t.getValue("age of kids").get == m("age of kids"))
    assert(t.getValue("speed of a car").get == m("speed of a car"))
    assert(t.getValue("latitude").get == m("latitude"))
    assert(t.getValue("date").get == m("date"))
    assert(t.getValue("time").get == m("time"))
    assert(t.getValue("latitude of the world").isEmpty)
  }

  test ("Test create from value") {
    val m = Map[String, Any]("A count"->10, "B_f"->20.5, "C"->"Hello")
    t = GrapevineSummary(m)

    assert(t.getValue("A count").get == m("A count"))
    assert(t.getValue("B_f").get == m("B_f"))
    assert(t.getValue("C").get == m("C"))
    assert(t.getValue("D").isEmpty)
  }

  test("test load") {
    t.load("contextSummary/src/test/scala/resource/sample_context.json")
    assert(t.get("abc") == "Hello, world")
  }
}
