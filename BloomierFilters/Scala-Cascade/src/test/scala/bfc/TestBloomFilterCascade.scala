package bfc

import org.scalatest.{BeforeAndAfter, FunSuite}

import scala.collection.BitSet
import scala.collection.mutable.{Map => MMap}
/**
 * Created by smcho on 7/1/14.
 */
class TestBloomFilterCascade extends FunSuite with BeforeAndAfter {

  var hundredInput : Map[String, Any] = null
  var byteInput : Map[String, Any] = null // ("00" -> 0, "01" -> 1, "10" -> 2, "11" -> 3)
  var bfc : BloomFilterCascade = null // = new BloomFilterCascade(dictionary = input, r = 8, m = List[Int](10,5,3), k = List[Int](3,2,2))

  before {
    val hundred = MMap[String, Any]()
    Range(1, 101).foreach {i =>
      hundred(i.toString) = i.toByte
    }
    hundredInput = hundred.toMap

    byteInput = Map[String, Any]("00" -> 0.toByte, "01" -> 1.toByte, "10" -> 2.toByte, "11" -> 3.toByte)
    //bfc = new BloomFilterCascade(dictionary = byteInput, r = 8, m = List[Int](10,5,3), k = List[Int](3,2,2))
  }

  ignore ("Simple") {
    bfc = new BloomFilterCascade(dictionary = byteInput, r = 8, m = List[Int](3,3,3), k = List[Int](2,2,2))
    //bfc.debug(true)
    assert(bfc.getAsValue("00", 8) == 0)
    assert(bfc.getAsValue("01", 8) == 1)
    assert(bfc.getAsValue("10", 8) == 2)
    assert(bfc.getAsValue("11", 8) == 3)

    assert(bfc.getSize() == 102)
  }

  ignore ("data2bitArray test") {
    assert(BloomFilterCascade.data2bitArray(byteInput, r=8) ==
      Map("00" -> BitSet(), "11" -> BitSet(0, 1), "01" -> BitSet(0), "10" -> BitSet(1)))
  }

  ignore ("create test") {
    // for hundred
    val bfc = new BloomFilterCascade(dictionary = hundredInput, r = 8, m = List[Int](10,5,3), k = List[Int](3,2,2))
    //bfc.create()
    bfc.debug(true)
  }
  /********************************************
    * False positives tests
    ********************************************/

  /********************************************
    * UTILITIES
    ********************************************/
    def analyzeResults(bf:BloomFilterCascade, result:MMap[String, Int], i:Int, r:Int) = {
      val value = bf.getAsValue(i.toString(), r)
      if (value == -1) {
        result("None") += 1
      }
      else {
        if (i == value) {
          result("OK") += 1
        }
        else {
          result("FP") += 1
        }
      }
      result
    }

    def createBf(n: Int, m: List[Int], k: List[Int], r: Int, seed: Int = 0) = {
      val dictionary = MMap[String, Any]()
      for (i <- Range(0, n)) {
        if (r == 8)
          dictionary(i.toString()) = i.toByte
        else if (r == 16)
          dictionary(i.toString()) = i.toShort
        else if (r == 32)
          dictionary(i.toString()) = i.toInt
        else
          throw new RuntimeException("Only 8/16/32 allowed")
      }
      new BloomFilterCascade(dictionary = dictionary.toMap, m = m, k = k, r = r, seed = seed)
    }

  def testFalsePositives2(N:Int, n: Int, m: List[Int], k: List[Int], r: Int) = {
    val result = MMap[String, Int]() withDefaultValue (0)
    val bfc = createBf(n, m, k, r)
    for (i <- Range(n, n+N)) {
      analyzeResults(bfc, result, i, r)
    }
    (bfc, result)
  }

  def testFalsePositives(n: Int, m: List[Int], k: List[Int], r: Int, seed: Int = 0) = {
    val bfc = createBf(n, m, k, r, seed)
    val result = MMap[String, Int]() withDefaultValue (0)
    for (i <- Range(0, n)) {
      analyzeResults(bfc, result, i, r)
    }
    (bfc, result)
  }

