package smcho

import org.scalatest.{BeforeAndAfterEach, FunSuite}

/**
 * Created by smcho on 8/21/15.
 */
class SummaryTest extends FunSuite with BeforeAndAfterEach {
  val jsonFilePath = "contextProcessor/src/test/resources/g1c0.json"
  val confFilePath = "contextProcessor/src/test/resources/g1c0.conf"
  var t : Summary = _

  override def beforeEach(): Unit = {
    t = new Summary(name="hello", filePath=jsonFilePath)
  }

  test("test name") {
    assert(t.name == "hello")
    t.name = "oops"
    assert(t.name == "oops")
  }

  test("test filePath") {
    assert(t.filePath == jsonFilePath)
    assert(t.confFilePath == confFilePath)
  }

  test("test getConfigurationFilePath") {
    val res = Summary.getConfigurationFilePath(jsonFilePath)
    assert(res == confFilePath)

    intercept[Exception] {
      Summary.getConfigurationFilePath("hello.json")
    }
  }

  test("test conf") {
    assert(t.conf == Map("q" -> 24, "k" -> 3, "m" -> 0, "complete" -> 0))
  }

  test("test sizes") {
    val expected = (105,52,29)
    assert(t.sizes == expected)
  }

  test("toString test") {
    assert(t.toString() == "hello|[105,52,29]")
  }

  test("test repr") {
    val expected = """{"name":"hello", "sizes":[105,52,29], "fileName":"g1c0.json"}"""
    assert(t.repr == expected)
  }

  //    m = 0
  //    k = 3
  //    q = 24
  //    complete = 0
  test ("test read property") {
    val res = util.file.readers.readProperty(confFilePath)
    assert(res == Map("q" -> 24, "k" -> 3, "m" -> 0, "complete" -> 0))
  }
  test ("test getConf") {
    assert(t.conf == Map("q" -> 24, "k" -> 3, "m" -> 0, "complete" -> 0))
  }

  test("test loadContext") {
    var s = Summary.loadContext(directory = "contextProcessor/src/test/resources/", name = "g1c0", othername = "default")
    assert(s.toString() == "g1c0|[105,52,29]")
    s = Summary.loadContext(directory = "contextProcessor/src/test/resources/", name = "a", othername = "g1c0")
    assert(s.toString() == "a|[105,52,29]")
    assert(s.filePath.endsWith("g1c0.json"))
  }

  test("test loadContexts") {
    val res = Summary.loadContexts(directory = "contextProcessor/src/test/resources/")
    assert(res.size == 2) // there is only one context in the directory

    val res2 = Summary.loadContexts(directory = "contextProcessor/src/test/resources/", List(5,5,5))
    assert(res2.size == (5+5+5+2-1)) // default (5+5+5), +2 existing -1 (g1c0)

    // check if there is no file, the default is setup correctly
    res2 foreach {
      case (key, summary) => {
        val group = NameParser.getGroupIdIgnoringSummaryType(key)
        if (key != "g1c0" && key != "g3c1")
          assert(summary.filePath.contains(s"default${group}"))
      }
    }
  }

  test("test loadContexts 2") {
    val res2 = Summary.loadContexts(directory = "contextProcessor/src/test/resources/", "5:5:5")
    assert(res2.size == (5+5+5+2-1)) // default (5+5+5), +2 existing -1 (g1c0)
  }

  test("test summariesToJsonString") {
    val summaries = Summary.loadContexts(directory = "contextProcessor/src/test/resources/")
    val expected = "g1c0"
    assert(Summary.summariesToJsonString(summaries).contains(expected))
  }
}
