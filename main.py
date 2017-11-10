from lexical import *
from symbol_table import *

# 新建符号表
symbol_table = SymbolTable()

# 新建词法分析器
lexical = Lexical()
# 装载源程序
lexical.put_source(open('test.c').read())
# 装载符号表
lexical.put_symbol_table(symbol_table)
# 执行词法分析
lexical.execute()
