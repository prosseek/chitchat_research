package node.codegen

import node.{AssignmentNode, FunctionNode, ExpressionsNode, TypedefNode}

import collection.mutable.{ListBuffer, Map => MMap}

/**
  * === Nomenclature ===
  * Group Node: Range/Encoding/String/Float
  * History: a extends b, b extends c => the history is [a, b, c]
  * === Idea ===
  * 1. assign map appraoch: we make a map that contains the information to fill in the template
  *
  */

trait AssignMapResolver {

  private def isParentInGroups(parentName: String) = {
    val set = Set("Range", "Encoding", "String", "Float")
    set.contains(parentName)
  }

  /** Returns an assignment map (subclass values overwrites the superclass values)
    * Given a history of typedefnodes (the later in hierarchy means superclass)
    *
    * ==== typedefNode ====
    * {{{
    * val assignments = ListBuffer[AssignmentNode]()
    * var function_call:Function_callNode = null
    * var values = ListBuffer[ValueNode]()
    * }}}
    *
    * ==== Example ====
    * {{{
    *  when a(x = 10, y = 20) -> b(x = 20) -> c (z = 30) when a < b < c (c is superclass of b)
    *  1. z = 30 (super class)
    *  2. x = 20, z = 30
    *  3. x = 10 (overwitten), y = 20, z = 30
    *  the output is (x = 10, y = 20, z = 30)
    * }}}
 *
    * @param history
    * @return
    */
  def getAssignMapFromHistory(history:List[TypedefNode]) = {
    val map = MMap[String, String]()
    history.reverse foreach {
      typeNode => {
        typeNode.assignments foreach {
          assignment => { // AssignmentNode
            val key = assignment.id.name
            map(key) = assignment.getValueInString(key)
          }
        }
      }
    }
    map
  }

  /** Returns typedef node (object) from name
    *
    * @param name
    * @param typeNodes
    * @return
    */
  def getTypeNode(name:String, typeNodes:List[TypedefNode]) = {
    val typeNode = typeNodes find (_.id.name  == name)
    if (typeNode.isEmpty) throw new RuntimeException(s"No ${name} in types")
    typeNode.get
  }

  /** Returns all the hierarchical history up to the type group (Range/Encoding/String/Float)
    * Given a range time
    *
    * ==== Example ====
    * {{{
    *  1. a extends b
    *  2. b extends c
    *  3. c extends Range
    *
    *  input : a => output [a][b][c] as a list of nodes
    * }}}
    *
    * ==== Algorithm ===
    * {{{
    *   1. get the typeNode from input (goalRangeName == a), and put it in a history
    *   2. check if goalRangeName is type group (Range/Encoding/String/Float)
    *   3. If so, stop and return the map
    *   4. If not, find parent name (b) and check 2
    *   5. Get the parent names (a, b, c) until the parent name is Range
    * }}}
    *
    * @param goalRangeName
    * @param typeNodes
    * @return
    */
  def getHistory(goalRangeName:String, typeNodes:List[TypedefNode]) = {
    val typeHierarchy = ListBuffer[TypedefNode]()

    // 1. check if the goalRangeName is in the type database
    //    set current node into the hierarchy
    val typeNode = getTypeNode(goalRangeName, typeNodes)
    typeHierarchy += typeNode

    // 2. get the parentNames and store them into database
    var parentName = typeNode.base_name
    while (!isParentInGroups(parentName)) {
      val typeNode = getTypeNode(parentName, typeNodes)
      typeHierarchy += typeNode
      parentName = typeNode.base_name
    }
    typeHierarchy.toList
  }

  /** Returns the Range with all the adjusted assignments
    * Given goalRangeName,
    *
    * ==== example ====
    * {{{
    *   1. Given
    *   -type hour extends Range(size=5, min=0, max=23, signed=false)
    *   -type markethour extends hour(min=10, max=18)
    *
    *   2. The types are stored in `val typeNodes:List[TypeNode]`
    *   3. When input == "makehour"
    *   4. Returns a map of ("name" -> "makehour, "group" -> "Range",
    *                     "size"->"5", "min"->"10", "max=18", "signed=false")
    * }}}
    *
    * ==== Algorithm ====
    *
    *  1. Find the history of parents up to one of the four type groups
    *     - markethour -> hour -> Range
    *     - hour has Assign expressions
    *  1. In reverse order, fill in the map
    *     - from hour set size/min/max/signed
    *     - from markethour update min/max
    *  1. return the map
    *
    * ==== Note ====
    *  1. It uses `getHistory` to get all the type nodes from the input to the node whose paresnt is Group Node
    *  1. It uses `getAssignMapFromHistory` to build assignment map from retrieved history of TypeNodes.
    */
  def getAssignMapFromRangeName(rangeName:String, typeNodes:List[TypedefNode]) = {
    val map = MMap[String, String]()
    map ++= Map("name" -> rangeName, "group" -> "Range")
    val history = getHistory(rangeName, typeNodes)
    map ++= getAssignMapFromHistory(history)
    map.toMap
  }
  def getAssignMapFromFloatName(floatName:String, typeNodes:List[TypedefNode]) = {
    val map = MMap[String, String]()
    map ++= Map("name" -> floatName, "group" -> "Float")
    val history = getHistory(floatName, typeNodes)
    map ++= getAssignMapFromHistory(history)
    map.toMap
  }

