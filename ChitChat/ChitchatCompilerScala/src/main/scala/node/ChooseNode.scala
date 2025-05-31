package node

import node.codegen.Template
import scala.collection.mutable.{Map => MMap}

/**
  * choose: (id '|'?)+ ;
  */
case class ChooseNode(override val name:String,
                      val ids:List[IdNode]) extends Node(name = name) with Template {
  /*
    read event
    jpeekfalse EVENT
    register event
    jmp ADVERTISEMENTEND
EVENT:

    pop $temp
    read advertisement
    jpeekfalse END
    register advertisement
ADVERTISEMENTEND:
   */

  def codeGen(progNode:ProgNode, labels:Map[String, String] = null) :String = {

    val endLabel = labels("endLabel")
    val endLabelInChoose = name + "_END"
    val res = new StringBuilder

    // except the last
    ids.reverse.tail.reverse foreach {
      id => res ++= s"read ${id.name}\njpeekfalse ${id.name}_LABEL:\nregister${id.name}\njmp ${endLabelInChoose}\n\n"
    }
    // last processing
    val last = ids.last
    res ++= ("pop $temp\n" + s"read ${last.name}\njpeekfalse ${endLabel}\nregister ${last.name}\n${endLabelInChoose}:\n")

    res.toString

  }
}
