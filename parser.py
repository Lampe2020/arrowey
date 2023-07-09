import tatsu
ebnf = """program                     ::= zero_to_infinite_space { expression_separator } [ expression | scope ] { expression_separator { expression_separator } [ expression | scope ] } zero_to_infinite_space ; (* Note: the script itself has to end in an `end: ` statement with one argument which can be <> <0> <1> or any integer number. If it doesn't it will run into the next wall and crash that way. *)
scope                       ::= "[" program "]" ; (* enclosing a set of instructions in squared braces sets it into an own scope *)
error_catching_scope        ::= "@" scope "_" scope [ "_" scope ];
escape_sequence             ::= "\\" ( '"' | "'" | "\\" | expression_separator ) ;
expression                  ::= ( string | regex | number | arithmetic_expression | arraylike_access | array | object | inline_if | assignment | function_definition | function_call | variable_reference | scope | error_catching_scope | ( "(" zero_to_infinite_space [ expression ] zero_to_infinite_space ")" ) ) ; (* Can be nested. *)
assignment                  ::= object_reference equal_sign expression ;
function_call               ::= [ object_reference ] identifier  ":" { " " expression } ;
object_reference            ::= [ expression "." { flagless_variable_reference "." } ];
function_definition         ::= variable_reference { " " variable_reference } " " scope ;
expression_separator        ::= ( zero_to_infinite_space "←" zero_to_infinite_space ) | ( zero_to_infinite_space "↑" zero_to_infinite_space ) | ( zero_to_infinite_space "↓" zero_to_infinite_space ) | ( zero_to_infinite_space "→" zero_to_infinite_space ) ;
variable_reference          ::= [ "g" ] [ "c" | "i" | "d" ] flagless_variable_reference [ "." ( variable_reference | function_call | assignment ) ] ;
flagless_variable_reference ::= "<" [ ( "0" | "1" | identifier ) ] ">" ;
identifier                  ::= ( letter | "_" ) { ( letter | digit | "_" ) } ;
string                      ::= ( '"' [ { #'[^"]' | '\\"' } #"[^\\]" ] '"' ) | ( "'" [ { #"[^']" | "\\'" } #"[^\\]" ] "'" ) ;
regex                       ::= '/' [ { #'[^/]' | '\\/' } #"[^\\]" ] '/' { "g" | "i" | "m" | "s" | "u" | "y" } ;
object                      ::= "{" { ( string | variable_reference ) equal_sign expression "," zero_to_infinite_space } "}" ; (* Maybe fix it up to not require a comma after each property *)
array                       ::= [ "c" ] "a" "{" { expression "," zero_to_infinite_space } "}" ;
arraylike_access            ::= expression "{" ( integer_number | variable_reference ) [ "_" ( integer_number | variable_reference ) [ "_" ( integer_number | variable_reference ) ] ] "}" ; (* indices are built like this (see square braces as "make optional"): `{startindex[_endindex[_steplength]]}` *)
inline_if                   ::= zero_to_infinite_space ( ( "(" zero_to_infinite_space [ expression ] zero_to_infinite_space ")" ) | expression ) zero_to_infinite_space "?" zero_to_infinite_space expression zero_to_infinite_space "*" zero_to_infinite_space expression zero_to_infinite_space ;
number                      ::= integer_number | float_number ;
letter                      ::= "a" | "b" | "c" | "d" | "e" | "f" | "g"
                              | "h" | "i" | "j" | "k" | "l" | "m" | "n"
                              | "o" | "p" | "q" | "r" | "s" | "t" | "u"
                              | "v" | "w" | "x" | "y" | "z" | "A" | "B"
                              | "C" | "D" | "E" | "F" | "G" | "H" | "I"
                              | "J" | "K" | "L" | "M" | "N" | "O" | "P"
                              | "Q" | "R" | "S" | "T" | "U" | "V" | "W"
                              | "X" | "Y" | "Z" ;
digit                       ::= "0" | nonzero_digit ;
integer_number              ::=  [ negation ] nonzero_digit { positive_integer } ;
float_number                ::= ( integer_number "." positive_integer ) | "NaN" ;
nonzero_digit               ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
zero_to_infinite_space      ::= { " " } ;
negation                    ::= "-";
equal_sign                  ::= "=" ;
dot_operator                ::= "•" | ":" ;
dash_operator               ::= "+" | negation ;
operator                    ::= dot_operator | dash_operator ;
positive_integer            ::= "0" | ( nonzero_digit { digit } ) ; (* zero or any whole number not starting with zero *)
dotarithmetic_expression    ::= expression { dot_operator expression } ;
dasharithmetic_expression   ::= expression { dash_operator expression } ;
arithmetic_expression       ::= dotarithmetic_expression | dasharithmetic_expression ;"""
model = tatsu.compile(ebnf, 'arrowey')
print(model.parse("""<do_smth> <arg> [out: a{"Hello World", 3•5:3, /.*/gu, <arg>,}] → end: (do_smth: {<XD>=5,}){1} → "x"?3•3*NaN"""))