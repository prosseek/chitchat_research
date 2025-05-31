package node

import java.io.{File, FileInputStream}

import org.antlr.v4.runtime.{ANTLRInputStream, CommonTokenStream}
import parser.{ChitchatLexer, ChitchatParser}
import visitor.ChitchatVisitor

object NodeGenerator {
  def get(filePath:String) = {
    //var filePath = "./resources/example/input.txt"
    var fileInput = new File(filePath)
    var fileInputStream = new FileInputStream(fileInput)

    val input   = new ANTLRInputStream(fileInputStream)
    val lexer   = new ChitchatLexer(input)
    val tokens  = new CommonTokenStream(lexer)
    val parser  = new ChitchatParser(tokens)
    val tree    = parser.prog
    val visitor = new ChitchatVisitor
    visitor.visit(tree)
    visitor.prognode
  }
}
