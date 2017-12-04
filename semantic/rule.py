from semantic.symbol import *
from error import SemanticError
from semantic.code import get_temp_block_name, get_temp_var_name


"""
添加语义规则的文法
0.  program{code} ->{.init} define-list
1.  define-list{code} -> define define-list
                {code} | empty
2.  define{code} -> type ID define-type{type id}
3.  define-type{code .enter} ->{.judge} var-define-follow{type id}
                {code} |{.judge} fun-define-follow{return_type fun}
4.  var-define-follow{type} -> ;
                {type length} | [ NUM ] ;
5.  type ->{type}   int
         |{type} void
6.  fun-define-follow{code} -> ( params{return_type fun} ) code-block{fun}
7.  params{.create} -> param-list{id}
               {.create} | empty
8.  param-list -> param{id} param-follow{id}
9. param-follow -> , param{id} param-follow{id}
                | empty
10. param -> type ID array-subscript
11. array-subscript{type} -> [ ]
               {type} | empty
12. code-block{code} -> { local-define-list{fun} code-list{fun} }
13. local-define-list -> local-var-define{fun} local-define-list{fun}
                | empty
14. local-var-define -> type ID var-define-follow
15. code-list{code} -> code{fun} code-list{fun}
                | empty
16. code{code} -> normal-statement{fun}
                | selection-statement{fun}
                | iteration-statement{fun}
                | return-statement{fun}
17. normal-statement -> ;
                | ID normal-statement-follow{fun id}
18. normal-statement-follow{code} -> var-follow = expression ;
               {code} | call-follow{fun id} ;
19. call-follow{code} -> ( call-params{fun id} )
20. call-params{code} -> call-param-list
                | empty
21. call-param-list{num code} -> expression call-param-follow
22. call-param-follow{num code names} -> , expression call-param-follow
                | empty
23. selection-statement -> if ( expression ) { code-list } selection-follow
24. selection-follow -> else { code-list }
                | empty
25. iteration-statement -> while ( expression ) iteration-follow
26. iteration-follow -> { code-list }
                | code
27. return-statement -> return return-follow
28. return-follow -> ;
                | expression ;
29. var-follow{code name type} -> [ expression ]
               {type} | empty
30. expression{code name} -> additive-expr expression-follow
31. expression-follow -> rel-op additive-expr
                | empty
32. rel-op ->     <=
                | <
                | >
                | >=
                | ==
                | !=
33. additive-expr -> term additive-expr-follow
34. additive-expr-follow -> add-op term additive-expr-follow
                | empty
35. add-op ->     +
                | -
36. term -> factor term-follow
37. term-follow -> mul-op factor term-follow
                | empty
38. mul-op ->     *
                | /
39. factor -> ( expression )
                | ID id-factor-follow | NUM
40. id-factor-follow -> var-follow
                | ( args )
41. args -> arg-list
                | empty
42. arg-list -> expression arg-list-follow
43. arg-list-follow -> , expression arg-list-follow
                | empty
"""


# 定义一个符号表池，每次调用函数的时候使用深拷贝从这里取局部变量表
symbol_table_pool = SymbolTablePool()


class SemanticRule:
    """
    语义规则
    """
    def __init__(self, node):
        """
        构造
        :param node: 树节点
        """
        self.__node = node
        self.errors = list()

    def __rule(self, node):
        """
        实际的语义规则，需要复写
        :param node:
        """
        return []

    def execute(self):
        """
        执行语义规则
        """
        self.__rule(self.__node)

    def have_no_errors(self):
        """
        是否没有错误
        :return: 是否没有错误
        """
        return len(self.errors) == 0


class SemanticRuleFactory:
    """
    语义规则工厂，根据给出的 rule_key 返回相应的实例
    """
    def get_instance(self, rule_key, node):
        pass


# S 产生式开始
# E 产生式结束
# CN 产生式第N个元素应用之后


# 0
class Program0S(SemanticRule):
    def __rule(self, node):
        symbol_table_pool.init()


class Program0E(SemanticRule):
    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)


# 1
class DefineList0E(SemanticRule):
    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)
        for c in node.children[1].code:
            node.code.append(c)


class DefineList1E(SemanticRule):
    def __rule(self, node):
        node.code.clear()


# 2
class Define0E(SemanticRule):
    def __rule(self, node):
        for c in node.children[2].code:
            node.code.append(c)


