package smcho

import core.LabeledSummary
import org.scalatest.{BeforeAndAfterEach, FunSuite}
import org.scalatest.Assertions._

/**
 * Created by smcho on 8/12/15.
 */
class ReadersTest extends FunSuite  with BeforeAndAfterEach {

  val confFilePath = "contextSummary/src/test/scala/resource/unittest.conf"
  test ("test read property") {
    val res = util.file.readers.readProperty(confFilePath)
    assert(res == Map("name" -> "Hello", "q" -> 24, "k" -> 3, "m" -> 0, "complete" -> 0))
  }
}
