package smcho

/**
 * Created by smcho on 8/26/15.
 */
trait LoadClass {
  // From the className, database can load different strategies
  def getClass (className: String) = {
    var c: Class[_] = null
    try {
      c = Class.forName(className)
    }
    catch {
      case e: ClassNotFoundException => {
        throw new Exception("Couldn't find class '" + className + "'" + "\n" + e.getMessage, e)
      }
    }
    c
  }

  def loadObject (className: String) = {
    var o: Any = null

    try {
      val objClass = getClass(className)
      o = objClass.newInstance
    }
    catch {
      case e: SecurityException => {
        e.printStackTrace
        throw new Exception("Fatal exception " + e, e)
      }
    }
    o
  }
}