class Define0C2(SemanticRule):
    def __rule(self, node):
        node.type = node.get_pre_brother(2).type
        node.id = node.get_pre_brother(1).lexical


# 3
class DefineType0S(SemanticRule):
    def __rule(self, node):
        # 检查 type 是否是 void
        if node.type == 'void':
            self.errors.append(SemanticError('变量' + node.id + '不能定义为void类型'))
        if node.type == 'int':
            # 检查是否重定义
            if symbol_table_pool.global_var_table.exist(node.id):
                self.errors.append(SemanticError('变量' + node.id + '重定义'))


class DefineType0E(SemanticRule):
    def __rule(self, node):
        if node.children[0].type == 'var':
            symbol_table_pool.global_var_table.append(
                GlobalVar(node.id, 'int', 4)
            )
        if node.children[0].type == 'array':
            symbol_table_pool.global_var_table.append(
                GlobalVar(node.id, 'array', 4 * node.children[0].length)
            )


class DefineType0C0(SemanticRule):
    def __rule(self, node):
        node.type = node.parent.type
        node.id = node.parent.id


class DefineType1S(SemanticRule):
    def __rule(self, node):
        # 检查是否重定义
        if symbol_table_pool.fun_table.exist(node.id):
            self.errors.append(SemanticError('函数名' + node.id + '重定义'))


class DefineType1C0(SemanticRule):
    def __rule(self, node):
        node.return_type = node.parent.type
        node.fun = node.parent.id


class DefineType1E(SemanticRule):
    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)


# 4
class VarDefineFollow0E(SemanticRule):
    def __rule(self, node):
        node.type = 'var'


class VarDefineFollow1E(SemanticRule):
    def __rule(self, node):
        node.type = 'array'
        node.length = node.children[1].lexical


# 5
class Type0S(SemanticRule):
    def __rule(self, node):
        node.type = 'int'


class Type1S(SemanticRule):
    def __rule(self, node):
        node.type = 'void'


# 6
class FunDefineFollow0E(SemanticRule):
    def __rule(self, node):
        for c in node.children[3].code:
            node.code.append(c)


class FunDefineFollow0C1(SemanticRule):
    def __rule(self, node):
        node.return_type = node.parent.return_type
        node.id = node.parent.id


