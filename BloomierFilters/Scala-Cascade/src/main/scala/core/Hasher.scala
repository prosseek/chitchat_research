package core

import hash.Hash

object Hasher {
  var useUnique = false

  def get(key:String, m:Int, k:Int, seed:Int) = {
    if (Hasher.useUnique)
      Hash.getUniqueHashes(key, count = k, maxVal = m, startSeed = seed)
    else
      Hash.getHashes(key, count = k, maxVal = m, startSeed = seed)
  }

}

/**
 * Created by smcho on 7/1/14.
 */
//case class Hasher(val maxVal:Int, val startSeed:Int) {
//  def get(key:String, count:Int) = {
//    if (Hasher.useUnique)
//      Hash.getUniqueHashes(key, count = count, maxVal = maxVal, startSeed = startSeed)
//    else
//      Hash.getHashes(key, count = count, maxVal = maxVal, startSeed = startSeed)
//  }
//}
