package node

import node.codegen.Template

import scala.collection.mutable.{ListBuffer, Map => MMap}

case class CorrelationNode(override val name:String, override val id:IdNode) extends Node(name = name, id = id) with Template {
  var function_call:Function_callNode = null
  var values = ListBuffer[ValueNode]()

  /**
    * Update the values
    *
    * @param value
    * @return
    */
  def add(value:ValueNode) = {
    values += value
  }
  def add(fc:Function_callNode) = {
    function_call = fc
  }

  /** Returns all the name of the fully resolved correlated names.
    *
    * ==== Example ====
    * {{{
    *   correlation a = (s, z)
    *   correlation z = (p, q)
    *   correlation s = (k, l)
    *
    *   a.get([a,z,s]) => (p, q, k, l)
    * }}}
    *
    * ==== Idea ====
    * {{{
    *   Building a tree will tell you what is a node and what is a leaf
    *
    *    a
    *   |  \
    *   s   z
    *   |\   |\
    *   k l  p q
    * }}}
    *
    * ==== Algorithm ====
    *  1. From input correlationNames create a tree
    *  2. Given a name (a), find all the leaves
    *
    * @param correlationNodes
    * @return a set of name strings
    */
  def get(correlationNodes:List[CorrelationNode]) : List[String] = {
    util.Tree(correlationNodes).get(this.id.name)
  }

  def generate_for_function(progNode:ProgNode) = {

    val fnode = progNode.functions.find(_.id.name == function_call.id.name)
    if (fnode.isEmpty) throw new RuntimeException(s"No function ${function_call.id.name} found")

    def getPreCode(params:List[ValueNode]) = {
      /*
             read producename
             jpeekfalse END
             read price_i
             jpeekfalse END
             function_call_stack priceMatch 2
         END:
             stop
       */
      val endlabel = id.name + "_END"
      val paramsCode = new StringBuilder()
      params foreach {
        param => paramsCode ++= s"read ${param.name}\njpeekfalse ${endlabel}\n"
      }
      paramsCode ++= function_call.codeGen(progNode)
      paramsCode ++= s"${endlabel}:\nstop\n"
      paramsCode.toString()
    }

    val template =
      """
        |#{preCode}
        |#{function}
      """.stripMargin

    val map = MMap[String, String]()
    map("preCode") = getPreCode(function_call.args.values)
    map("function") = fnode.get.codeGen(progNode)
    getTemplateString(template, map.toMap)
  }

  def codeGen(progNode:ProgNode, labels:Map[String, String] = null) : String = {
    val correlationNodes = progNode.correlations.toList

    def generate_for_simple(values: List[String]) = {
      val res = new StringBuilder
      res ++= values.mkString("allexists ", " ", "\n")
      res ++= "stop\n"
      res.toString
    }

    if (function_call == null) {
      val info = get(correlationNodes)
      return generate_for_simple(info)
    }
    else {
      return generate_for_function(progNode)
    }
  }
}

