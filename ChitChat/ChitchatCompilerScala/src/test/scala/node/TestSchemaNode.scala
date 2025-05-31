package node

import org.scalatest.FunSuite

class TestSchemaNode extends FunSuite {
  /**
      # +schema sender = (a b c)
      read a
        jpeekfalse END
        register a
        read b
        jpeekfalse END
        register b
        read c
        jpeekfalse END
        register c
        push_summary
       END:
        stop

    */
  test("simple") {
    val prognode = NodeGenerator.get("./resources/unittest_example/schema_simple.txt")
    val bs = prognode.getNode[SchemaNode]("sender", prognode.schemas).get

    val res = bs.codeGen(prognode)
    println(res)
  }

  test("classic") {
    // +schema sensors = (name , event | advertisement , time?)
    val prognode = NodeGenerator.get("./resources/unittest_example/schema_classic.txt")
    val bs = prognode.getNode[SchemaNode]("sensors", prognode.schemas).get

    val res = bs.codeGen(prognode)
    println(res)
  }

  test("rep") {
    // todo: the value is not allowed in the schema
    // # + schema x = (name , event , (sensor, v)+ )
    val prognode = NodeGenerator.get("./resources/unittest_example/schema_rep.txt")
    val bs = prognode.getNode[SchemaNode]("x", prognode.schemas).get

    val res = bs.codeGen(prognode)
    println(res)
  }
}
