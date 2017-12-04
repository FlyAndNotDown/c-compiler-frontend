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
18. normal-statement-follow{code} -> var-follow{fun} = expression{fun} ;
               {code} | call-follow{fun id} ;
19. call-follow{code} -> ( call-params{fun id} )
20. call-params{code} -> call-param-list{fun}
                | empty
21. call-param-list{num code} -> expression{fun} call-param-follow{fun}
22. call-param-follow{num code names} -> , expression{fun} call-param-follow{fun}
                | empty
23. selection-statement{code} -> if ( expression{fun} ) { code-list } selection-follow
24. selection-follow{code} -> else { code-list }
               {code} | empty
25. iteration-statement -> while ( expression{fun} ) iteration-follow
26. iteration-follow{code} -> { code-list }
               {code} | code
27. return-statement{code} -> return return-follow{fun}
28. return-follow -> ;
                | expression{fun} ;
29. var-follow{code name type} -> [ expression{fun} ]
               {type} | empty
30. expression{code name bool} -> additive-expr{fun} expression-follow{fun}
31. expression-follow{bool code op name} -> rel-op additive-expr{fun}
               {bool} | empty
32. rel-op{op} -> <=
                | <
                | >
                | >=
                | ==
                | !=
33. additive-expr{name code} -> term{fun} additive-expr-follow{fun}
34. additive-expr-follow{add op code name} -> add-op term{fun} additive-expr-follow{fun}
               {add} | empty
35. add-op{op} -> +
                | -
36. term{name code} -> factor{fun} term-follow{fun}
37. term-follow{mul op code name} -> mul-op factor{fun} term-follow{fun}
               {mul} | empty
38. mul-op{op} ->     *
                | /
39. factor{name code} -> ( expression{fun} )
                | ID id-factor-follow{id fun}
                | NUM
40. id-factor-follow -> var-follow{fun}
                | ( args )
41. args{code num} -> arg-list
                | empty
42. arg-list{code num} -> expression arg-list-follow
43. arg-list-follow{code num names} -> , expression arg-list-follow
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
    @classmethod
    def get_instance(cls, rule_key, node):
        # 0
        if rule_key == 'Program0S':
            return Program0S(node)
        if rule_key == 'Program0E':
            return Program0E(node)

        # 1
        if rule_key == 'DefineList0E':
            return DefineList0E(node)
        if rule_key == 'DefineList1E':
            return DefineList1E(node)

        # 2
        if rule_key == 'Define0E':
            return Define0E(node)
        if rule_key == 'Define0C2':
            return Define0C2(node)

        # 3
        if rule_key == 'DefineType0S':
            return DefineType0S(node)
        if rule_key == 'DefineType0E':
            return DefineType0E(node)
        if rule_key == 'DefineType0C0':
            return DefineType0C0(node)
        if rule_key == 'DefineType1S':
            return DefineType1S(node)
        if rule_key == 'DefineType1C0':
            return DefineType1C0(node)
        if rule_key == 'DefineType1E':
            return DefineType1E
        # TODO 继续填写


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


