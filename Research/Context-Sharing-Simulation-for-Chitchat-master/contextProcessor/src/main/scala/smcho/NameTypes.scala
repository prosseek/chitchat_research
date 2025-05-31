package smcho

import scala.collection.mutable
import scala.collection.mutable.{Map => mm}

object NameTypes {
  val cacheMap = mm[String, Iterable[NameType]]()

  def count() = cacheMap.size

  def size(names:String, summariesMap:mm[String, Summary]) = {
    NameTypes(names, summariesMap).size()
  }

  def split(names:String) = {
    names.split(":").toSet.toList
  }

  def nameSort(name: String) = {
    name.split(":").toSet.toList.sorted.mkString(":")
  }

  /**
   * Given names, return a list of
   * @param nameTypes
   * @return
   */
  def getNameTypeIterable(nameTypes:String, summariesMap:mm[String, Summary]) = {
    (scala.collection.mutable.ListBuffer[NameType]() /: split(nameTypes)) {
      (acc, value) => acc += NameType(value, summariesMap)
    }
  }

  def add(nameTypes:String, summaries:mm[String, Summary]) = {
    val sortedName = nameSort(nameTypes)
    if (!cacheMap.contains(sortedName)) {
      cacheMap(sortedName) = getNameTypeIterable(sortedName, summaries)
    }
    cacheMap(sortedName)
  }

  def set(nameTypes: String, value: Iterable[NameType]) = {
    cacheMap(nameSort(nameTypes)) = value
  }

  def get(nameTypes: String) = {
    cacheMap.get(nameSort(nameTypes)) match {
      case Some(p) => p
      case None => null
    }
  }
}

/**
 * Created by smcho on 9/12/15.
 */
case class NameTypes(name:String, summariesMap:mm[String, Summary]) {
  // Add nameTypes to the cache
  val nameTypeStrings = NameTypes.split(name)
  val sortedName = NameTypes.nameSort(name)
  val nameTypes: Iterable[NameType] = NameTypes.add(name, summariesMap)

  def count() = nameTypes.size

  def size() = {
    (0 /: nameTypes) { (acc, value) => acc + value.size }
  }

  /**
   * Returns a set of NameType objects that nameType sring represents
   */
  def get(nameTypeString:String) : NameType = {
    if (nameTypeStrings.contains(nameTypeString)) {
      nameTypes foreach { nameType =>
        //println(nameType.name)
        if (nameType.name == nameTypeString)
          return nameType
      }
      null
    }
    else null
  }

  override def toString() = {
    val result = (new StringBuilder() /: nameTypes) { (acc, value) =>
        acc ++= s"${value.name}|${value.size()}:"
    }
    result.toString.dropRight(1)
  }
  
  def repr() = {
    s"""{"name":"${name}", "sortedName":"${sortedName}", "size":${size}}"""
  }
}