class FunDefineFollow0C3(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


# 7
class Params0S(SemanticRule):
    def __rule(self, node):
        symbol_table_pool.append(
            LocalVarTable(node.id, symbol_table_pool.global_var_table)
        )
        symbol_table_pool.fun_table.append(
            Fun(node.id, node.return_type, symbol_table_pool.query(node.id))
        )


class Param0C0(SemanticRule):
    def __rule(self, node):
        node.id = node.parent.id


class Param1S(SemanticRule):
    def __rule(self, node):
        symbol_table_pool.append(
            LocalVarTable(node.id, symbol_table_pool.global_var_table)
        )
        symbol_table_pool.fun_table.append(
            Fun(node.id, node.return_type, symbol_table_pool.query(node.id))
        )


# 8
class ParamList0C0(SemanticRule):
    def __rule(self, node):
        node.id = node.parent.id


class ParamList0C2(SemanticRule):
    def __rule(self, node):
        node.id = node.parent.id


# 9
class ParamFollow0C1(SemanticRule):
    def __rule(self, node):
        node.id = node.parent.id


class ParamFollow0C2(SemanticRule):
    def __rule(self, node):
        node.id = node.parent.id


# 10
class Param0E(SemanticRule):
    def __rule(self, node):
        # 先判断 type 是否为 void
        if node.children[0].type == 'void':
            self.errors.append(SemanticError('参数' + node.children[1].lexical + '不能定义为void类型'))
        if node.children[0].type == 'int':
            # 判断是否重定义
            if symbol_table_pool.query(node.id).exist(node.children[1].lexical):
                self.errors.append(SemanticError('参数' + node.children[1].lexical + '重定义'))
            else:
                if node.children[2].type == 'array':
                    symbol_table_pool.query(node.id).append(
                        LocalVar(node.children[1].lexical, 'address', 4, True)
                    )
                if node.children[2].type == 'var':
                    symbol_table_pool.query(node.id).append(
                        LocalVar(node.children[1].lexical, 'int', 4, True)
                    )


# 11
class ArraySubscript0S(SemanticRule):
    def __rule(self, node):
        node.type = 'array'


class ArraySubscript1S(SemanticRule):
    def __rule(self, node):
        node.type = 'var'


# 12
class CodeBlock0E(SemanticRule):
    def __rule(self, node):
        node.code.append(node.id + ':')
        for c in node.children[2].code:
            node.code.append(c)


class CodeBlock0C1(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


class CodeBlock0C2(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


# 13
class LocalDefineList0C0(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


class LocalDefineList0C1(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


# 14
class LocalVarDefine0E(SemanticRule):
    def __rule(self, node):
        if node.children[0].type == 'void':
            self.errors.append(SemanticError('变量' + node.children[1].lexical + '不能定义为void类型'))
        if node.children[0].type == 'int':
            if symbol_table_pool.query(node.fun).exist(node.children[1].lexical):
                self.errors.append(SemanticError('变量' + node.children[1].lexical + '重定义'))
            else:
                if node.children[2].type == 'var':
                    symbol_table_pool.query(node.fun).append(
                        LocalVar(node.children[1].lexical, 'int', 4, False)
                    )
                if node.children[2].type == 'array':
                    symbol_table_pool.query(node.fun).append(
                        LocalVar(node.children[1].lexical, 'array', 4 * node.children[2].length, False)
                    )


# 15
class CodeList0E(SemanticRule):
    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)
        for c in node.children[1].code:
            node.code.append(c)


class CodeList0C0(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


class CodeList0C1(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


class CodeList1E(SemanticRule):
    def __rule(self, node):
        node.code.clear()


# 16
class Code0E(SemanticRule):
    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)


class Code0C0(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


class Code1E(SemanticRule):
    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)


class Code1C0(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


class Code2E(SemanticRule):
    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)


class Code2C0(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


class Code3E(SemanticRule):
    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)


class Code3C0(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


# 17
class NormalStatement0E(SemanticRule):
    def __rule(self, node):
        node.code.clear()


class NormalStatement1E(SemanticRule):
    def __rule(self, node):
        for c in node.children[1].code:
            node.code.append(c)


class NormalStatement1C1(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun
        node.id = node.get_pre_brother(1).lexical


# 18
class NormalStatementFollow0E(SemanticRule):
    def __rule(self, node):
        if node.children[0].type == 'var':
            for c in node.children[2].code:
                node.code.append(c)
            node.code.append(node.id + ' := ' + node.children[2].name)
        if node.children[0].type == 'array':
            for c in node.children[0].code:
                node.code.append(c)
            for c in node.children[2].code:
                node.code.append(c)
            node.code.append(node.id + '[' + node.children[0].name + ']' + ' := ' + node.children[2].name)


class NormalStatementFollow1E(SemanticRule):
    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)
        node.code.append('call ' + node.id + ', ' + symbol_table_pool.query(node.fun).get_params_num())


class NormalStatementFollow1C0(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun
        node.id = node.parent.id


# 19
class CallFollow0E(SemanticRule):
    def __rule(self, node):
        for c in node.children[1].code:
            node.code.append(c)


class CallFollow0C1(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun
        node.id = node.parent.id


# 20
class CallParams0E(SemanticRule):
    def __rule(self, node):
        if symbol_table_pool.query(node.fun).get_params_num() != node.children[0].num:
            self.errors.append(SemanticError('函数体' + node.fun + '调用' + node.id + '的时候，参数数量不匹配'))
        else:
            for c in node.children[0].code:
                node.code.append(c)


class CallParams1E(SemanticRule):
    def __rule(self, node):
        if symbol_table_pool.query(node.fun).get_params_num() != 0:
            self.errors.append(SemanticError('函数体' + node.fun + '调用' + node.id + '的时候，参数数量不匹配'))


# 21
class CallParamList0E(SemanticRule):
    def __rule(self, node):
        node.num = 1 + node.children[1].num
        for c in node.children[0].code:
            node.code.append(c)
        for c in node.children[1].code:
            node.code.append(c)
        node.code.append('param ' + node.children[0].name)
        for name in node.children[1].names:
            node.code.append('param' + name)


# 22
class CallParamFollow0E(SemanticRule):
    def __rule(self, node):
        node.num = 1 + node.children[2].num
        for c in node.children[1].code:
            node.code.append(c)
        for c in node.children[2].code:
            node.code.append(c)
        node.names.append(node.children[1].name)
        for n in node.children[2].names:
            node.names.append(n)


class CallParamFollow1E(SemanticRule):
    def __rule(self, node):
        node.num = 0
        node.code.clear()
        node.names.clear()


