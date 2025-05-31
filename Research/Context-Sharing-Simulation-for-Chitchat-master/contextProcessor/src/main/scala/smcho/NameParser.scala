package smcho

/**
 * Created by smcho on 9/12/15.
 */
object NameParser {
    def isValidName(nameType:String) = {
      getParams(nameType) match {
        case Some((name, groupId, hostId, summaryType)) => true
        case None => false
      }
    }

    def getParams(nameType:String) = {
      val p = """^(g(\d+)c(\d+))([blj])$""".r
      nameType match {
        case p(name, groupId, hostId, summaryType) => Some(name, groupId.toInt, hostId.toInt, summaryType)
        case _ => None
      }
    }

    def getParamsIgnoringSummaryType(nameType:String) = {
      val p = """^(g(\d+)c(\d+))([blj])?$""".r
      nameType match {
        case p(name, groupId, hostId, summaryType) => Some(name, groupId.toInt, hostId.toInt, summaryType)
        case _ => None
      }
    }

    def getGroupId(nameType:String) = {
      getParams(nameType) match {
        case Some((name, groupId, hostId, summaryType)) => groupId
        case None => -1
      }
    }

    def getGroupIdIgnoringSummaryType(nameType:String) = {
      val p = """^(g(\d+)c(\d+))([blj])?$""".r
      nameType match {
        case p(name, groupId, hostId, summaryType) => groupId.toInt
        case _ => throw new Exception(s"Error no correct format: ${nameType}")
      }
    }

    def getHostId(nameType:String) = {
      getParams(nameType) match {
        case Some((name, groupId, hostId, summaryType)) => hostId
        case None => -1
      }
    }

    def getSummaryType(nameType:String) = {
      getParams(nameType) match {
        case Some((name, groupId, hostId, summaryType)) => summaryType
        case None => ""
      }
    }

    def getName(nameType:String) = {
      getParams(nameType) match {
        case Some((name, groupId, hostId, summaryType)) => name
        case None => ""
      }
    }
}
