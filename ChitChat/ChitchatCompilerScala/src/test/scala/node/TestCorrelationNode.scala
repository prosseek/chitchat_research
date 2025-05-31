package node

import org.scalatest.FunSuite



class TestCorrelationNode extends FunSuite {
//  val prognode = NodeGenerator.get("./resources/unittest_example/correlation_simple.txt")

  /**
    *
  === Input ===
  # correlation location = (latitude, longitude)
  # correlation bookseller = (name, location)

  === Output ===
    allexists latitude longitude
    stop

    allexists name latitude longitude
    stop
    */
  test ("simple") {
    val prognode = NodeGenerator.get("./resources/unittest_example/correlation_simple.txt")
    val bs = prognode.getNode[CorrelationNode]("bookseller", prognode.correlations).get
    val loc = prognode.getNode[CorrelationNode]("location", prognode.correlations).get
    assert(bs.id.name == "bookseller")
    assert(loc.id.name == "location")
    assert(bs.function_call == null)
    assert(loc.function_call == null)

    assert(bs.values.length == 2)
    assert(bs.values.length == 2)

    assert(bs.get(prognode.correlations.toList).toString == "List(name, latitude, longitude)")
    val res = loc.get(prognode.correlations.toList)
    assert(res.toString == "List(latitude, longitude)")
  }
}
