package smcho

import core.LabeledSummary
import org.scalatest.{BeforeAndAfterEach, FunSuite}
import org.scalatest.Assertions._

/**
 * Created by smcho on 8/12/15.
 */
class DatabaseWithStrategyTest extends FunSuite  with BeforeAndAfterEach {

  var database: DatabaseWithStrategy = _
  val strategy = "smcho.SimpleShareLogic"

  override def beforeEach() {
    database = DatabaseWithStrategy(strategy, "contextProcessor/src/test/resources", "l", "1:0:1")
  }

  test("test construction") {
    assert(database.storage.repr.startsWith("""{"summaries":[{"name":"g1c0""""))
    assert(database.strategy == strategy)
    assert(database.storage.summariesMap == ContextMessage.summariesMap)
  }

  // add received ContextMessage to host
  test ("test add") {
    // add(host: Int, contextMessage: ContextMessage)
    database.add(0, ContextMessage("g1c0l:g3c1b"))
    assert(database.storage.getContexts(0).toString == "Set([0->0/0.0/g1c0l:g3c1b/81])")
    assert(database.storage.getContexts(3).toString == "Set()")
  }
  test ("test getSize") {
    //getSize(nameTypesString: String) : Int
    assert(database.getSize("g1c0l:g3c1b") == 81)
  }
  test ("test hosts") {

    assert(database.hostsConfigMap ==
      Map("n" -> 3, "group1" -> 3, "group2" -> 3, "group3" -> 3, "default3" -> 3000, "default1" -> 1000, "1" -> 4000, "0" -> 5000, "default2" -> 2000)
    )
  }
  test("test getHostLimit") {
    val directory = "contextProcessor/src/test/resources"
    val hosts = util.file.readers.readProperty(directory + "/" + "hosts.txt")
    assert(database.getHostLimit(0, hosts) == 5000)
    assert(database.getHostLimit(1, hosts) == 4000)
    assert(database.getHostLimit(2, hosts) == 1000)
    assert(database.getHostLimit(3, hosts) == 2000)
    assert(database.getHostLimit(4, hosts) == 2000)
    assert(database.getHostLimit(5, hosts) == 2000)
    assert(database.getHostLimit(6, hosts) == 3000)
    assert(database.getHostLimit(7, hosts) == 3000)
    assert(database.getHostLimit(8, hosts) == 3000)
    intercept[Exception] {
      assert(database.getHostLimit(9, hosts) == -1)
    }
  }
}
