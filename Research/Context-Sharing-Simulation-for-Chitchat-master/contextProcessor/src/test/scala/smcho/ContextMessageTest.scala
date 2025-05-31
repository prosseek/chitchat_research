package smcho

import org.scalatest.{BeforeAndAfterEach, FunSuite}

/**
 * Created by smcho on 8/12/15.
 */
class ContextMessageTest extends FunSuite with BeforeAndAfterEach {

  val jsonDir = "contextProcessor/src/test/resources"
  var nameTypesString: String = "g1c0l:g3c1b"
  val summariesMap = Summary.loadContexts(jsonDir)
  ContextMessage.summariesMap = summariesMap

  override def beforeEach(): Unit = {
  }

  test ("test simple") {
    val c = ContextMessage(nameTypesString)
    val expected = """[0->0/0.0/g1c0l:g3c1b/81]"""
    assert(c.toString == expected)
  }

  test ("test simple2") {
    val c = ContextMessage(0,5,3.4,nameTypesString)
    val expected = """[0->5/3.4/g1c0l:g3c1b/81]"""
    assert(c.toString == expected)
  }

  test ("test repr") {
    val c = ContextMessage(nameTypesString)
    val expected = """{"host1":0, "host2":0, "time":0.0, "nameTypes":"g1c0l:g3c1b", "size":81}"""
    assert(c.repr == expected)
  }

  test ("test repr 2") {
    val c = ContextMessage(0,5,3.4,nameTypesString,100)
    val expected = """{"host1":0, "host2":5, "time":3.4, "nameTypes":"g1c0l:g3c1b", "size":100}"""
    assert(c.repr == expected)
  }
}