  /********************************************
    * TESTS
    ********************************************/
  ignore ("False Positives Test up to 100") {
    val n = 100
    //val m = List(n/2, n/4)
    //val m = List(n/2, n/4, n/8)
    //val m = List(n/2)
    //val m = List(n/2, n/4)
    // val m = List(n/4, n/4, n/4, n/8)
    //val m = List(n/4)
    //val m = List(n, n/2)
    //val m = List(n, n/2, n/4, n/8)
    val m = List(n, n/2, n/4, n/8)
    val k = List(2,2,2)
    val r = 8
    val (bfc, result) = testFalsePositives(n=n, m=m, k=k, r=r)

    println(result)
    println(s"Size - ${bfc.getSize(false)}")
  }

  ignore ("False Positives Test up to 10000") {
    val n = 100
    val N = 10000
    //val m = List(n/2, n/4)
    //val m = List(n/2, n/4, n/8)
    //val m = List(n/2)
    //val m = List(n/2, n/4)
    //val m = List(n/4, n/4, n/4, n/8)
    val m = List(n/4)
    //val m = List(n, n/2)
    //val m = List(n, n/2, n/4)
    //val m = List(n, n/2, n/4, n/8)
    val k = List(2,2,2)
    val r = 16
    val (bfc, result) = testFalsePositives2(N=N, n=n, m=m, k=k, r=r)

    println(result)
    //println(s"Size - ${bfc.getSize(false)}")
  }

  // additional test 1
  test ("best pattern, different k") {
    val n = 100
    val N = 10000
    val m = List(n/2, n/4)
    //val m = List(n/2, n/4, n/8)
    //val m = List(n/2)
    //val m = List(n/2, n/4)
    //val m = List(n/4, n/4, n/4, n/8)
    //val m = List(n, n/10)
    //val m = List(n, n/2)
    //val m = List(n, n/2, n/4)
    //val m = List(n, n/2, n/4, n/8)
    val k = List(3,3,3)
    val r = 8
    val (bfc, result) = testFalsePositives2(N=N, n=n, m=m, k=k, r=r)

    println(result)
    println(s"Size - ${bfc.getSize(true)}")
  }

  // additional test 2
  ignore ("n = 100, then n2 = 1/10*n1") {
    val n = 100
    val N = 10000
    //val m = List(n/2, n/4)
    //val m = List(n/2, n/4, n/8)
    //val m = List(n/2)
    //val m = List(n/2, n/4)
    //val m = List(n/4, n/4, n/4, n/8)
    val m = List(n, n/10)
    //val m = List(n, n/2)
    //val m = List(n, n/2, n/4)
    //val m = List(n, n/2, n/4, n/8)
    val k = List(2,2,2)
    val r = 16
    val (bfc, result) = testFalsePositives2(N=N, n=n, m=m, k=k, r=r)

    println(result)
    println(s"Size - ${bfc.getSize(true)}")
  }

