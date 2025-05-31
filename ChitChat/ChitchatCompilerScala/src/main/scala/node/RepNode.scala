package node

import node.codegen.Template

import scala.collection.mutable.{Map => MMap}
/**
  *   rep: '(' (id ','?)+ ')' '+';
  */
case class RepNode(override val name:String,
                   val ids:List[IdNode]) extends Node(name = name) with Template {
  /**
    * Beware that this returns the function body
    *
    * @param progNode
    * @param labels
    * @return
    */
  def codeGen(progNode:ProgNode, labels:Map[String, String] = null) :String = {

    def read(name:String, map:Map[String, String]) = {
      s"read $name " + "$temp\n" + s"jpeekfalse ${map("error_end_loop")}\nregister $name" + "$temp\n\n"
    }
    /**
      *     read sensor $temp
      *     jpeekfalse ERRORENDLOOP
      *     register sensor $temp
      *
      * @return
      */
    def readFirstIds(map:Map[String, String]) = {
      val res = new StringBuilder
      ids foreach {
        id => res ++= read(id.name, map)
      }
      res.toString
    }
    def readIds(map:Map[String, String]) = {
      val res = new StringBuilder
      ids foreach {
        id => res ++= read(id.name, map)
      }
      val header =
        """
          |load $bp + 2
          |push 1
          |iadd
          |
          |store $bp + 2
          |load $bp + 2
          |pop $temp
          |""".stripMargin

      val footer = s"jmp ${map("init")}"

      header + res.toString + footer
    }

    val map = MMap[String, String]()
    val template =
      """
        |#{label}:
        |load $bp + 2
        |pop $temp
        |#{readfirstids}
        |#{init}:
        |#{readids}
        |#{error_end_loop}:
        |swap
        |#{end_loop}:
        |pop
        |r 0
      """.stripMargin

    map("label") = name
    map("error_end_loop") = name + "_EEL"
    map("end_loop") = name + "_EL"
    map("readfirstids") = readFirstIds(map.toMap)
    map("init") = name + "_INIT"
    map("readids") = readIds(map.toMap)

    getTemplateString(template, map.toMap)
  }

  def headerCodeGen(progNode:ProgNode, labels:Map[String, String] = null) = {
    val endLabel = labels("endLabel")
    s"f ${name}\njpeekfalse ${endLabel}"
  }
}
