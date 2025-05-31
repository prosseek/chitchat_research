package core

import grapevineType.{BottomType}
import grapevineType.BottomType._
import org.scalatest.{BeforeAndAfter, FunSuite}

/**
 * Created by smcho on 8/16/14.
 */
class TestBloomierFilterSummary extends FunSuite with BeforeAndAfter {
  var message = "hello, world?"
  var t: BloomierFilterSummary = _
  var t2: BloomierFilterSummary = _

  //  {
  //    "latitude": [10, 10, 10, 10],
  //    "message": "Hello, world",
  //    "time": [11, 11],
  //    "date":[2014, 10, 1]
  //  }
  val filePath = "contextSummary/src/test/scala/resource/unittest.json"
  val m = Map[String, Any]("number of apples"->10, "age of kids"->4, "speed of a car"->14, "latitude"->(32, 22, 44, 33), "date"->(2014,10,1), "time"->(11,11))

  before {
    t = BloomierFilterSummary(m)
    t2 = BloomierFilterSummary(filePath)
  }

  test ("test initM") {
    val bf = BloomierFilterSummary(filePath)
    bf.setup(m = 10, k = 3, q = 8*5)
    assert(bf.getInitM() == 10)
    assert(bf.getM() == 10)

    bf.setup(m = 0, k = 3, q = 8*5)
    assert(bf.getInitN() == 4) // 4 items
    assert(bf.getN() == 6) // folded to make 6 items
    assert(bf.getInitM() == 6) // m = 0 -> 4*1.5 (automatic change)
    assert(bf.getM() == 7) // ultimate change

    assert(bf.get("time") == (11,11))
  }

  test ("test create from Labeled") {
    val l = LabeledSummary(filePath)
    val bf = BloomierFilterSummary(l)
    bf.setup(m = 10, k = 3, q = 8*5)
    assert(l.getSize() == 52)
    assert(bf.getSize() == 32)
  }
  test ("Size test") {
    // map1 size
    t.setup(m = 8, k = 3, q = 8*4)
    println(t.getDetailedSize())
    //println(t.getM())
    val expectedSize = t.getM()/8 + 4 * m.size
    //println(t.getSizes())
    assert(t.getSizes()._1 == expectedSize)
  }

  test ("test contains") {
    // probabilistic, but it should be OK
    t.setup(m = 6, k = 3, q = 8*4)
    assert(t.contains("number of apples"))
    assert(!t.contains("number of apples2"))

    // false positive error with floating point number
    assert(t.contains("a_f")) // It should return null, but this is false positive
  }

  test ("test Simple") {
    t.setup(m = 6, k = 3, q = 8*4)

    if (t.check("latitude") == NoError) {
      assert(t.get("latitude") == (32, 22, 44, 33))
    }
    if (t.contains("latitude")) {
      assert(t.get("latitude") == (32, 22, 44, 33))
    }
    assert(t.get("latitude2") == null)
  }

  test ("test setup") {
    val map = Map("latitude" ->(32, 22, 44, 33),
      "message to you" -> "hi, there", // , world?",
      "time" ->(11, 21),
      "date" ->(2014, 10, 10))

    t.setup(map)
    assert(t.getKeys().toSet == Set("latitude", "message to you", "time", "date"))

    t.setup(map, m = 6, k = 3, q = 8*4, complete=false)
    assert(t.get("date") == (2014,10,10))
  }

  def test(width:Int, map:Map[String, Any]) = {
    t.setup(m = 8, k = 3, q = 8*width)
    if (t.check("latitude") == NoError)
      assert(t.get("latitude") == (32, 22, 44, 33))
    if (t.check("time") == NoError)
      assert(t.get("time") == (11,11))
    if (t.check("date") == NoError)
      assert(t.get("date") == (2014,10, 1))

    println(s"width = ${width}, ${t.getSizes}, ${t.getSize}")
  }

  test ("test size from Map") {

    def getMap(message:String) = {
      var map: Map[String, Any] = Map("latitude" ->(32, 22, 44, 33),
        "message" -> message, // , world?",
        "time" ->(11, 11),
        "date" ->(2014, 10, 1))
      map
    }
    message = "Hello, world"
    test(1, getMap(message))
    test(2, getMap(message))
    test(3, getMap(message))
    test(4, getMap(message))
    test(5, getMap(message))
    test(6, getMap(message))
    test(7, getMap(message))
    test(8, getMap(message))

    val ls = LabeledSummary(getMap("Hello, world"))
    ls.setup(jsonMap = getMap(message))
    println(s"Labeled - ${ls.getSizes}")
    println(s"Output from ${new Exception().getStackTrace.head.getFileName}")
  }

  test ("test size from Json") {
    val (map, jsonSize, jsonCompressedSize) = ContextSummary.loadJsonAll("contextSummary/src/test/scala/resource/unittest.json")
    test(1, map)
    test(2, map)
    test(3, map)
    test(4, map)
    test(5, map)
    test(6, map)
    test(7, map)
    test(8, map)

    println(s"json - ${jsonSize}-${jsonCompressedSize}")
  }

  test ("load") {
    t.load("contextSummary/src/test/scala/resource/sample_context.json")
    t.setup(m = 10, k = 3, q = 8*4)
    assert(t.check("abc") == BottomType.NoError)
    assert(t.get("abc") == "Hello, world")
    assert(t.check("recommendation") == BottomType.NoError)
    assert(t.get("recommendation") == "Chef")
    assert(t.check("level of recommendation") == BottomType.NoError)
    assert(t.get("level of recommendation") == 5)
    assert(t.check("level of recommendations") != BottomType.NoError)
  }

  test ("load 2") {
    t.load("contextSummary/src/test/scala/resource/sample_context.json", m = 10, k = 3, q = 8*4)
    assert(t.check("abc") == BottomType.NoError)
    assert(t.get("abc") == "Hello, world")
    assert(t.check("recommendation") == BottomType.NoError)
    assert(t.get("recommendation") == "Chef")
    assert(t.check("level of recommendation") == BottomType.NoError)
    assert(t.get("level of recommendation") == 5)
    assert(t.check("level of recommendations") != BottomType.NoError)
  }

  test ("store") {
    val filePath = "contextSummary/src/test/scala/resource/sample_context_test_result.json"

    val file = new java.io.File(filePath)
    if (file.exists()) {
      file.delete()
    }
    val mp = Map[String, Any]("a" -> "helloa", "level of a" -> 3)
    t.setup(mp, m=4, k=3, q=8*5, complete=false)

    assert(t.get("a") == "helloa")
    t.save(filePath)

    t.load(filePath)
    assert(t.check("a") == BottomType.NoError)
    assert(t.get("a") == mp("a"))
    assert(t.check("level of a") == BottomType.NoError)
    assert(t.get("level of a") == mp("level of a"))
  }

  test ("test repr") {
    t.setup(m=10, k=3, q=4*4)
    val expect = """{"type":"b", "complete":0, "size":16, "jsonSize":144, "jsonCompSize":117, "n":7, "m":10, "k":3, "q":16}"""
    assert(t.repr() == expect)
  }
}
