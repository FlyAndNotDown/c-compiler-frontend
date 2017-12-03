from semantic.symbol import *
from error import SemanticError
from semantic.code import get_temp_block_name, get_temp_var_name


"""
添加语义规则的文法
0.  program{code} ->{.init} define-list
1.  define-list{code} -> define define-list
                {code} | empty
2.  define{code} -> type ID define-type{type id}
3.  define-type{code} ->{.judge} var-define-follow{type id}
                {code} |{.judge} fun-define-follow{return_type id}
4.  var-define-follow ->{.enter} ;
                 | [ NUM{.enter} ] ;
5.  type ->{type}   int
         |{type} void
6.  fun-define-follow{code} -> ( params{return_type id} ) code-block{id}
7.  params{.enter} -> param-list
               {.enter} | empty
8.  param-list{param_types param_names} -> param param-follow
9. param-follow{.judge} -> , param param-follow
                | empty
10. param -> type ID array-subscript
11. array-subscript -> [ ]
                | empty
12. code-block -> { local-define-list code-list }
13. local-define-list -> local-var-define local-define-list
                | empty
14. local-var-define -> type ID var-define-follow
15. code-list -> code code-list
                | empty
16. code -> normal-statement
                | selection-statement
                | iteration-statement
                | return-statement
17. normal-statement -> ;
                | ID normal-statement-follow
18. normal-statement-follow -> var-follow = expression ;
                | call-follow ;
19. call-follow -> ( call-params )
20. call-params -> call-param-list
                | empty
21. call-param-list -> expression call-param-follow
22. call-param-follow -> , expression call-param-follow
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
29. var-follow -> [ expression ]
                | empty
30. expression -> additive-expr expression-follow
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


class DefineType0C0(SemanticRule):
    def __rule(self, node):
        node.type = node.parent.type
        node.id = node.parent.id


class DefineType0E(SemanticRule):
    def __rule(self, node):
        node.code.clear()


class DefineType1S(SemanticRule):
    def __rule(self, node):
        # 检查是否重定义
        if symbol_table_pool.fun_table.exist(node.id):
            self.errors.append(SemanticRule('函数名' + node.id + '重定义'))


class DefineType1C0(SemanticRule):
    def __rule(self, node):
        node.return_type = node.parent.type
        node.id = node.parent.id


class DefineType1E(SemanticRule):
    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)


# 4


# 4
class VarDefineFollow0S(SemanticRule):
    def __rule(self, node):
        symbol_table_pool.global_var_table.append(
            GlobalVar(node.id, 'int', 4)
        )


class VarDefineFollow0C1(SemanticRule):
    def __rule(self, node):
        symbol_table_pool.global_var_table.append(
            GlobalVar(node.parent.id, 'array', 4 * node.lexical)
        )


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
        node.id = node.parent.id


# 7
class Params0E(SemanticRule):
    def __rule(self, node):
        symbol_table_pool.append(
            LocalVarTable(node.id, symbol_table_pool.global_var_table)
        )
        symbol_table_pool.fun_table.append(
            Fun(node.id, node.children[0].param_types, node.return_type, symbol_table_pool.query(node.id))
        )
        for i in range(0, len(node.children[0].param_types)):
            symbol_table_pool.query(node.id).append(
                LocalVar(node.children[0].param_names[i], node.children[0].param_types[i], 4, True)
            )


class Param1E(SemanticRule):
    def __rule(self, node):
        symbol_table_pool.append(
            LocalVarTable(node.id, symbol_table_pool.global_var_table)
        )
        symbol_table_pool.fun_table.append(
            Fun(node.id, [], node.return_type, symbol_table_pool.query(node.id))
        )


# 8
class ParamList0E(SemanticRule):
    def __rule(self, node):
        node.param_types.append(node.children[0].param_type)
        node.param_names.append(node.children[0].param_name)
        for t in node.children[1].param_types:
            node.param_types.append(t)
        for n in node.children[1].param_names:
            node.param_names.append(n)


