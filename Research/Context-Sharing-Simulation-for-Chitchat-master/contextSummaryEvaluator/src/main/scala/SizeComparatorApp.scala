
/**
 * Created by smcho on 9/17/15.
 */
object SizeComparatorApp extends App {
  def getSizeEfficiencyTable(contextName:String) =
  {
    val baseDirectory = s"contextSummaryEvaluator/resources/jsonContexts/${contextName}/"
    val filePath = s"${baseDirectory}/results.json"
    val v = new SizeComparator(filePath)
    v.getColumnFormat(false)
  }

  def getSizePowerTable(contextName:String) =
  {
    val baseDirectory = s"contextSummaryEvaluator/resources/jsonContexts/${contextName}/"
    val filePath = s"${baseDirectory}/results.json"
    val v = new SizeComparator(filePath)
    v.getSizeConsumptionFormat(false)
  }

  val series = Array("s1", "s2", "s3", "s4", "s5", "s6", "c1", "c2")
  val sb = new StringBuffer()
  (sb /: series) { (acc, value) =>
    acc.append(getSizeEfficiencyTable(value))
  }
  //runit("c1")
  println(sb)

  val sb2 = new StringBuffer()
  (sb2 /: series) { (acc, value) =>
    acc.append(getSizePowerTable(value))
  }
  println(sb2)
}
