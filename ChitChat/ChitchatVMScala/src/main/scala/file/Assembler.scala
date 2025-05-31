package file

import java.nio.file.{Files, Paths}

import scala.collection.mutable.{ListBuffer, Map => MMap}
import scala.io.Source

case class Assembler(filePath:String = null) {

  /**
    * returns a list of string that replaces labels into code position
    *
    * ==== Example ====
    * In this example, '#' is a comment, and a label should end with (":")
    * The comments and label are removed, and only the code is returned with
    * label names resolved.
    *
    {{{
       Input:
       # This is a test
       push 10
       push 20
       LABEL:
       add
       jmp LABEL
       LABEL2:
       jmpc LABEL2

    Intermediate output:

       Map(LABEL2 -> 4, LABEL -> 2)
       List(push 10, push 20, add, jmp LABEL, jmpc LABEL2)

    Final output:

       List(push 10, push 20, add, jmp 2, jmpc 4)
    }}}
    *
    * @param src
    * @return
    */
  def assemble(src:String = null) = {
    // map label to code line
    val labelToLine = MMap[String, Int]()
    val code = ListBuffer[String]()

    /**
      * Iterate over all the labelToLine elements (label, codeline) to replace
      * the given code that may have labels.
      *
      * @param code
      * @return
      */
    def replaceLabel(code:String) = {
      // only the whole string should match
      // "xyz abcdef abc".replaceAll("\\babc\\b", "9")
      // "xyz abcdef 9"
      (code /: labelToLine) ((acc, input) => acc.replaceAll("\\b" + input._1 + "\\b", input._2.toString))
    }

    var sourceCode = src
    if (sourceCode == null) {
      if (Files.exists(Paths.get(filePath)))
        sourceCode = Source.fromFile(filePath).mkString("")
      else
        throw new RuntimeException(s"No assembly file ${filePath}")
    }

    // from input to intermediate
    var count = 0
    sourceCode.split("\n(\r)?").map(_.trim) foreach {
      case s if s.startsWith("#") => code // ignore comment
      case s if s.contains(":") => labelToLine += (s.replace(":", "") -> count)
      case s if s.length == 0 => code // ignore blank line
      case s => code += s; count += 1
    }

    // resolve the label
    val iter1 = (code map {c => replaceLabel(c)})
    iter1.toList
  }
}
