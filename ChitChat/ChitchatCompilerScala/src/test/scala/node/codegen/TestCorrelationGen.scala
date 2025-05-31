package node.codegen

import node.{CorrelationNode, NodeGenerator}
import org.scalatest.FunSuite

class TestCorrelationGen extends FunSuite
{
  /**
    * correlation location = (latitude, longitude)
    * correlation bookseller = (name, location)
    */
  test ("simple") {
    val prognode = NodeGenerator.get("./resources/unittest_example/correlation_simple.txt")
    val cs = prognode.correlations

    val c = prognode.getNode[CorrelationNode]("bookseller", prognode.correlations).get
    println(c.codeGen(progNode = prognode))
  }

  test ("simple function") {
    val prognode = NodeGenerator.get("./resources/unittest_example/correlation_function.txt")
    val cs = prognode.correlations

    val c = prognode.getNode[CorrelationNode]("producePrice", prognode.correlations).get
    println(c.codeGen(progNode = prognode))
  }
}
