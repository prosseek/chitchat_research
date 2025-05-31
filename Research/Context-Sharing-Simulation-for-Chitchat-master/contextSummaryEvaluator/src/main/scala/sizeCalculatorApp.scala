package smcho

/**
 * Created by smcho on 9/16/15.
 */
object sizeCalculatorApp extends App {

  def runit(contextName:String, noKey:Boolean=true, maxValue:Int = 380) = {
    val baseDirectory = s"contextSummaryEvaluator/resources/jsonContexts/${contextName}/"
    val testFilePathEmergency = s"${baseDirectory}/${contextName}.json"
    val sizeResultJsonFileName = s"${baseDirectory}/results.json"
    val dataFileName = s"${baseDirectory}/data.txt"
    val gnuFileName = s"${baseDirectory}/gnuplot.txt"

    val v = new SizeCalculator(testFilePathEmergency, maxValue = maxValue)
    val r = v.getResultInJson(sizeResultJsonFileName)
    val d = v.getDataFromJsonString(r, dataFileName)
    val g = v.getGnuplotScript(gnuFileName, contextName, noKey)
    v.runGnuScript(baseDirectory)
  }
  runit("building", noKey=true)
  runit("emergency", noKey = false)
  runit("market", noKey=true)

//  for (i <- 1.until(7)) {
//    runit(s"s${i}", noKey = true)
//  }
//  for (i <- 1.until(3)) {
//    runit(s"c${i}", noKey = true, maxValue=260)
//  }
}
