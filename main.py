"""
主程序
"""
from lexical.lexical import Lexical


# 新建词法分析器
lexical = Lexical()
# 载入源代码
lexical.load_source(open('test.c').read())
# 执行词法分析
lexical_success = lexical.execute()
# 打印结果
print('词法分析是否成功:\t', lexical_success)
if lexical_success:
    lexical_result = lexical.get_result()
    print()
    print('词法分析结果:')
    for i in lexical_result:
        print(i.type, i.str, i.line)
else:
    print('错误原因:\t', lexical.get_error())