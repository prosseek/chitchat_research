grammar Chitchat;

prog: (typedef | correlation | situation | schema | valuedef | function | command )+ ;

// typedef
typedef: annotation TYPE id EXT  base_type ;
base_type: id '(' expressions ')' ;

// correlation
correlation: CORRELATION id '=' '(' expressions ')' ;

// situation
situation: SITUATION id params '=' expression ;

// schema
schema: annotation SCHEMA id '=' '(' (scheme ','?)+ ')' ;
scheme: id | rep | choose;
choose: (id '|'?)+ ;
rep: '(' (id ','?)+ ')' '+';

// value
valuedef: VALUE id params '=' block ;

// function
function: FUNCTION return_type id params '=' block ;

// command
command: '{' (expression ';'?)+ '}' ;

///////////////////////////////////////
// EXPRESSION

return_type: 'int' | 'bool' ;

ids: (id ','?)+;
expressions: (expression ','?)*;
// due to mutual recursion, logic and comparion 
// is in this form not comparsion: expression ... form.
// the processor generates a Comparison/Logic node from the expression
expression: function_call | value | assignment | absolute
          | '(' expression ')'
          | expression arithmetic_operator expression
          | expression comparison_operator expression  // comparsion
          | expression logic_operator expression ;     // logic

params: '(' ( id ','? )* ')' ;
args: '(' ( value ','?)* ')' ;

value: id | constant_unit | list ;
function_call: id args ;
assignment: id '=' expression ;
absolute: '|' expression '-' expression '|' ;

while_loop: WHILE '(' expression ')' block ;
if_else: IF '(' expression ')' block (ELSE block)? ;

block: '{' expressions '}';

/////////////////////////////////

id: ID | STRING;
annotation: ('+'|'-');
arithmetic_operator: '+' | '-' | '*' | '/' ;
comparison_operator: '<'|'>'|'<='|'>=' | '==' ;
logic_operator: '&&' | '||' ;
constant_unit : constant (unit)? ;
constant: INT | FLOAT | TRUE | FALSE | CHAR ;
unit: '_km' | '_m' | '_hour' ;
unit_value: constant (unit)?;
list: '[' (value ','?)+ ']' ;

////////////////////////////////////////
// TERMINAL

TYPE: 'type';
CORRELATION: 'correlation';
SITUATION: 'situation';
EXT: 'extends';
GROUP: 'group';
SCHEMA: 'schema';
DEFINE: 'define';
SUMMARY: 'summary';
FUNCTION: 'function';
WHILE: 'while';
IF: 'if';
ELSE: 'else';
VALUE: 'value';

CHAR: '\''[a-zA-Z]'\'';
TRUE: 'true';
FALSE: 'false'; 
INT: ('+'|'-')?[0-9]+;
FLOAT: ('+'|'-')?[0-9]+'.'[0-9]+;
ID : [_a-zA-Z][a-zA-Z0-9?]* ;
STRING : '"' .*? '"' ;

COMMENT: '//' ~( '\r' | '\n' )*  -> skip ;
WS: [ \t\r\n]+ -> skip;