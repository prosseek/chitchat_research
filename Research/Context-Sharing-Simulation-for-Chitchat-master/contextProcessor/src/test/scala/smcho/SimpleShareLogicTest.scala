package smcho

import org.scalatest.{BeforeAndAfterEach, FunSuite}

import scala.collection.mutable.ListBuffer

/**
 * Created by smcho on 8/28/15.
 */
class SimpleShareLogicTest extends FunSuite with BeforeAndAfterEach {

  val directory = "contextProcessor/src/test/resources"
  var s:SimpleShareLogic = _
  var storage:Storage = _

  override def beforeEach() {
    Storage.storage = new Storage(directory, "1:0:1")
    storage = Storage.storage
    s = SimpleShareLogic()
  }

  override def afterEach(): Unit = {
    Storage.reset()
  }

  test("test findContextTuple") {
    val host = 0
    val limit = 1000
    Storage.storage.add(host, ContextMessage("g1c0l:g3c1b"))
    storage.add(1, ContextMessage("g1c0l:g3c1b"))
    assert(s.findContextTuple(host).get == (0,0,0.0,"g1c0l",52))
    assert(s.findContextTuple("g1c0").get == (0,0,0.0,"g1c0l",52))
    assert(s.findContextTuple(1).get == (0,0,0.0,"g3c1b",29))
    assert(s.findContextTuple("g3c1").get == (0,0,0.0,"g3c1b",29))
  }

  test("test findContextTuple 2") {
    val host = 0
    val limit = 1000
    storage.add(host, ContextMessage("g1c0l:g3c1b"))
    assert(s.findContextTuple(host).get == (0,0,0.0,"g1c0l",52))
    assert(s.findContextTuple("g1c0").get == (0,0,0.0,"g1c0l",52))
    assert(s.findContextTuple(1).getOrElse(null) == null)
    assert(s.findContextTuple("g3c1").getOrElse(null) == null)
  }

  test("test addContextTupleUptoLimit") {
    val host = 0
    storage.add(host, ContextMessage("g1c0l:g3c1b"))
    val contextTuples = s.getContextTuples(host)

    assert(s.addContextTupleUptoLimit(0, contextTuples) == List())
    assert(s.addContextTupleUptoLimit(60, contextTuples) == List((0,0,0.0,"g3c1b",29))) // == List())
    assert(s.addContextTupleUptoLimit(160, contextTuples) == List((0,0,0.0,"g3c1b",29), (0,0,0.0,"g1c0l",52)))
  }

  test("test getSimilarContexts") {
    storage.add(0, ContextMessage("g1c0l:g3c1b"))
    assert(s.getSimilarContexts(0, "message", "hello") == ListBuffer((0,0,0.0,"g3c1b",29), (0,0,0.0,"g1c0l",52)))
    assert(s.getSimilarContexts(0, "message", "x") == ListBuffer())
    assert(s.getSimilarContexts(0, "m", "x") == ListBuffer())
  }

  test("test containsContext") {
    storage.add(1, ContextMessage("g1c0l:g3c1b"))
    val contextTuples = s.getContextTuples(1)
    assert(s.containsContext((1,2,10.0,"g1c0l",10), contextTuples))
    assert(s.containsContext((1,2,10.0,"g3c1b",10), contextTuples)) // Only name is compared
    assert(!s.containsContext((1,2,10.0,"a",10), contextTuples))
  }

  test("test getContextsSorted") {

    storage.add(1, ContextMessage(1,2,10.0,"g1c0l"))
    storage.add(1, ContextMessage(1,2,100.0,"g3c1l"))
    val contextTuples = s.getContextTuples(1)

    assert(s.getContextsSorted(1, null) == List((1,2,100.0,"g3c1l",52), (1,2,10.0,"g1c0l",52)))
    assert(s.getContextsSorted(1, List((1,2,100.0,"g3c1l",52))) == List((1,2,10.0,"g1c0l",52)))
  }


  test("test tuplesToNameTypes") {
    val l = List((1,2,100.0,"g3c1l",52), (1,2,10.0,"g1c0l",52))
    assert(s.tuplesToNameTypes(l) == "g1c0l:g3c1l")
    assert(s.tuplesToNameTypes(List()) == "")
  }

  test("testGet first case") {
    val host = 0
    val limit = 1000

    // "l" is initial summary type that is shared
    assert(s.get(host, limit, "l") == "g1c0l")
  }

  test("testGet unlimited case") {
    val host = 0
    val limit = 100000

    storage.add(host, ContextMessage("g1c0l:g3c1b"))
    // "l" is initial summary type that is shared
    assert(s.get(host, limit, "l") == "g1c0l:g3c1b")
  }
}
