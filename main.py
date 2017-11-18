from lexical import *
from syntax_test import *

lexical = Lexical()
lexical.put_source(open('test.c').read())
lexical.execute()

syntax = Syntax()
syntax.execute()