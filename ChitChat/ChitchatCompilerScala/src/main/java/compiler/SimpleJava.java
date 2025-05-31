package compiler;

import parser.*;
import org.antlr.v4.runtime.ANTLRInputStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;

public class SimpleJava {
    public static void main(String[] args) throws Exception {
// create a CharStream that reads from standard input
        ANTLRInputStream input = new ANTLRInputStream(System.in); // create a lexer that feeds off of input CharStream
        ChitchatLexer lexer = new ChitchatLexer(input); // create a buffer of tokens pulled from the lexer
        CommonTokenStream tokens = new CommonTokenStream(lexer); // create a parser that feeds off the tokens buffer
        ChitchatParser parser = new ChitchatParser(tokens);
        ParseTree tree = parser.prog(); // begin parsing at init rule
        System.out.println(tree.toStringTree(parser)); // print LISP-style tree
    }
}
