package core

import org.scalatest.FunSuite

/**
 * Created by smcho on 7/4/14.
 */
class TestKeys extends FunSuite {
  test ("Simple") {
    val keys = Keys()
    keys.add(1, 2, "Hello")
    assert(keys.get(1,2).contains("Hello"))
    assert(keys.get(1,2).contains("Not Hello") == false)

    keys.add(0, 3, "Hello")
    assert(keys.get(1,2).contains("Hello"))
  }

  test ("Debug print") {
    val keys = Keys()
    keys.add(0, 0, "0Hello0")
    keys.add(1, 0, "1Hello0")
    keys.add(0, 1, "0Hello1")
    keys.add(1, 1, "")

    println(keys.debug())
  }

  test("Check test") {
    val keys = Keys()
    keys.add(0, 0, "Hello")
    keys.add(0, 4, "Hello")

    /*
      0 -> 4 to cause AssertionError that the sequences are not increased by 1
     */
    intercept[AssertionError] {
      keys.check()
    }
  }
  test("Max size") {
    val keys = Keys()
    keys.add(0, 0, "Hello")
    keys.add(0, 1, "Hello")

    keys.add(1, 0, "Hello")
    keys.add(1, 1, "Hello")
    assert(keys.getMaxLevel() == 1)
  }

  test("Add test") {
    val keys = Keys()
    val ks = List("Hello", "World")
    keys.add(0,0,ks)
    keys.debug(true)
  }
}
