package bf

import org.scalatest.FunSuite

import scala.collection.mutable.ArrayBuffer
import scala.math.{exp, pow}
/**
 * Created by smcho on 7/1/14.
 */
class TestBloomFilter extends FunSuite {
  test ("Debug") {
    val s = Set("A","B","C")
    val bf = new BloomFilter(s, m = 10, k = 3)
    //bf.debug()
  }
  test ("Test - no false negatives") {
    val s = Set("A","B","C")
    val bf = new BloomFilter(s, m = 10, k = 3)
    assert(bf.get("A") == true)
    assert(bf.get("B") == true)
    assert(bf.get("C") == true)
  }

  def fpInTheory(n:Int, m:Int, k:Int) = {
    pow((1 - exp(-k.toDouble * n.toDouble / m.toDouble)), k)
  }

  def testBloomFilter(k:Int) {
    val ab = ArrayBuffer[String]()

    // S = [0 .. 99]
    val n = 100
    val sampleSize = 10000
    Range(0,n).foreach(ab += _.toString)
    val results = ArrayBuffer[Boolean]()

    for (alpha <- Range(1, 10)) {
      var m = n * alpha
      val bf = new BloomFilter(ab.toSet, m = m, k = k)
      results.clear()

      Range(n, sampleSize + n).foreach { v =>
        bf.get(v.toString) +=: results
      }

      val (t, f) = results.partition(_ == true)
      println(s"k(${k})/alpha(${alpha}): FP (${t.length/sampleSize.toDouble}) - THEORY (${fpInTheory(n,m,k)})")
    }
  }

  test ("Calculate false positives") {
    testBloomFilter(3)
    testBloomFilter(5)
  }
}
