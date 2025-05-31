package bfc

import org.scalatest.FunSuite

import scala.collection.BitSet

/**
 * Created by smcho on 7/1/14.
 */
class TestPartition extends FunSuite {
  test ("Simple") {
    val d = Map("a"->BitSet(7), "b"->BitSet(7), "c"->BitSet(6), "d"->BitSet(6))
    val p = Partition(d)
    assert(p.partition(7) == (Set("a", "b"),Set("c", "d")))
    assert(p.partition(6) == (Set("c", "d"),Set("a", "b")))
  }

  test("maxIndex") {
    val d = Map("a"->BitSet(17), "b"->BitSet(7), "c"->BitSet(6), "d"->BitSet(6))
    val p = Partition(d)
    assert(p.getMaxIndex() == 17)
  }

  test("get Test") {
    val d = Map("a"->BitSet(0), "b"->BitSet(1), "c"->BitSet(2), "d"->BitSet(3))
    val p = Partition(d)
    assert(p.get() == Map(3 -> (Set("d"),Set("a", "b", "c")), 2 -> (Set("c"),Set("a", "b", "d")), 1 -> (Set("b"),Set("a", "c", "d")), 0 -> (Set("a"),Set("b", "c", "d"))))
  }
}
