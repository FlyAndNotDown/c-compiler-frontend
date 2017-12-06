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
                {code} |{.judge} fun-define-follow{type fun}
4.  var-define-follow{type} -> ;
                {type length} | [ NUM ] ;
5.  type ->{type}   int
         |{type} void
6.  fun-define-follow{code} -> ( params{type fun} ) code-block{fun}
7.  params{.create} -> param-list{fun}
               {.create} | empty
8.  param-list -> param{fun} param-follow{fun}
9. param-follow -> , param{fun} param-follow{fun}
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
23. selection-statement{code} -> if ( expression{fun} ) { code-list{fun} } selection-follow{fun}
24. selection-follow{code} -> else { code-list{fun} }
               {code} | empty
25. iteration-statement -> while ( expression{fun} ) iteration-follow{fun}
26. iteration-follow{code} -> { code-list{fun} }
               {code} | code{fun}
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
                | ( args{fun} )
41. args{code num} -> arg-list{fun}
                | empty
42. arg-list{code num} -> expression{fun} arg-list-follow{fun}
43. arg-list-follow{code num names} -> , expression{fun} arg-list-follow{fun}
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
        self.node = node
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
        self.__rule(self.node)

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
            return DefineType1E(node)

        # 4
        if rule_key == 'VarDefineFollow0E':
            return VarDefineFollow0E(node)
        if rule_key == 'VarDefineFollow1E':
            return VarDefineFollow1E(node)

        # 5
        if rule_key == 'Type0S':
            return Type0S(node)
        if rule_key == 'Type1S':
            return Type1S(node)

        # 6
        if rule_key == 'FunDefineFollow0E':
            return FunDefineFollow0E(node)
        if rule_key == 'FunDefineFollow0C1':
            return FunDefineFollow0C1(node)
        if rule_key == 'FunDefineFollow0C3':
            return FunDefineFollow0C3(node)

        # 7
        if rule_key == 'Params0S':
            return Params0S(node)
        if rule_key == 'Params0C0':
            return Params0C0(node)
        if rule_key == 'Params1S':
            return Params1S(node)

        # 8
        if rule_key == 'ParamList0C0':
            return ParamList0C0(node)
        if rule_key == 'ParamList0C1':
            return ParamList0C1(node)

        # 9
        if rule_key == 'ParamFollow0C1':
            return ParamFollow0C1(node)
        if rule_key == 'ParamFollow0C2':
            return ParamFollow0C2(node)

        # 10
        if rule_key == 'Param0E':
            return Param0E(node)

        # 11
        if rule_key == 'ArraySubscript0S':
            return ArraySubscript0S(node)
        if rule_key == 'ArraySubscript1S':
            return ArraySubscript1S(node)

        # 12
        if rule_key == 'CodeBlock0E':
            return CodeBlock0E(node)
        if rule_key == 'CodeBlock0C1':
            return CodeBlock0C1(node)
        if rule_key == 'CodeBlock0C2':
            return CodeBlock0C2(node)

        # 13
        if rule_key == 'LocalDefineList0C0':
            return LocalDefineList0C0(node)
        if rule_key == 'LocalDefineList0C1':
            return LocalDefineList0C1(node)

        # 14
        if rule_key == 'LocalVarDefine0E':
            return LocalVarDefine0E(node)

        # 15
        if rule_key == 'CodeList0E':
            return CodeList0E(node)
        if rule_key == 'CodeList0C0':
            return CodeList0C0(node)
        if rule_key == 'CodeList0C1':
            return CodeList0C1(node)
        if rule_key == 'CodeList1E':
            return CodeList1E(node)

        # 16
        if rule_key == 'Code0E':
            return Code0E(node)
        if rule_key == 'Code0C0':
            return Code0C0(node)
        if rule_key == 'Code1E':
            return Code1E(node)
        if rule_key == 'Code1C0':
            return Code1C0(node)
        if rule_key == 'Code2E':
            return Code2E(node)
        if rule_key == 'Code2C0':
            return Code2C0(node)
        if rule_key == 'Code3E':
            return Code3E(node)
        if rule_key == 'Code3C0':
            return Code3C0(node)

        # 17
        if rule_key == 'NormalStatement0E':
            return NormalStatement0E(node)
        if rule_key == 'NormalStatement1E':
            return NormalStatement1E(node)
        if rule_key == 'NormalStatement1C1':
            return NormalStatement1C1(node)

        # 18
        if rule_key == 'NormalStatementFollow0E':
            return NormalStatementFollow0E(node)
        if rule_key == 'NormalStatementFollow0C0':
            return NormalStatementFollow0C0(node)
        if rule_key == 'NormalStatementFollow0C2':
            return NormalStatementFollow0C2(node)
        if rule_key == 'NormalStatementFollow1E':
            return NormalStatementFollow1E(node)
        if rule_key == 'NormalStatementFollow1C0':
            return NormalStatementFollow1C0(node)

        # 19
        if rule_key == 'CallFollow0E':
            return CallFollow0E(node)
        if rule_key == 'CallFollow0C1':
            return CallFollow0C1(node)

        # 20
        if rule_key == 'CallParams0E':
            return CallParams0E(node)
        if rule_key == 'CallParams0C0':
            return CallParams0C0(node)
        if rule_key == 'CallParams1E':
            return CallParams1E(node)

        # 21
        if rule_key == 'CallParamList0E':
            return CallParamList0E(node)
        if rule_key == 'CallParamList0C0':
            return CallParamList0C0(node)
        if rule_key == 'CallParamList0C1':
            return CallParamList0C1(node)

        # 22
        if rule_key == 'CallParamFollow0E':
            return CallParamFollow0E(node)
        if rule_key == 'CallParamFollow0C1':
            return CallParamFollow0C1(node)
        if rule_key == 'CallParamFollow0C2':
            return CallParamFollow0C2(node)
        if rule_key == 'CallParamFollow1E':
            return CallParamFollow1E(node)

        # 23
        if rule_key == 'SelectionStatement0E':
            return SelectionStatement0E(node)
        if rule_key == 'SelectionStatement0C2':
            return SelectionStatement0C2(node)
        if rule_key == 'SelectionStatement0C5':
            return SelectionStatement0C5(node)
        if rule_key == 'SelectionStatement0C7':
            return SelectionStatement0C7(node)

        # 24
        if rule_key == 'SelectionFollow0E':
            return SelectionFollow0E(node)
        if rule_key == 'SelectionFollow0C2':
            return SelectionFollow0C2(node)
        if rule_key == 'SelectionFollow1E':
            return SelectionFollow1E(node)

        # 25
        if rule_key == 'IterationStatement0E':
            return IterationStatement0E(node)
        if rule_key == 'IterationStatement0C2':
            return IterationStatement0C2(node)
        if rule_key == 'IterationStatement0C4':
            return IterationStatement0C4(node)

        # 26
        if rule_key == 'IterationFollow0E':
            return IterationFollow0E(node)
        if rule_key == 'IterationFollow0C1':
            return IterationFollow0C1(node)
        if rule_key == 'IterationFollow1E':
            return IterationFollow1E(node)
        if rule_key == 'IterationFollow1C0':
            return IterationFollow1C0(node)

        # 27
        if rule_key == 'ReturnStatement0E':
            return ReturnStatement0E(node)
        if rule_key == 'ReturnStatement0C1':
            return ReturnStatement0C1(node)

        # 28
        if rule_key == 'ReturnFollow0E':
            return ReturnFollow0E(node)
        if rule_key == 'ReturnFollow1E':
            return ReturnFollow1E(node)
        if rule_key == 'ReturnFollow1C0':
            return ReturnFollow1C0(node)

        # 29
        if rule_key == 'VarFollow0E':
            return VarFollow0E(node)
        if rule_key == 'VarFollow0C1':
            return VarFollow0C1(node)
        if rule_key == 'VarFollow1E':
            return VarFollow1E(node)

        # 30
        if rule_key == 'Expression0E':
            return Expression0E(node)
        if rule_key == 'Expression0C0':
            return Expression0C0(node)
        if rule_key == 'Expression0C1':
            return Expression0C1(node)

        # 31
        if rule_key == 'ExpressionFollow0E':
            return ExpressionFollow0E(node)
        if rule_key == 'ExpressionFollow0C1':
            return ExpressionFollow0C1(node)
        if rule_key == 'ExpressionFollow1E':
            return ExpressionFollow1E(node)

        # 32
        if rule_key == 'RelOp0E':
            return RelOp0E(node)
        if rule_key == 'RelOp1E':
            return RelOp1E(node)
        if rule_key == 'RelOp2E':
            return RelOp2E(node)
        if rule_key == 'RelOp3E':
            return RelOp3E(node)
        if rule_key == 'RelOp4E':
            return RelOp4E(node)
        if rule_key == 'RelOp5E':
            return RelOp5E(node)

        # 33
        if rule_key == 'AdditiveExpr0E':
            return AdditiveExpr0E(node)
        if rule_key == 'AdditiveExpr0C0':
            return AdditiveExpr0C0(node)
        if rule_key == 'AdditiveExpr0C1':
            return AdditiveExpr0C1(node)

        # 34
        if rule_key == 'AdditiveExprFollow0E':
            return AdditiveExprFollow0E(node)
        if rule_key == 'AdditiveExprFollow0C1':
            return AdditiveExprFollow0C1(node)
        if rule_key == 'AdditiveExprFollow0C2':
            return AdditiveExprFollow0C2(node)
        if rule_key == 'AdditiveExprFollow1E':
            return AdditiveExprFollow1E(node)

        # 35
        if rule_key == 'AddOp0E':
            return AddOp0E(node)
        if rule_key == 'AddOp1E':
            return AddOp1E(node)

        # 36
        if rule_key == 'Term0E':
            return Term0E(node)
        if rule_key == 'Term0C0':
            return Term0C0(node)
        if rule_key == 'Term0C1':
            return Term0C1(node)

        # 37
        if rule_key == 'TermFollow0E':
            return TermFollow0E(node)
        if rule_key == 'TermFollow0C1':
            return TermFollow0C1(node)
        if rule_key == 'TermFollow0C2':
            return TermFollow0C2(node)

        # 38
        if rule_key == 'MulOp0E':
            return MulOp0E(node)
        if rule_key == 'MulOp1E':
            return MulOp1E(node)

        # 39
        if rule_key == 'Factor0E':
            return Factor0E(node)
        if rule_key == 'Factor0C1':
            return Factor0C1(node)
        if rule_key == 'Factor1E':
            return Factor1E(node)
        if rule_key == 'Factor1C1':
            return Factor1C1(node)
        if rule_key == 'Factor2E':
            return Factor2E(node)

        # 40
        if rule_key == 'IdFactorFollow0E':
            return IdFactorFollow0E(node)
        if rule_key == 'IdFactorFollow1E':
            return IdFactorFollow1E(node)
        if rule_key == 'IdFactorFollow1C1':
            return IdFactorFollow1C1(node)

        # 41
        if rule_key == 'Args0E':
            return Args0E(node)
        if rule_key == 'Args0C0':
            return Args0C0(node)
        if rule_key == 'Args1E':
            return Args1E(node)

        # 42
        if rule_key == 'ArgList0E':
            return ArgList0E(node)
        if rule_key == 'ArgList0C0':
            return ArgList0C0(node)
        if rule_key == 'ArgList0C1':
            return ArgList0C1(node)

        # 43
        if rule_key == 'ArgListFollow0E':
            return ArgListFollow0E(node)
        if rule_key == 'ArgListFollow0C1':
            return ArgListFollow0C1(node)
        if rule_key == 'ArgListFollow0C2':
            return ArgListFollow0C2(node)
        if rule_key == 'ArgListFollow1E':
            return ArgListFollow1E(node)

        return None

