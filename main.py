"""
主程序
"""
from lexical.lexical import Lexical
from syntax.syntax import Syntax


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
    print()

    # 开始执行语法分析
    syntax = Syntax()
    syntax.put_source(lexical_result)
    syntax_success = syntax.execute()
    print('语法分析和语义分析是否成功\t', syntax_success)
    if syntax_success:
        print()
        print('语义分析结果:\t')
        print('三地址代码:\t')
        i = -1
        for code in syntax.get_result().root.code:
            i += 1
            print(i, '  \t', code)
    else:
        print('错误原因:\t', syntax.get_error().info, syntax.get_error().line, '行')
else:
    print('错误原因:\t', lexical.get_error().info)
