package node

import scala.collection.mutable.{Map => MMap}
import node.codegen.Template

case class FunctionNode(override val name:String,
                        val return_type:String,
                        override val id:IdNode,
                        val params:List[String],
                        val block:BlockNode)
  extends Node(name = name, id = id) with Template {

  /**
    * === function ===
    * 1. function name => label
    * 2. the number of parameter (n) makes the "return n"
    * 3. the parameters are accessed with $bp - N
    * 4. local variable makes additional code
    * 5. local variables are accessed with $bp + N
    **
    *==== Example ====
    * {{{
    *   F2(x, y, z)
    *   x + y + z
    * }}}
    * {{{
    *   F2:
    *   load $bp - 1
    *   load $bp - 2
    *   iadd
    *   load $bp - 3
    *   iadd
    *   return 3
    * }}}
    */

  /**
    * {{{
    *   f(a,b,c)
    *   size = |a,b,c| = 3
    *   a = index 0 => bp - 3 = (size - index)
    *   b = index 1 => bp - 2
    *   c = index 2 => bp - 1
    * }}}
    *
    * @param name
    * @return
    */
  def parameterTranslate(name:String) = {
    if (params.contains(name)) {
      val count = params.length - params.indexOf(name)
      "$bp" + s" - ${count}"
    }
    else
      name
  }

  def codeGen(progNode:ProgNode, labels:Map[String, String] = null) :String = {
    val template =
      """#{function_name}:
        |#{block_code}
        |return #{param_count}
      """.stripMargin

    val map = MMap[String, String]()

    progNode.context = this

    map("function_name") = id.name
    map("block_code") = block.codeGen(progNode)
    map("param_count") = params.size.toString
    val result = getTemplateString(template, map.toMap)
    progNode.context = null

    result
  }

}

