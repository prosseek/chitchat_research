package core

import org.scalatest._

import scala.collection.BitSet

/**
 * Created by smcho on 7/1/14.
 */
class TestBitArray extends FunSuite {
  test ("set test out of range") {
    val v = new BitArray(10, 0)
    intercept[java.lang.IndexOutOfBoundsException] {
      v.set(100)
    }
    intercept[java.lang.IndexOutOfBoundsException] {
      v.set(-1)
    }
  }

  test ("set and get test") {
    val v = new BitArray(10, 0)
    v.set(4)
    assert(v.get(4) == true)
    assert(v.get(0) == false)
  }

  test ("set with hasher") {
    val v = new BitArray(10, 0)
    v.setUnique(true) // get unique values
    v.set("Hello", k=3)
    assert(v.get() == BitSet(3, 7, 8))
  }
}
