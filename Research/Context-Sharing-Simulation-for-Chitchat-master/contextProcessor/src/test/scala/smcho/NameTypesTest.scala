package smcho

import org.scalatest.{BeforeAndAfterEach, FunSuite}

/**
 * Created by smcho on 9/12/15.
 */
class NameTypesTest extends FunSuite with BeforeAndAfterEach {
  var summaries = Summary.loadContexts(directory = "contextProcessor/src/test/resources/")
  var nt: NameTypes = _

  override def beforeEach() {

  }

  // Object test

  test("test nameSort") {
    val input = "z:z:y:x:p:a:c:d:c"
    val expected = "a:c:d:p:x:y:z"
    assert(NameTypes.nameSort(input) == expected)
  }

  test("test split") {
    val ntString = "g1c0l:g3c1j"
    val n = NameTypes.split(ntString)
    assert(n == List("g1c0l", "g3c1j"))
  }

  test("test add") {
    var ntString = "g1c0l:g3c1j"
    var n = NameTypes.add(ntString, summaries)
    assert(n.size == 2)

    // order doesn't matter
    ntString = "g3c1j:g1c0l"
    n = NameTypes.add(ntString, summaries)
    assert(n.size == 2)

    ntString = "g3c1j"
    n = NameTypes.add(ntString, summaries)
    assert(n.size == 1)
  }

  test("test getNameTypeSeq") {
    val ntString = "g1c0l:g3c1j"
    val result = NameTypes.getNameTypeIterable(ntString, summaries)
    assert(result.size == 2)

    val names = (("" /: result) {(acc, value) => acc + value.name + ":"}).dropRight(1)
    assert(NameTypes.nameSort(names) == NameTypes.nameSort(ntString))
  }

  test("test size") {
    val ntString2 = "g3c1j:g1c0l:g3c1j"
    assert(NameTypes.size(ntString2, summaries) == 52 + 105)
  }

  // Class test

  test("test constructor") {
    val ntString1 = "g1c0l:g3c1j"
    val ntString2 = "g3c1j:g1c0l:g3c1j"

    val v1 = NameTypes(ntString1, summaries)
    val v2 = NameTypes(ntString2, summaries)

    assert(v1.size == 52 + 105)
    assert(v1.count == 2)
    assert(v2.size == 52 + 105)
    assert(v2.count == 2)
    assert(v1.nameTypes == v2.nameTypes)
  }

  test("test set/get") {
    val ntString1 = "g1c0l:g3c1j"
    val v1 = NameTypes(ntString1, summaries)
    assert(null == v1.get("g1c5l"))
    assert(v1.get("g1c0l").name == "g1c0l")
  }

  test("test count") {
    val ntString1 = "g1c0l:g3c1j"
    val v1 = NameTypes(ntString1, summaries)
    assert(v1.count == 2)
  }

  test("test size in class") {
    val ntString1 = "g1c0l:g3c1j"
    val v1 = NameTypes(ntString1, summaries)
    assert(v1.size == 52 + 105)
  }

  test("test toString") {
    val ntString1 = "g1c0l:g3c1j"
    val v1 = NameTypes(ntString1, summaries)
    val expected = "g1c0l|52:g3c1j|105"
    assert(v1.toString == expected)
  }

  test("test repr") {
    val ntString1 = "g3c1j:g3c1j:g1c0l:g3c1j"
    val v1 = NameTypes(ntString1, summaries)
    val expected = s"""{"name":"$ntString1", "sortedName":"g1c0l:g3c1j", "size":157}"""
    assert(v1.repr == expected)
  }
}
