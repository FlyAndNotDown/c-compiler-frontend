from old.syntax import *

from old.lexical import *

lexical = Lexical()
lexical.put_source(open('test.c').read())
lexical.execute()

syntax = Syntax()
syntax.put_source(lexical.get_result())
syntax.execute()