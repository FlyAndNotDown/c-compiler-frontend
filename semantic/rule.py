from semantic.symbol import *
from error import SemanticError


"""
添加语义规则的文法
1.  program {p.code += c0.code} -> define-list
2.  define-list {p.code += c0.code; p.code += c1.code} -> define define-list
                {p.code.clear()} | empty
3.  define {switch c2} -> type ID define-type
4.  define-type {p.var_fun = var p.type = c0.type p.length = c0.length} -> var-define-follow
                {p.var_fun = fun p.code = c0.code} | fun-define-follow
5.  var-define-follow {p.type = normal-var} -> ;
                {p.type = array; p.length = c1.lexical} | [ NUM ] ;
6.  type -> {p.type = c0.lexical}  int
            {p.type = c0.lexical} | void
7.  fun-define-follow {p.code = c3.code ...} -> ( params ) code-block
8.  params -> param-list
                | empty
9.  param-list -> param param-follow
10. param-follow -> , param param-follow
                | empty
11. param -> type ID array-subscript
12. array-subscript -> [ ]
                | empty
13. code-block -> { local-define-list code-list }
14. local-define-list -> local-var-define local-define-list
                | empty
15. local-var-define -> type ID var-define-follow
16. code-list -> code code-list
                | empty
17. code -> normal-statement
                | selection-statement
                | iteration-statement
                | return-statement
18. normal-statement -> ;
                | ID normal-statement-follow
19. normal-statement-follow -> var-follow = expression ;
                | call-follow ;
20. call-follow -> ( call-params )
21. call-params -> call-param-list
                | empty
22. call-param-list -> expression call-param-follow
23. call-param-follow -> , expression call-param-follow
                | empty
24. selection-statement -> if ( expression ) { code-list } selection-follow
25. selection-follow -> else { code-list }
                | empty
26. iteration-statement -> while ( expression ) iteration-follow
27. iteration-follow -> { code-list }
                | code
28. return-statement -> return return-follow
29. return-follow -> ;
                | expression ;
30. var-follow -> [ expression ]
                | empty
31. expression -> additive-expr expression-follow
32. expression-follow -> rel-op additive-expr
                | empty
33. rel-op ->     <=
                | <
                | >
                | >=
                | ==
                | !=
34. additive-expr -> term additive-expr-follow
35. additive-expr-follow -> add-op term additive-expr-follow
                | empty
36. add-op ->     +
                | -
37. term -> factor term-follow
38. term-follow -> mul-op factor term-follow
                | empty
39. mul-op ->     *
                | /
40. factor -> ( expression )
                | ID id-factor-follow | NUM
41. id-factor-follow -> var-follow
                | ( args )
42. args -> arg-list
                | empty
43. arg-list -> expression arg-list-follow
44. arg-list-follow -> , expression arg-list-follow
                | empty
"""


# 定义一个符号表池
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


class SemanticRuleFactory:
    """
    语义规则工厂，根据给出的 rule_key 返回相应的实例
    """
    def get_instance(self, rule_key, node):
        pass


# 1
class Program0P(SemanticRule):
    def __init__(self, node):
        super().__init__(node)

    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)
            return []


# 2(1)
class DefineList0P(SemanticRule):
    def __init__(self, node):
        super().__init__(node)

    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)
        for c in node.children[1].code:
            node.code.append(c)
        return []


# 2(2)
class DefineList1P(SemanticRule):
    def __init__(self, node):
        super().__init__(node)

    def __rule(self, node):
        node.code.clear()
        return []


# 3(1)
class Define0P(SemanticRule):
    def __init__(self, node):
        super().__init__(node)

    def __rule(self, node):
        errors = list()
        # 如果定义的是变量
        if node.children[2].var_fun == 'var':
            # 看全局变量表是否在符号表中存在，如果不存在，就创建一张全局变量表
            if not symbol_table_pool.exist('global_var'):
                symbol_table_pool.append(SymbolTable(SymbolTable.TYPE_GLOBAL_VAR, 'global_var'))

            # 然后看是否有重定义
            # 如果重定义了
            if symbol_table_pool.query('global_var').exist(node.children[1].lexical):
                errors.append(SemanticError('变量' + node.children[1].lexical + '重定义'))
            # 如果没有重定义，将其填入符号表
            else:
                # 根据定义的类型进行操作
                if node.children[0].type == 'void':
                    errors.append(SemanticError('无法定义void型变量'))
                # 如果是 int
                if node.children[0].type == 'int':
                    # 如果是一般变量
                    if node.children[2].type == 'normal_var':
                        symbol_table_pool.query('global_var').append(Symbol(node.children[1].lexical,
                                                                            Symbol.TYPE_NORMAL_VAR, 4))
                    # 如果是数组
                    if node.children[2].type == 'array':
                        symbol_table_pool.query('global_var').append(Symbol(node.children[1].lexical,
                                                                    Symbol.TYPE_ARRAY, 4 * node.children[2].length))
        # 如果定义的是函数
        if node.children[2].var_fun == 'fun':
            for c in node.children[2].code:
                node.code.append(c)


# 4(1)
class DefineType0P(SemanticRule):
    def __init__(self, node):
        super().__init__(node)

    def __rule(self, node):
        node.var_fun = 'var'
        node.type = node.children[0].type
        node.length = node.children[0].length


# 4(2)
class DefineType1P(SemanticRule):
    def __init__(self, node):
        super().__init__(node)

    def __rule(self, node):
        node.var_fun = 'fun'
        for c in node.children[0].code:
            node.code.append(c)

