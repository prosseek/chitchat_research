package node

import node.codegen.Template
import scala.collection.mutable.{Map => MMap}

object IdNode {
  def make(name:String) = {
    IdNode(name = name.replace("\"", ""))
  }
}

case class IdNode(override val name:String) extends Node(name = name) with Template {
  def codeGen(progNode:ProgNode, labels:Map[String, String] = null) :String = {
    val bpName = progNode.parameterTranslate(name)
    // when bpName == name, the name is not a parameter
    if (bpName == name)
      s"push ${name}\n"
    else
      s"load ${bpName}\n"
  }

  def schemaCodeGen(progNode:ProgNode, endLabel:String) :String = {
    /*
             read time
             jpeekfalse TIMEEND
             register time
             jmp TIMENEXT
         TIMEEND:
             pop $temp
         TIMENEXT:
     */
    if (name.endsWith("?")) {
      val name = this.name.replace("?", "")
      val template ="""
          |# optional start #{name}
          |read #{name}
          |jpeekfalse #{end}
          |register #{name}
          |jmp #{next}
          |#{end}:
          |pop $temp
          |#{next}:
        """.stripMargin
      val map = MMap[String, String]()

      map("name") = name
      map("end") = name + "_END"
      map("next") = name + "_NEXT"
      getTemplateString(template, map.toMap)
    }
    else
      s"read ${name}\njpeekfalse ${endLabel}\nregister ${name}\n"
  }
}
