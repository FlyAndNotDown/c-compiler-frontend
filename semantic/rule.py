from semantic.symbol import *
from error import SemanticError
from semantic.code import get_temp_block_name, get_temp_var_name


"""
添加语义规则的文法
0.  program -> define-list
1.  define-list -> define define-list
                 | empty
2.  define -> type ID define-type
3.  define-type -> var-define-follow
                 | fun-define-follow
4.  var-define-follow -> ;
                 | [ NUM ] ;
5.  type ->    int
             | void
6.  fun-define-follow -> ( params ) code-block
7.  params -> param-list
                | empty
8.  param-list -> param param-follow
9. param-follow -> , param param-follow
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


# 1
class P0L(SemanticRule):
    def __rule(self, node):
        # TODO
        pass