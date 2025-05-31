package smcho

import org.scalatest.FunSuite

/**
 * Created by smcho on 9/12/15.
 */
class NameParserTest extends FunSuite {

  test("test GetGroupId") {
    var input = "g3c0l"

    var expected = 3
    assert(NameParser.getGroupId(input) == expected)
    expected = 0
    assert(NameParser.getHostId(input) == expected)
    var stringExpected = "l"
    assert(NameParser.getSummaryType(input) == stringExpected)
    stringExpected = "g3c0"
    assert(NameParser.getName(input) == stringExpected)

    input = "xg33c0p"

    expected = -1
    assert(NameParser.getGroupId(input) == expected)
    expected = -1
    assert(NameParser.getHostId(input) == expected)
    stringExpected = ""
    assert(NameParser.getSummaryType(input) == stringExpected)
    stringExpected = ""
    assert(NameParser.getName(input) == stringExpected)
  }

  test("test getGroupIdIgnoringSummaryType") {
    var input = "g3c0l"
    var expected = 3
    assert(NameParser.getGroupIdIgnoringSummaryType(input) == expected)

    input = "g3c0"
    expected = 3
    assert(NameParser.getGroupIdIgnoringSummaryType(input) == expected)

    input = "XXX"
    intercept[Exception] {
      assert(NameParser.getGroupIdIgnoringSummaryType(input) == expected)
    }
  }

}
