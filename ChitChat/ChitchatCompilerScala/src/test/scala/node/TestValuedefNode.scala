package node

import org.scalatest.FunSuite

class TestValuedefNode extends FunSuite {

  /**
    * value cityParkCenter(latitude, longitude) = {
    *   latitude = [30, 25, 01, 74]
    *   longitude = [-97, 47, 21, 83]
    * }
    */
  test("simple") {
    val prognode = NodeGenerator.get("./resources/unittest_example/value_simple.txt")
    val a = prognode.getNode[ValuedefNode]("cityParkCenter", prognode.valuedefs).get

    assert(a.id.toString() == "IdNode(cityParkCenter)")
    assert(a.map.toString == "Map(latitude -> [30,25,01,74], longitude -> [-97,47,21,83])")
  }
}