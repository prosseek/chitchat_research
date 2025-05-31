package bf

import core.{BitArray, Hasher}

/**
 * Created by smcho on 6/30/14.
 */
class BloomFilter(keys:Set[String], m: Int, k: Int, seed: Int = 0) {
  val bitArray = BitArray(m, seed = seed)
  //val hasher = Hasher(maxVal = m)
  keys.foreach(key =>
    Hasher.get(key = key, m = m, k = k, seed = seed).foreach(bitArray.set(_)))

  def get(key:String) = {
    getIndexes(key).map(bitArray.get(_)).forall(_ == true)
  }

  def debug() = {
   println(bitArray.bitSet)
  }

  def getIndexes(key:String) = {
    Hasher.get(key = key, m = m, k = k, seed = seed)
  }
}
