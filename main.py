from lexical import *

lexical = Lexical()
lexical.put_source(open('test.c').read())
lexical.execute()
