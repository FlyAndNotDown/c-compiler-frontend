from semantic.symbol import *
from error import SemanticError


"""
添加语义规则的文法
1.  program -> {p.code = c0.code} define-list
2.  define-list {p.code = c0.code + c1.code} -> define define-list
                {p.code = None} | empty
3.  define {} -> type ID define-type
4.  define-type {p.define = 'var' p.length = c0.length} -> var-define-follow
                {p.define = 'fun' p.code = c0.code p.types = c0.types p.names = c0.names} | fun-define-follow
5.  var-define-follow {p.length = 1} -> ;
                 {p.length = c1.lexical} | [ NUM ] ;
6.  type {p.type = c0.lexical} -> int
         {p.type = c0.lexical}    | void
7.  fun-define-follow {p.code = c3.code p.types = c1.types p.names = c1.names} -> ( params ) code-block
8.  params {p.types = c0.types p.names = c0.names} -> param-list
            {p.types = None} | empty
9.  param-list {p.types = c0.type + c1.types ...} -> param param-follow
10. param-follow {p.types = c1.type + c2.types ...} -> , param param-follow
                 {p.types = None} | empty
11. param {p.type = c0.type ...} -> type ID array-subscript
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


# 2(1)
class DefineList0P(SemanticRule):
    def __init__(self, node):
        super().__init__(node)

    def __rule(self, node):
        for c in node.children[0].code:
            node.code.append(c)
        for c in node.children[1].code:
            node.code.append(c)


# 2(2)
class DefineList1P(SemanticRule):
    def __init__(self, node):
        super().__init__(node)

    def __rule(self, node):
        node.code.clear()


# 3
class Define0P(SemanticRule):
    def __init__(self, node):
        super().__init__(node)

    def __rule(self, node):
        errors = list()
        # 如果定义的是变量
        if node.children[2].define == 'var':
            # type 不能为 void
            if node.children[0].type == 'void':
                errors.append(SemanticError('不能定义void型的变量'))
            # 如果定义的是int型
            if node.children[0].type == 'int':
                # 先看一下全局变量表中有没有重定义变量
                if symbol_table_pool.get_global_var_table().exist(node.children[1].lexical):
                    errors.append(SemanticError('变量' + node.children[1].lexical + '重定义'))
                # 如果没有重定义
                else:
                    # 根据是不是数组进行全局变量的添加
                    if node.children[2].length == 1:
                        symbol_table_pool.get_global_var_table().append(
                            GlobalVarItem(node.children[1].lexical, 'int', 4)
                        )
                    else:
                        symbol_table_pool.get_global_var_table().append(
                            GlobalVarItem(node.children[1].lexical, 'array', 4 * node.children[2].length)
                        )
        # 如果定义的是函数
        if node.children[2].define == 'fun':
            # 看函数名是否重定义
            if symbol_table_pool.get_fun_table().exist(node.children[1].lexical):
                errors.append('函数' + node.children[1].lexical + '重定义')
            # 如果没有重定义
            else:
                # 填入函数表
                fun_type = ''
                fun_type += node.children[0].type + '('
                for t in node.children[2].types:
                    fun_type += t + ','
                fun_type.rstrip(',')
                fun_type += ')'
                symbol_table_pool.get_fun_table().append(
                    FunItem(node.children[1].lexical, fun_type)
                )
                # 为该函数新建一张局部变量表
                symbol_table_pool.new_local_var_table(node.children[1].lexical)
                # 添加代码
                node.code.append(node.children[1].lexical + ':')
                for c in node.children[2].code:
                    node.code.append(c)


# 4(1)
class DefineType0P(SemanticRule):
    def __init__(self, node):
        super().__init__(node)

    def __rule(self, node):
        node.define = 'var'
        node.length = node.children[0].length


# 4(2)
class DefineType1P(SemanticRule):
    def __init__(self, node):
        super().__init__(node)

    def __rule(self, node):
        node.define = 'fun'
        for c in node.children[0].code:
            node.code.append(c)
        for t in node.children[0].types:
            node.types.append(t)
        for n in node.children[0].names:
            node.names.append(n)


# 5(1)
class VarDefineFollow0P(SemanticRule):
    def __init__(self, node):
        super().__init__(node)

    def __rule(self, node):
        node.length = 1


# 5(2)
class VarDefineFollow1P(SemanticRule):
    def __init__(self, node):
        super().__init__(node)

    def __rule(self, node):
        node.length = int(node.children[1].lexical)


# 6(1)
class Type0P(SemanticRule):
    def __init__(self, node):
        super().__init__(node)

    def __rule(self, node):
        node.type = node.children[0].lexical


# 6(2)
class Type1P(SemanticRule):
    def __init__(self, node):
        super().__init__(node)

    def __rule(self, node):
        node.type = node.children[0].lexical


# 7
class FunDefineFollow0P(SemanticRule):
    def __init__(self, node):
        super().__init__(node)

    def __rule(self, node):
        for c in node.children[3].code:
            node.code.append(c)
        for t in node.children[1].types:
            node.types.append(t)
        for n in node.children[1].names:
            node.names.append(n)


# 8(1)
class Params0P(SemanticRule):
    def __init__(self, node):
        super().__init__(node)

    def __rule(self, node):
        for t in node.children[0].types:
            node.types.append(t)
        for n in node.children[0].names:
            node.names.append(n)


# 8(2)
class Params1P(SemanticRule):
    def __init__(self, node):
        super().__init__(node)

    def __rule(self, node):
        node.types.clear()
        node.names.clear()


# 9
class ParamList0P(SemanticRule):
    def __init__(self, node):
        super().__init__(node)

    def __rule(self, node):
        node.types.append(node.children[0].type)
        node.types.append(node.children[0].name)
        for t in node.children[1].types:
            node.children[1].append(t)
        for n in node.children[1].names:
            node.names.append(n)



# 10(1)
class ParamFollow0P(SemanticRule):
    def __init__(self, node):
        super().__init__(node)

    def __rule(self, node):
        node.types.append(node.children[1].type)
        node.types.append(node.children[1].name)
        for t in node.children[2].types:
            node.types.append(t)
        for n in node.children[2].names:
            node.names.append(n)


# 10(2)
class ParamFollow1P(SemanticRule):
    def __init__(self, node):
        super().__init__(node)

    def __rule(self, node):
        node.types.clear()
        node.names.claer()


