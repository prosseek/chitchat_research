package node

import org.scalatest.FunSuite

class TestSituation extends FunSuite {
  /*
  value cityParkCenter(latitude, longitude) = {
    latitude = [30, 25, 01, 74]
    longitude = [-97, 47, 21, 83]
  }
  situation nearCityPark() = |[latitude, longitude] - cityParkCenter| <= 5 _km
   */
  test ("simple") {
    val prognode = NodeGenerator.get("./resources/unittest_example/situation_citypark.txt")
    val a = prognode.getNode[SituationNode]("nearCityPark", prognode.situations).get
    println(a.codeGen(prognode))
  }
}