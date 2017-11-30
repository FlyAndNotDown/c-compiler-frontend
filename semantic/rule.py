from semantic.symbol import *
from error import SemanticError


"""
添加语义规则的文法
1.  program -> define-list
2.  define-list -> define define-list
                 | empty
3.  define -> type ID define-type
4.  define-type -> var-define-follow
                 | fun-define-follow
5.  var-define-follow -> ;
                 | [ NUM ] ;
6.  type ->    int
             | void
7.  fun-define-follow -> ( params ) code-block
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