class NormalStatementFollow0C0(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


class NormalStatementFollow0C2(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


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


class CallParam0C0(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


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
            node.code.append('param ' + name)


class CallParamList0C0(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


class CallParamList0C1(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


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


class CallParamFollow0C1(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


class CallParamFollow0C2(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


class CallParamFollow1E(SemanticRule):
    def __rule(self, node):
        node.num = 0
        node.code.clear()
        node.names.clear()


# 23
class SelectionStatement0E(SemanticRule):
    def __rule(self, node):
        if not node.children[2].bool:
            self.errors.append(SemanticError('if-结构中的表达式不是bool表达式'))
        else:
            for c in node.children[2].code:
                node.code.append(c)
            if_block = get_temp_block_name()
            else_block = get_temp_block_name()
            next_block = get_temp_block_name()
            node.code.append('if ' + node.children[2].name + ' goto ' + if_block)
            node.code.append(else_block + ':')
            for c in node.children[7].code:
                node.code.append(c)
            node.code.append('goto ' + next_block)
            node.code.append(if_block + ':')
            for c in node.children[5].code:
                node.code.append(c)
            node.code.append('goto ' + next_block)
            node.code.append(next_block + ':')


class SelectionStatement0C2(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


# 24
class SelectionFollow0E(SemanticRule):
    def __rule(self, node):
        for c in node.children[2].code:
            node.code.append(c)


class SelectionFollow1E(SemanticRule):
    def __rule(self, node):
        node.code.clear()


# 25
class IterationStatement0E(SemanticRule):
    def __rule(self, node):
        judge_block = get_temp_block_name()
        iteration_block = get_temp_block_name()
        next_block = get_temp_block_name()
        node.code.append(judge_block + ':')
        for c in node.children[2].code:
            node.code.append(c)
        node.code.append('if ' + node.children[2].name + ' goto ' + iteration_block)
        node.code.append('goto ' + next_block)
        node.code.append(iteration_block + ':')
        for c in node.children[4].code:
            node.code.append(c)
        node.code.append('goto ' + judge_block)
        node.code.append(next_block + ':')


class IterationStatement0C2(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


# 26
class IterationFollow0E(SemanticRule):
    def __rule(self, node):
        for c in node.children[1].code:
            node.code.append(c)


class IterationFollow1E(SemanticRule):
    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)


# 27
class ReturnStatement0E(SemanticRule):
    def __rule(self, node):
        for c in node.children[1].code:
            node.code.append(c)


class ReturnStatement0C1(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


# 28
class ReturnFollow0E(SemanticRule):
    def __rule(self, node):
        node.code.append('return')


class ReturnFollow1E(SemanticRule):
    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)
        node.code.append('return ' + node.children[0].name)


class ReturnFollow1C0(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


# 29
class VarFollow0E(SemanticRule):
    def __rule(self, node):
        node.type = 'array'
        node.name = node.children[1].name
        for c in node.children[1].code:
            node.code.append(c)


class VarFollow0C1(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


class VarFollow1E(SemanticRule):
    def __rule(self, node):
        node.type = 'var'


# 30
class Expression0E(SemanticRule):
    def __rule(self, node):
        node.bool = node.children[1].bool
        if node.children[1].bool:
            node.name = get_temp_var_name()
            for c in node.children[0].code:
                node.code.append(c)
            for c in node.children[1].code:
                node.code.append(c)
            node.code.append(node.name + ' := ' + node.children[0].name + ' '
                             + node.children[1].op + ' ' + node.children[1].name)
        else:
            node.name = node.children[0].name
            for c in node.children[0].code:
                node.code.append(c)


class Expression0C0(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


class Expression0C1(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


# 31
class ExpressionFollow0E(SemanticRule):
    def __rule(self, node):
        node.bool = True
        node.op = node.children[0].lexical
        node.name = node.children[1].name
        for c in node.children[1].code:
            node.code.append(c)


class ExpressionFollow0C1(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


class ExpressionFollow1E(SemanticRule):
    def __rule(self, node):
        node.bool = False


# 32
class RelOp0E(SemanticRule):
    def __rule(self, node):
        node.op = node.children[0].lexical


class RelOp1E(SemanticRule):
    def __rule(self, node):
        node.op = node.children[0].lexical


class RelOp2E(SemanticRule):
    def __rule(self, node):
        node.op = node.children[0].lexical


class RelOp3E(SemanticRule):
    def __rule(self, node):
        node.op = node.children[0].lexical


class RelOp4E(SemanticRule):
    def __rule(self, node):
        node.op = node.children[0].lexical


class RelOp5E(SemanticRule):
    def __rule(self, node):
        node.op = node.children[0].lexical


# 33
class AdditiveExpr0E(SemanticRule):
    def __rule(self, node):
        if node.children[1].add:
            node.name = get_temp_var_name()
            for c in node.children[0].code:
                node.code.append(c)
            for c in node.children[1].code:
                node.code.append(c)
            node.code.append(node.name + ' := ' + node.children[0].name + ' ' + node.children[1].op
                             + ' ' + node.children[1].name)
        else:
            node.name = node.children[0].name
            for c in node.children[0].code:
                node.code.append(c)


class AdditiveExpr0C0(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


class AdditiveExpr0C1(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


# 34
class AdditiveExprFollow0E(SemanticRule):
    def __rule(self, node):
        node.add = True
        node.op = node.children[0].op
        if node.children[2].add:
            node.name = get_temp_var_name()
            for c in node.children[1].code:
                node.code.append(c)
            for c in node.children[2].code:
                node.code.append(c)
            node.code.append(node.name + ' := ' + node.children[1].name + ' ' + node.children[2].op
                             + ' ' + node.children[2].name)
        else:
            node.name = node.children[1].name
            for c in node.children[1].code:
                node.code.append(c)


class AdditiveExprFollow0C1(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


class AdditiveExprFollow0C2(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


class AdditiveExprFollow1E(SemanticRule):
    def __rule(self, node):
        node.add = False


# 35
class AddOp0E(SemanticRule):
    def __rule(self, node):
        node.op = node.children[0].lexical


class AddOp1E(SemanticRule):
    def __rule(self, node):
        node.op = node.children[0].lexical


# 36
class Term0E(SemanticRule):
    def __rule(self, node):
        if node.children[1].mul:
            node.name = get_temp_var_name()
            for c in node.children[0].code:
                node.code.append(c)
            for c in node.children[1].code:
                node.code.append(c)
            node.code.append(node.name + ' := ' + node.children[0].name + ' ' + node.children[1].op
                             + ' ' + node.children[1].name)
        else:
            node.name = node.children[0].name
            for c in node.children[0].code:
                node.code.append(c)


class Term0C0(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


class Term0C1(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


# 37
class TermFollow0E(SemanticRule):
    def __rule(self, node):
        node.mul = True
        node.op = node.children[0].op
        if node.children[2].mul:
            node.name = get_temp_var_name()
            for c in node.children[1].code:
                node.code.append(c)
            for c in node.children[2].code:
                node.code.append(c)
            node.code.append(node.name + ' := ' + node.children[1].name + ' ' + node.children[2].op
                             + ' ' + node.children[2].name)
        else:
            node.name = node.children[1].name
            for c in node.children[1].code:
                node.code.append(c)


class TermFollow0C1(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


class TermFollow0C2(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


# 38
class MulOp0E(SemanticRule):
    def __rule(self, node):
        node.op = node.children[0].lexical


class MulOp1E(SemanticRule):
    def __rule(self, node):
        node.op = node.children[0].lexical


# 39
class Factor0E(SemanticRule):
    def __rule(self, node):
        for c in node.children[1].code:
            node.code.append(c)
        node.name = node.children[1].name


class Factor0C1(SemanticRule):
    def __rule(self, node):
        node.fun = node.parent.fun


class Factor1E(SemanticRule):
    def __rule(self, node):
        for c in node.children[1].code:
            node.code.append(c)
        node.name = node.children[1].name


class Factor1C1(SemanticRule):
    def __rule(self, node):
        node.id = node.get_pre_brother(1).lexical
        node.fun = node.parent.fun


class Factor2E(SemanticRule):
    def __rule(self, node):
        node.name = get_temp_var_name()
        node.code.append(node.name + ' := ' + node.children[0].lexical)


# 40
class IdFactorFollow0E(SemanticRule):
    def __rule(self, node):
        if symbol_table_pool.query(node.fun).exist(node.id):
            if node.children[0].type == 'var':
                node.name = node.id
            if node.children[0].type == 'array':
                node.name = get_temp_var_name()
                for c in node.children[0].code:
                    node.code.append(c)
                node.code.append(node.name + ' := ' + node.id + '[' + node.children[0].name + ']')
        else:
            self.errors.append('变量' + node.id + '未定义')


class IdFactorFollow1E(SemanticRule):
    def __rule(self, node):
        if symbol_table_pool.fun_table.exist(node.id):
            if node.children[1].num != symbol_table_pool.query(node.fun).get_params_num():
                self.errors.append('调用函数' + node.id + '的时候参数数量不匹配')
            else:
                for c in node.children[1].code:
                    node.code.append(c)
                node.code.append('call ' + node.id + ', ' + symbol_table_pool.query(node.fun).get_params_num())
                node.name = get_temp_var_name()
                node.code.append(node.name + ' := ' + 'result')
        else:
            self.errors.append('函数' + node.id + '未定义')


# 41
class Args0E(SemanticRule):
    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)
        node.num = node.children[0].num


class Args1E(SemanticRule):
    def __rule(self, node):
        node.code.clear()
        node.num = 0


# 42
class ArgList0E(SemanticRule):
    def __rule(self, node):
        node.num = 1 + node.children[1].num
        for c in node.children[0].code:
            node.code.append(c)
        for c in node.children[1].code:
            node.code.append(c)
        node.code.append('param ' + node.children[0].name)
        for name in node.children[1].names:
            node.code.append('param ' + name)


# 43
class ArgListFollow0E(SemanticRule):
    def __rule(self, node):
        node.num = 1 + node.children[2].num
        for c in node.children[1].code:
            node.code.append(c)
        for c in node.children[2].code:
            node.code.append(c)
        node.names.append(node.children[1].name)
        for name in node.children[2].names:
            node.names.append(name)


class ArgListFollow1E(SemanticRule):
    def __rule(self, node):
        node.num = 0
        node.code.clear()
        node.names.clear()
