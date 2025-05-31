package util.file

import java.io.FileInputStream
import java.util.Properties
import scala.collection.JavaConversions._

/**
 * Created by smcho on 9/13/15.
 */
object readers {
  def readProperty(filePath:String) = {
    // http://stackoverflow.com/questions/9938098/how-to-check-to-see-if-a-string-is-a-decimal-number-in-scala
    def isAllDigits(x: String) = x forall Character.isDigit
    def convert(value: Any) = {
      val newValue = value.asInstanceOf[String]
      if (isAllDigits(newValue))
        newValue.toInt
      else
        newValue
    }

    val prop = new Properties()
    val input = new FileInputStream(filePath)
    val m = scala.collection.mutable.Map[String, Any]()
    prop.load(input)
    prop.keySet foreach { key =>
      val newKey = key.asInstanceOf[String]
      val value = convert(prop(newKey))
      m(newKey) = value
    }
    m.toMap
  }
}