  ignore ("different seed") {
    val n = 100
    //val m = List(n/2, n/4)
    val m = List(n/2, n/4, n/8)
    //val m = List(n/2)
    //val m = List(n/2, n/4)
    //val m = List(n/4, n/4, n/4, n/8)
    //val m = List(n, n/10)
    //val m = List(n, n/2)
    //val m = List(n, n/2, n/4)
    //val m = List(n, n/2, n/4, n/8)
    val k = List(2,2,2)
    val r = 8
    val seed = 0
    var (bfc, result) = testFalsePositives(n=n, m=m, k=k, r=r, seed = seed)
    println(s"r(${seed})Size - ${bfc.getSize(true)}")
    //println(result)
//    Range(0, 20).foreach {seed =>
//      val res = testFalsePositives(n=n, m=m, k=k, r=r, seed = seed)
//      val bfc = res._1
//
//      println(s"r(${seed})Size - ${bfc.getSize()}")
//    }
  }

//  /********************************************
//    * UNIT TESTS
//    ********************************************/
//
//  test("Simple") {
//    val dictionary = Map[String, Any]("a"->1, "b"->2, "c"->4)
//    val m = 10
//    val mp = 5
//    val r = 8*4
//    val k = 3
//    val bf = new BloomFilterCascade(dictionary=dictionary, m = m, mp = mp, k = k, r = r)
//    //bf.debug()
//  }
//
//  test("isIncluded test") {
//    val bs = BitSet(0,1,2,3)
//    assert(true == BloomFilterCascade.isIncluded(bs, List(1,2,3)))
//    assert(false == BloomFilterCascade.isIncluded(bs, List(2,3,4)))
//  }
//
//  test("get test") {
//    val dictionary = Map[String, Any]("a"->1.toByte, "b"->2.toByte, "c"->4.toByte)
//    val m = 10
//    val mp = 5
//    val r = 8
//    val k = 3
//    val bf = new BloomFilterCascade(dictionary=dictionary, m = m, mp = mp, k = k, r = r)
//    assert(bf.get("a") == Some(BitSet(0)))
//    assert(bf.get("b") == Some(BitSet(1)))
//    assert(bf.get("c") == Some(BitSet(2)))
//  }
//
//  /********************************************
//    * TEST CODE FOR TABLE GENERATION
//    ********************************************/
//
//  ignore("false positives calculation n = 10") {
//    val n = 10
//    val alpha = 2.5
//    val m: Integer = (n * alpha).toInt
//    val mp = (0.5*n).toInt
//    val r = 8
//    val k = 3
//    val kp = 3
//    val N = 10000
//
//    for (i <- Range(1,2).map(i => i / 2.toFloat)) {
//      val result = testFalsePositives(N, n, m, mp, r, k, kp)
//      println(s"${i} - ${result}")
//    }
//  }
//
//  ignore("false positives calculation n = 100") {
//    val n = 100
//    val alpha = 3.5
//    val m: Integer = (n * alpha).toInt
//    val mp = (0.5*n).toInt
//    val r = 8
//    val k = 3
//    val kp = 3
//    val N = 10000
//
//    for (i <- Range(1,2).map(i => i / 2.toFloat)) {
//      val result = testFalsePositives(N, n, m, mp, r, k, kp)
//      println(s"${i} - ${result}")
//    }
//  }
//
//  test("false positives calculation n = 1000") {
//    val n = 1000
//    val alpha = 5.5
//    val m: Integer = (n * alpha).toInt
//    val mp = (0.5*n).toInt
//    val r = 16
//    val k = 3
//    val kp = 3
//    val N = 10000
//
//    for (i <- Range(1,2).map(i => i / 2.toFloat)) {
//      val result = testFalsePositives(N, n, m, mp, r, k, kp)
//      println(s"${i} - ${result}")
//    }
//  }
//
//  ignore("false negatives calculation n = 1000") {
//    val n = 1000
//    val mp = (0.1*n).toInt
//    val r = 16
//    val k = 3
//    val kp = 3
//
//    for (i <- Range(1, 20).map(i => i / 2.toFloat)) {
//      val alpha = i
//      val m: Integer = (n * alpha).toInt
//
//      val result = testFalseNegatives(n, m, mp, r, k, kp)
//      println(s"${i} - ${result}")
//    }
//  }
//
//  ignore("false negatives calculation n = 10") {
//    val n = 10
//    val mp = (1*n).toInt
//    val r = 8
//    val k = 3
//    val kp = 3
//
//    for (i <- Range(1, 10).map(i => i / 2.toFloat)) {
//      val alpha = i
//      val m: Integer = (n * alpha).toInt
//
//      val result = testFalseNegatives(n, m, mp, r, k, kp)
//      println(s"${i} - ${result}")
//    }
//  }
//
//  ignore("false negatives calculation n = 100") {
//    val n = 100
//    val mp = (0.5*n).toInt
//    val r = 8
//    val k = 3
//    val kp = 3
//
//    for (i <- Range(1, 10).map(i => i / 2.toFloat)) {
//      val alpha = i
//      val m: Integer = (n * alpha).toInt
//
//      val result = testFalseNegatives(n, m, mp, r, k, kp)
//      println(s"${i} - ${result}")
//    }
//  }
}

