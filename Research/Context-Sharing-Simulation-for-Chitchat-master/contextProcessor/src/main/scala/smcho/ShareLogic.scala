package smcho

import scala.collection.mutable.{Set => mSet, Map => mm}

/**
 * Created by smcho on 8/22/15.
 */
trait ShareLogic {

//
//  def getSummaries() = summaries
//  def getHistory() = history
  //def setStorage(storage:Storage)
  def get(host: Int, limit: Int, initialSummaryType:String): String
  def get(host: Int, limit: Int, initialSummaryType:String, key:String, value:String): String
}
