## From parse tree to node tree

ANTLR returns a parse tree from Chitchat source.
The first step is to create a node tree from the source tree.

The parse tree has the structure that maps the
input chitchat script following the chitchat grammar.
We need to process the parse tree to build a node tree.
A node tree is a simpler form of AST aiming to generate
plugins. A node tree also includes a node that has a sequence
of commands to be executed.

The generation of a node tree from a parse tree involves the following step.

1. The removal of decorative lexemes (?) such as ',' and '('
2. The connection of one type of nodes to the other.
    * In a parse tree, a typedef has expressions as a subtree that
   has expressions. In a node tree, a typedef node has a list of expression nodes.
   So we need to generate expression nodes to build a list of them to make
   it a component of a typedef node.