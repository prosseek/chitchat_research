package smcho

import org.scalatest.{BeforeAndAfterEach, FunSuite}

/**
 * Created by smcho on 9/12/15.
 */
class NameTypeTest extends FunSuite with BeforeAndAfterEach {

  var nameType:NameType = _
  var summaries = Summary.loadContexts(directory = "contextProcessor/src/test/resources/")

  override def beforeEach() {

  }

  test("test splitNameTypes") {
    val input = "g3c14l"
    val expected = ("g3c14", "l")
    assert(NameType.split(input) == expected)
  }

  test("test constructor") {
    val n = NameType("g1c0l", summaries)
    assert(n.summaryName == "g1c0")
    assert(n.groupId == 1)
    assert(n.hostId == 0)
    assert(n.summaryType == "l")
  }

  test("test constructor 2") {
    val n = NameType("g1c0l", summaries)
    assert(n.summary.toString() == "g1c0|[105,52,29]")
  }

  test("test get/sizes") {
    nameType = NameType("g1c0l", summaries)
    assert(nameType.get("h") == null)
    assert(nameType.get("latitude") == (10, 10, 10, 10))
    assert(nameType.size() == 52)

    nameType = NameType("g1c0b", summaries)
    assert(nameType.get("h") == null)
    assert(nameType.get("latitude") == (10, 10, 10, 10))
    assert(nameType.size() == 29)

    nameType = NameType("g1c0j", summaries)
    assert(nameType.get("h") == null)
    assert(nameType.get("latitude") == (10, 10, 10, 10))
    assert(nameType.size() == 105)
  }

  test("test size") {
    nameType = NameType("g1c0l", summaries)


    nameType = NameType("g1c0b", summaries)
    assert(nameType.get("h") == null)
    assert(nameType.get("latitude") == (10, 10, 10, 10))

    nameType = NameType("g1c0j", summaries)
    assert(nameType.get("h") == null)
    assert(nameType.get("latitude") == (10, 10, 10, 10))
  }

  test("test hostIdToContextName") {
    val r = NameType.hostIdToContextName(5, "3:3:3")
    println(r)
  }

  test("test") {
    assert(NameType.hostIdToContextName(0, "3:3:3") == "g1c0")
    assert(NameType.hostIdToContextName(1, "3:3:3") == "g1c1")
    assert(NameType.hostIdToContextName(2, "3:3:3") == "g1c2")
    assert(NameType.hostIdToContextName(3, "3:3:3") == "g2c3")
    assert(NameType.hostIdToContextName(4, "3:3:3") == "g2c4")
    assert(NameType.hostIdToContextName(5, "3:3:3") == "g2c5")
    assert(NameType.hostIdToContextName(6, "3:3:3") == "g3c6")
    assert(NameType.hostIdToContextName(7, "3:3:3") == "g3c7")
    assert(NameType.hostIdToContextName(8, "3:3:3") == "g3c8")
    // This is wrong, as the largest group is 3, and id is 8
    intercept[Exception] {
      assert(NameType.hostIdToContextName(9, "3:3:3") == "g4c9")
    }
  }

  test("test contextNameToHostId") {
    assert(NameType.contextNameToHostId("g1c0") == 0)
  }
}