  /** Returns a mp that describes the String's constraints
    *
    * We support only the cases
    *
    *   1. function call
    *   1. assignment
    *
    * ==== Example ====
    * {{{
    *   +type event extends String(alphanum())
    *   +type max10 extends String(maxlength(10))
    *   +type "only a b" extends String(min = 'a', max = 'b')
    * }}}
    *
    *
    * @param stringName
    * @param typeNodes
    * @return
    */
  def getMapFromStringName(stringName:String, typeNodes:List[TypedefNode]) = {
    val map = MMap[String, String]()
    map ++= Map("name" -> stringName, "group" -> "String")

    // todo: we need more general approach
    //       we also need some structural/architectural approach for text
    //       need more documentation
    val typeNode = getTypeNode(stringName, typeNodes)
    if (typeNode.function_call != null) {
      val fname = typeNode.function_call.id.name
      if (fname == "alphanum") {
        map("type") = "assign"
        map("max") = "122" // 'Z'
        map("min") = "0" // 'a'
      }
      else {
        map("type") = "function_call"
        map("function_name") = fname
        map("value") = typeNode.function_call.args.values(0).name
      }
    }
    else if (typeNode.assignments != null) {
      val assignments = typeNode.assignments

      assignments foreach {
        assignment =>
          map("type") = "assign"
          val key = assignment.id.name
          map(key) = assignment.expression.name
      }
    }
    map.toMap
  }

  /**
    * Given a typeNodeName, it returns the group where the typeNode belongs to
    *
    * ==== Example ====
    * {{{
    * a extend b -> b extends Range
    *
    * Given a, this function returns the string "Range"
    * }}}
    *
    * @return
    */
  def getTypeGroupName(typeNodeName:String, typeNodes:List[TypedefNode]) = {
    /**
      * Given typeNode (as name, not node), finds the ultimate (the node whose parent is one of the four groups)
      * node (not name)
      *
      * ==== Example ====
      * {{{
      *  a extend b, b extends c, c extends Range
      *  getNodeWhoseParentIsTypeGroup(a) returns
      *   1. the information [c extends Range]
      *   2. as a typeNode
      * }}}
      *
      * @param typeNode
      * @return
      */
    def getNodeWhoseParentIsTypeGroup(typeNode:TypedefNode) : TypedefNode = {
      var parent = typeNode

      // make an advancement to test
      var parentName = typeNode.base_name
      while (!isParentInGroups(parentName)) {

        val result = typeNodes find (_.id.name  == parentName)
        if (result.isDefined) {
          // make an advancement, the parentName should be one of the four to break the loop
          parent = result.get
          parentName = result.get.base_name
        }
        else // error as one of the type is not in the database
          throw new RuntimeException(s"${parentName} is not in the type names (database)")
      }
      parent
    }

    // 1. find typeNode that should be in the type nodes (database)
    val _typeNode = (typeNodes find (_.id.name  == typeNodeName))
    if (_typeNode.isEmpty)
      throw new RuntimeException(s"Type ${typeNodeName} is not available")
    val typeNode = _typeNode.get

    // 2. get the group node name
    val res = getNodeWhoseParentIsTypeGroup(typeNode)
    res
  }

  /**
    * Given a type name (of a node), it calculates the final group
    * and returns
    *
    * ==== Example ====
    * {{{
    *  type a extends b -> type b extends Encoding (x, y)
    *
    *  Given a, it returns x and y as a list of strings List(x,y)
    * }}}
    * ==== Warning ====
    *  1. It assumes that the Encoding should have parameters as primary expression, not assignment.
    *     In other words `Encoding(x, y)` not `Encoding(x = 10, y = 20)`
    *  1. The typeNodeName should be in "Encoding group" otherwise, it will raise an error.
    *
    * @param typeNodeName
    */
  def getRangeNamesFromEncoding(typeNodeName:String, typeNodes:List[TypedefNode]) = {
    val typeGroupNode = getTypeGroupName(typeNodeName, typeNodes)
    if (typeGroupNode.base_name != "Encoding")
      throw new RuntimeException(s"${typeNodeName} is not in Encoding group, but ${typeGroupNode.base_name}")
    var res = ListBuffer[String]()
    // return type is typeNode
    if (typeGroupNode.values.length > 0) {
      typeGroupNode.values foreach {
        value => res += value.name
      }
    }
    res.toList
  }
}