# S 产生式开始
# E 产生式结束
# CN 产生式第N个元素应用之后


# 0
class Program0S(SemanticRule):
    def __rule(self, node):
        symbol_table_pool.init()

    def execute(self):
        self.__rule(self.node)


class Program0E(SemanticRule):
    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)

    def execute(self):
        self.__rule(self.node)


# 1
class DefineList0E(SemanticRule):
    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)
        for c in node.children[1].code:
            node.code.append(c)

    def execute(self):
        self.__rule(self.node)


class DefineList1E(SemanticRule):
    def __rule(self, node):
        node.code.clear()

    def execute(self):
        self.__rule(self.node)


# 2
class Define0E(SemanticRule):
    def __rule(self, node):
        for c in node.children[2].code:
            node.code.append(c)

    def execute(self):
        self.__rule(self.node)


class Define0C2(SemanticRule):
    def __rule(self, node):
        node.type = node.get_pre_brother(2).type
        node.id = node.get_pre_brother(1).lexical

    def execute(self):
        self.__rule(self.node)


# 3
class DefineType0S(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        # 检查 type 是否是 void
        if node.type == 'void':
            self.errors.append(SemanticError('变量' + node.id + '不能定义为void类型'))
        if node.type == 'int':
            # 检查是否重定义
            if symbol_table_pool.global_var_table.exist(node.id):
                self.errors.append(SemanticError('变量' + node.id + '重定义'))


class DefineType0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

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
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.type = node.parent.type
        node.id = node.parent.id


class DefineType1S(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        # 检查是否重定义
        if symbol_table_pool.fun_table.exist(node.id):
            self.errors.append(SemanticError('函数名' + node.id + '重定义'))


class DefineType1C0(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.type = node.parent.type
        node.fun = node.parent.id


class DefineType1E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)


# 4
class VarDefineFollow0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.type = 'var'


class VarDefineFollow1E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.type = 'array'
        node.length = node.children[1].lexical


# 5
class Type0S(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.type = 'int'


class Type1S(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.type = 'void'


# 6
class FunDefineFollow0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        for c in node.children[3].code:
            node.code.append(c)


class FunDefineFollow0C1(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.type = node.parent.type
        node.fun = node.parent.fun


class FunDefineFollow0C3(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


# 7
class Params0S(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        symbol_table_pool.append(
            LocalVarTable(node.fun, symbol_table_pool.global_var_table)
        )
        symbol_table_pool.fun_table.append(
            Fun(node.fun, node.type, symbol_table_pool.query(node.fun))
        )


class Params0C0(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class Params1S(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        symbol_table_pool.append(
            LocalVarTable(node.fun, symbol_table_pool.global_var_table)
        )
        symbol_table_pool.fun_table.append(
            Fun(node.fun, node.type, symbol_table_pool.query(node.fun))
        )


# 8
class ParamList0C0(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class ParamList0C1(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


# 9
class ParamFollow0C1(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class ParamFollow0C2(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


# 10
class Param0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        # 先判断 type 是否为 void
        if node.children[0].type == 'void':
            self.errors.append(SemanticError('参数' + node.children[1].lexical + '不能定义为void类型'))
        if node.children[0].type == 'int':
            # 判断是否重定义
            if symbol_table_pool.query(node.fun).exist(node.children[1].lexical):
                self.errors.append(SemanticError('参数' + node.children[1].lexical + '重定义'))
            else:
                if node.children[2].type == 'array':
                    symbol_table_pool.query(node.fun).append(
                        LocalVar(node.children[1].lexical, 'address', 4, True)
                    )
                if node.children[2].type == 'var':
                    symbol_table_pool.query(node.fun).append(
                        LocalVar(node.children[1].lexical, 'int', 4, True)
                    )


# 11
class ArraySubscript0S(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.type = 'array'


class ArraySubscript1S(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.type = 'var'


# 12
class CodeBlock0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.code.append(node.fun + ':')
        for c in node.children[2].code:
            node.code.append(c)


class CodeBlock0C1(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class CodeBlock0C2(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


# 13
class LocalDefineList0C0(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class LocalDefineList0C1(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


# 14
class LocalVarDefine0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

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
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)
        for c in node.children[1].code:
            node.code.append(c)


class CodeList0C0(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class CodeList0C1(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class CodeList1E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.code.clear()


# 16
class Code0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)


class Code0C0(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class Code1E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)


class Code1C0(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class Code2E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)


class Code2C0(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class Code3E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)


class Code3C0(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


# 17
class NormalStatement0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.code.clear()


class NormalStatement1E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        for c in node.children[1].code:
            node.code.append(c)


class NormalStatement1C1(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun
        node.id = node.get_pre_brother(1).lexical


# 18
class NormalStatementFollow0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

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
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class NormalStatementFollow0C2(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class NormalStatementFollow1E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)
        node.code.append('call ' + node.id + ', ' + symbol_table_pool.query(node.fun).get_params_num())


class NormalStatementFollow1C0(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun
        node.id = node.parent.id


# 19
class CallFollow0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        for c in node.children[1].code:
            node.code.append(c)


class CallFollow0C1(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun
        node.id = node.parent.id


# 20
class CallParams0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        if symbol_table_pool.query(node.fun).get_params_num() != node.children[0].num:
            self.errors.append(SemanticError('函数体' + node.fun + '调用' + node.id + '的时候，参数数量不匹配'))
        else:
            for c in node.children[0].code:
                node.code.append(c)


class CallParams0C0(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class CallParams1E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        if symbol_table_pool.query(node.fun).get_params_num() != 0:
            self.errors.append(SemanticError('函数体' + node.fun + '调用' + node.id + '的时候，参数数量不匹配'))


# 21
class CallParamList0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

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
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class CallParamList0C1(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


# 22
class CallParamFollow0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

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
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class CallParamFollow0C2(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class CallParamFollow1E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.num = 0
        node.code.clear()
        node.names.clear()


# 23
class SelectionStatement0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

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
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class SelectionStatement0C5(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class SelectionStatement0C7(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


# 24
class SelectionFollow0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        for c in node.children[2].code:
            node.code.append(c)


class SelectionFollow0C2(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class SelectionFollow1E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.code.clear()


# 25
class IterationStatement0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

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
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class IterationStatement0C4(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


# 26
class IterationFollow0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        for c in node.children[1].code:
            node.code.append(c)


class IterationFollow0C1(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class IterationFollow1E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)


class IterationFollow1C0(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


# 27
class ReturnStatement0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        for c in node.children[1].code:
            node.code.append(c)


class ReturnStatement0C1(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


# 28
class ReturnFollow0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.code.append('return')


class ReturnFollow1E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)
        node.code.append('return ' + node.children[0].name)


class ReturnFollow1C0(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


# 29
class VarFollow0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.type = 'array'
        node.name = node.children[1].name
        for c in node.children[1].code:
            node.code.append(c)


class VarFollow0C1(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class VarFollow1E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.type = 'var'


# 30
class Expression0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

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
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class Expression0C1(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


# 31
class ExpressionFollow0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.bool = True
        node.op = node.children[0].op
        node.name = node.children[1].name
        for c in node.children[1].code:
            node.code.append(c)


class ExpressionFollow0C1(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class ExpressionFollow1E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.bool = False


# 32
class RelOp0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.op = node.children[0].lexical


class RelOp1E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.op = node.children[0].lexical


class RelOp2E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.op = node.children[0].lexical


class RelOp3E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.op = node.children[0].lexical


class RelOp4E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.op = node.children[0].lexical


class RelOp5E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.op = node.children[0].lexical


# 33
class AdditiveExpr0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

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
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class AdditiveExpr0C1(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


# 34
class AdditiveExprFollow0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

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
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class AdditiveExprFollow0C2(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class AdditiveExprFollow1E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.add = False


# 35
class AddOp0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.op = node.children[0].lexical


class AddOp1E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.op = node.children[0].lexical


# 36
class Term0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

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
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class Term0C1(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


# 37
class TermFollow0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

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
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class TermFollow0C2(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


# 38
class MulOp0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.op = node.children[0].lexical


class MulOp1E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.op = node.children[0].lexical


# 39
class Factor0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        for c in node.children[1].code:
            node.code.append(c)
        node.name = node.children[1].name


class Factor0C1(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class Factor1E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        for c in node.children[1].code:
            node.code.append(c)
        node.name = node.children[1].name


class Factor1C1(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.id = node.get_pre_brother(1).lexical
        node.fun = node.parent.fun


class Factor2E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.name = get_temp_var_name()
        node.code.append(node.name + ' := ' + node.children[0].lexical)


# 40
class IdFactorFollow0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

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
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        if symbol_table_pool.fun_table.exist(node.id):
            if node.children[1].num != symbol_table_pool.query(node.fun).get_params_num():
                self.errors.append('调用函数' + node.id + '的时候参数数量不匹配')
            else:
                for c in node.children[1].code:
                    node.code.append(c)
                node.code.append('call ' + node.id + ', ' + str(symbol_table_pool.query(node.fun).get_params_num()))
                node.name = get_temp_var_name()
                node.code.append(node.name + ' := ' + 'result')
        else:
            self.errors.append('函数' + node.id + '未定义')


class IdFactorFollow1C1(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


# 41
class Args0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)
        node.num = node.children[0].num


class Args0C0(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class Args1E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.code.clear()
        node.num = 0


# 42
class ArgList0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.num = 1 + node.children[1].num
        for c in node.children[0].code:
            node.code.append(c)
        for c in node.children[1].code:
            node.code.append(c)
        node.code.append('param ' + node.children[0].name)
        for name in node.children[1].names:
            node.code.append('param ' + name)


class ArgList0C0(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class ArgList0C1(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


# 43
class ArgListFollow0E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.num = 1 + node.children[2].num
        for c in node.children[1].code:
            node.code.append(c)
        for c in node.children[2].code:
            node.code.append(c)
        node.names.append(node.children[1].name)
        for name in node.children[2].names:
            node.names.append(name)


class ArgListFollow0C1(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class ArgListFollow0C2(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.fun = node.parent.fun


class ArgListFollow1E(SemanticRule):
    def execute(self):
        self.__rule(self.node)

    def __rule(self, node):
        node.num = 0
        node.code.clear()
        node.names.clear()
