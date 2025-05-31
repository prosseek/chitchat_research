package vm

import org.scalatest.FunSuite

class TestSystem extends FunSuite {
  test("here test") {
    val (lat, long) = System.here()
    println(lat, long)
  }

  test ("test here and now") {
    val res = System.now()
    println(res.mkString("[",":","]"))
  }
}
