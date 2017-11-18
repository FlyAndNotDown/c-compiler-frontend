from lexical import *


"""
原文法
1. programs -> declaration-list
2. declaration-list -> declaration-list declaration | declaration
3. declaration -> var-declaration | fun-declaration
4. var-declaration -> type-specifier ID ; | type-specifier ID [ NUM ] ;
5. type-specifier -> int | void
6. fun-declaration -> type-specifier ID ( params ) | compound-stmt
7. params -> params-list | void
8. param-list -> param-list , param | param
9. param -> type-specifier ID | type-specifier ID [ ]
10. compound-stmt -> { local-declaration statement-list }
11. local-declaration -> local-declaration var-declaration | empty
12. statement-list -> statement-list statement | empty
13. statement -> expression-stmt | compound-stmt | selection-stmt
    | iteration-stmt | return-stmt
14. expression-stmt -> expression ; | ;
15. selection-stmt -> if ( expression ) statement
                    | if ( expression ) statement else statement
16. iteration-stmt -> while ( expression ) statement
17. return-stmt -> return ; | return expression ;
18. expression -> var = expression | simple-expression
19. var -> ID | ID [ expression ]
20. simple-expression -> additive-expression relop additive-expression
                        | additive-expression
21. relop -> <= | < | > | >= | == | !=
22. additive-expression -> additive-expression addop term | term
23. addop -> + | -
24. term -> term mulop factor | factor
25. mulop -> * | /
26. factor -> ( expression ) | var | call | NUM
27. call -> ID ( args )
28. args -> arg-list | empty
29. arg-list -> arg-list , expression | expression
"""


"""
消除左递归和回溯之后的文法
1. programs -> declaration-list
2(1). declaration-list -> declaration declaration-list2
2(2). declaration-list2 -> declaration declaration-list2 | empty
3. declaration -> var-declaration | fun-declaration
4(1). var-declaration -> type-specifier ID var-declaration2
4(2). var-declaration2 -> ; | [ NUM ] ;
5. type-specifier -> int | void
6. fun-declaration -> type-specifier ID ( params ) | compound-stmt
7. params -> params-list | void
8(1). param-list -> param param-list2
8(2). param-list2 -> , param param-list2 | empty
9(1). param -> type-specifier ID param2
9(2). param2 -> [ ] | empty
10. compound-stmt -> { local-declaration statement-list }
11(1). local-declaration -> var-declaration local-declaration | empty
12(1). statement-list -> statement statement-list | empty
13. statement -> expression-stmt | compound-stmt | selection-stmt
                | iteration-stmt | return-stmt
14. expression-stmt -> expression ; | ;
15(1). selection-stmt -> if ( expression ) statement selection-stmt2
15(2). selection-stmt2 -> else statement | empty
16. iteration-stmt -> while ( expression ) statement
17(1). return-stmt -> return return-stmt2
17(2). return-stmt2 -> expression ; | ;
18. expression -> var = expression | simple-expression
19(1). var -> ID var2
19(2). var2 -> [ expression ] | empty
20(1). simple-expression -> additive-expression simple-expression2
20(2). simple-expression2 -> relop additive-expression | empty
21. relop -> <= | < | > | >= | == | !=
22(1). additive-expression -> term additive-expression2
22(2). additive-expression2 -> addop term additive-expression2 | empty
23. addop -> + | -
24(1). term -> factor term2
24(2). term2 -> mulop factor term2 | empty
25. mulop -> * | /
26. factor -> ( expression ) | var | call | NUM
27. call -> ID ( args )
28. args -> arg-list | empty
29(1). arg-list -> expression arg-list2
29(2). arg-list2 -> , expression arg-list2 | empty
"""


class Stack:
    """
    数据结构 - 栈 (使用 list 来模拟栈)
    """
    def __init__(self):
        """
        初始化
        """
        self.__stack = list()

    def push(self, elem):
        """
        入栈
        :param elem: 需要入栈的元素
        """
        self.__stack.append(elem)

    def pop(self):
        """
        栈顶元素出栈
        :return: 栈顶元素
        """
        top = self.__stack[-1]
        self.__stack.pop()
        return top

    def top(self):
        """
        获取栈顶元素
        :return: 站顶元素
        """
        return self.__stack[-1]

    def clear(self):
        """
        清空栈
        """
        self.__stack.clear()


class Sign:
    """
    终结符和非终结符的基类
    """
    def __init__(self, sign_type):
        """
        构造
        :param sign_type: 符号的类型
        """
        self.type = sign_type


class TreeNode:
    """
    树节点
    """
    def __init__(self, data, children=list()):
        """
        构造
        :param data: 节点储存的数据
        :param children: 该节点所有的孩子节点
        """
        self.data = data
        self.children = list()
        for child in children:
            self.children.append(child)


class Tree:
    """
    树
    """
    def __init__(self, root):
        """
        构造
        :param root: 根节点
        """
        self.root = root


class TerminalSign(Sign):
    """
    终结符
    """
    def __init__(self, terminal_sign_type, terminal_sign_str='', terminal_sign_line=-1):
        """
        构造
        :param terminal_sign_type: 终结符的类型
        """
        super().__init__(terminal_sign_type)
        self.__str = terminal_sign_str
        self.__line = terminal_sign_line


class NonTerminalSign(Sign):
    """
    非终结符
    """
    def __init__(self, non_terminal_sign_type):
        """
        构造
        :param non_terminal_sign_type: 非终结符的类型
        """
        super().__init__(non_terminal_sign_type)


class TerminalSignType(TokenType):
    """
    所有终结符的类型
    """
    POUND = 30                              # #
    EMPTY = 31                              # 空字


class NonTerminalSignType:
    """
    所有非终结符的类型
    """
    PROGRAMS = 0
    DECLARATION_LIST = 1
    DECLARATION_LIST2 = 2
    DEClARATION = 3
    VAR_DECLARATION = 4
    VAR_DECLARATION2 = 5
    TYPE_SPECIDIER = 6
    FUN_DECLARATION = 7
    PARAMS = 8
    PARAM_LIST = 9
    PARAM_LIST2 = 10
    PARAM = 11
    PARAM2 = 12
    COMPOUND_STMT = 13
    LOCAL_DECLARATION = 14
    STATEMENT_LIST = 15
    STATEMENT = 16
    EXPRESSION_STMT = 17
    SELECTION_STMT = 18
    SELECTION_STMT2 = 19
    ITERATION_STMT = 20
    RETURN_STMT = 21
    RETURN_STMT2 = 22
    EXPRESSION = 23
    VAR = 24
    VAR2 = 25
    SIMPLE_EXPRESSION = 26
    SIMPLE_EXPRESSION2 = 27
    RELOP = 28
    ADDITIVE_EXPRESSION = 29
    ADDITIVE_EXPRESSION2 = 30
    ADDOP = 31
    TERM = 32
    TERM2 = 33
    MULOP = 34
    FACTOR = 35
    CALL = 36
    ARGS = 37
    ARG_LIST = 38
    ARG_LIST2 = 39


class Production:
    """
    产生式
    """
    def __init__(self, non_terminal_sign, signs):
        """
        构造
        :param non_terminal_sign: 非终结符 (类)
        :param signs: 符号集合 (类集)
        """
        self.__left = non_terminal_sign
        self.__right = list()
        for sign in signs:
            self.__right.append(sign)

    def get_left(self):
        """
        获取产生式的左边
        :return: 产生式的左边
        """

    def get_right(self):
        """
        获取产生式的右边
        :return: 符号集合
        """
        return self.__right


class Grammar:
    """
    文法
    """
    productions = [
        # <0> 1. programs -> declaration-list
        Production(
            NonTerminalSign(NonTerminalSignType.PROGRAMS), [
                NonTerminalSign(NonTerminalSignType.DECLARATION_LIST)
            ]
        ),
        # <1> 2(1). declaration-list -> declaration declaration-list2
        Production(
            NonTerminalSign(NonTerminalSignType.DECLARATION_LIST), [
                NonTerminalSign(NonTerminalSignType.DEClARATION),
                NonTerminalSign(NonTerminalSignType.DECLARATION_LIST2)
            ]
        ),
        # <2> 2(2). declaration-list2 -> declaration declaration-list2 | empty
        Production(
            NonTerminalSign(NonTerminalSignType.DECLARATION_LIST2), [
                NonTerminalSign(NonTerminalSignType.DEClARATION),
                NonTerminalSign(NonTerminalSignType.DECLARATION_LIST2)
            ]
        ),
        # <3>
        Production(
            NonTerminalSign(NonTerminalSignType.DECLARATION_LIST2), [

            ]
        ),
        # <4> 3. declaration -> var-declaration | fun-declaration
        Production(
            NonTerminalSign(NonTerminalSignType.DEClARATION), [
                NonTerminalSign(NonTerminalSignType.VAR_DECLARATION)
            ]
        ),
        # <5>
        Production(
            NonTerminalSign(NonTerminalSignType.DEClARATION), [
                NonTerminalSign(NonTerminalSignType.FUN_DECLARATION)
            ]
        ),
        # <6> 4(1). var-declaration -> type-specifier ID var-declaration2
        Production(
            NonTerminalSign(NonTerminalSignType.VAR_DECLARATION), [
                NonTerminalSign(NonTerminalSignType.TYPE_SPECIDIER),
                TerminalSign(TerminalSignType.ID),
                NonTerminalSign(NonTerminalSignType.VAR_DECLARATION2)
            ]
        ),
        # <7> 4(2). var-declaration2 -> ; | [ NUM ] ;
        Production(
            NonTerminalSign(NonTerminalSignType.VAR_DECLARATION2), [
                TerminalSign(TerminalSignType.SEMICOLON)
            ]
        ),
        # <8>
        Production(
            NonTerminalSign(NonTerminalSignType.VAR_DECLARATION2), [
                TerminalSign(TerminalSignType.LEFT_BRACKET),
                TerminalSign(TerminalSignType.NUM),
                TerminalSign(TerminalSignType.RIGHT_BRACKET),
                TerminalSign(TerminalSignType.SEMICOLON)
            ]
        ),
        # <9> 5. type-specifier -> int | void
        Production(
            NonTerminalSign(NonTerminalSignType.TYPE_SPECIDIER), [
                TerminalSign(TerminalSignType.INT)
            ]
        ),
        # <10>
        Production(
            NonTerminalSign(NonTerminalSignType.TYPE_SPECIDIER), [
                TerminalSign(TerminalSignType.VOID)
            ]
        ),
        # <11> 6. fun-declaration -> type-specifier ID ( params ) | compound-stmt
        Production(
            NonTerminalSign(NonTerminalSignType.FUN_DECLARATION), [
                NonTerminalSign(NonTerminalSignType.TYPE_SPECIDIER),
                TerminalSign(TerminalSignType.ID),
                TerminalSign(TerminalSignType.LEFT_PARENTHESES),
                NonTerminalSign(NonTerminalSignType.PARAMS),
                TerminalSign(TerminalSignType.RIGHT_PARENTHESES)
            ]
        ),
        # <12>
        Production(
            NonTerminalSign(NonTerminalSignType.FUN_DECLARATION), [
                NonTerminalSign(NonTerminalSignType.COMPOUND_STMT)
            ]
        ),
        # <13> 7. params -> params-list | void
        Production(
            NonTerminalSign(NonTerminalSignType.PARAMS), [
                NonTerminalSign(NonTerminalSignType.PARAM_LIST)
            ]
        ),
        # <14>
        Production(
            NonTerminalSign(NonTerminalSignType.PARAMS), [
                TerminalSign(TerminalSignType.VOID)
            ]
        ),
        # <15> 8(1). param-list -> param param-list2
        Production(
            NonTerminalSign(NonTerminalSignType.PARAM_LIST), [
                NonTerminalSign(NonTerminalSignType.PARAM),
                NonTerminalSign(NonTerminalSignType.PARAM_LIST2)
            ]
        ),
        # <16> 8(2). param-list2 -> , param param-list2 | empty
        Production(
            NonTerminalSign(NonTerminalSignType.PARAM_LIST2), [
                TerminalSign(TerminalSignType.COMMA),
                NonTerminalSign(NonTerminalSignType.PARAM),
                NonTerminalSign(NonTerminalSignType.PARAM_LIST2)
            ]
        ),
        # <17>
        Production(
            NonTerminalSign(NonTerminalSignType.PARAM_LIST2), [

            ]
        ),
        # <18> 9(1). param -> type-specifier ID param2
        Production(
            NonTerminalSign(NonTerminalSignType.PARAM), [
                NonTerminalSign(NonTerminalSignType.TYPE_SPECIDIER),
                TerminalSign(TerminalSignType.ID),
                NonTerminalSign(NonTerminalSignType.PARAM2)
            ]
        ),
        # <19> 9(2). param2 -> [ ] | empty
        Production(
            NonTerminalSign(NonTerminalSignType.PARAM2), [
                TerminalSign(TerminalSignType.LEFT_BRACKET),
                TerminalSign(TerminalSignType.RIGHT_BRACKET)
            ]
        ),
        # <20>
        Production(
            NonTerminalSign(NonTerminalSignType.PARAM2), [

            ]
        ),
        # <21> 10. compound-stmt -> { local-declaration statement-list }
        Production(
            NonTerminalSign(NonTerminalSignType.COMPOUND_STMT), [
                TerminalSign(TerminalSignType.LEFT_BRACE),
                NonTerminalSign(NonTerminalSignType.LOCAL_DECLARATION),
                NonTerminalSign(NonTerminalSignType.STATEMENT_LIST),
                TerminalSign(TerminalSignType.RIGHT_BRACE)
            ]
        ),
        # <22> 11(1). local-declaration -> var-declaration local-declaration | empty
        Production(
            NonTerminalSign(NonTerminalSignType.LOCAL_DECLARATION), [
                NonTerminalSign(NonTerminalSignType.VAR_DECLARATION),
                NonTerminalSign(NonTerminalSignType.LOCAL_DECLARATION)
            ]
        ),
        # <23>
        Production(
            NonTerminalSign(NonTerminalSignType.LOCAL_DECLARATION), [

            ]
        ),
        # <24> 12(1). statement-list -> statement statement-list | empty
        Production(
            NonTerminalSign(NonTerminalSignType.STATEMENT_LIST), [
                NonTerminalSign(NonTerminalSignType.STATEMENT),
                NonTerminalSign(NonTerminalSignType.STATEMENT_LIST)
            ]
        ),
        # <25>
        Production(
            NonTerminalSign(NonTerminalSignType.STATEMENT_LIST), [

            ]
        ),
        # <26> 13. statement -> expression-stmt | compound-stmt | selection-stmt
        #                       | iteration-stmt | return-stmt
        Production(
            NonTerminalSign(NonTerminalSignType.STATEMENT), [
                NonTerminalSign(NonTerminalSignType.EXPRESSION_STMT)
            ]
        ),
        # <27>
        Production(
            NonTerminalSign(NonTerminalSignType.STATEMENT), [
                NonTerminalSign(NonTerminalSignType.COMPOUND_STMT)
            ]
        ),
        # <28>
        Production(
            NonTerminalSign(NonTerminalSignType.STATEMENT), [
                NonTerminalSign(NonTerminalSignType.SELECTION_STMT)
            ]
        ),
        # <29>
        Production(
            NonTerminalSign(NonTerminalSignType.STATEMENT), [
                NonTerminalSign(NonTerminalSignType.ITERATION_STMT)
            ]
        ),
        # <30>
        Production(
            NonTerminalSign(NonTerminalSignType.STATEMENT), [
                NonTerminalSign(NonTerminalSignType.RETURN_STMT)
            ]
        ),
        # <31> 14. expression-stmt -> expression ; | ;
        Production(
            NonTerminalSign(NonTerminalSignType.EXPRESSION_STMT), [
                NonTerminalSign(NonTerminalSignType.EXPRESSION),
                TerminalSign(TerminalSignType.SEMICOLON)
            ]
        ),
        # <32>
        Production(
            NonTerminalSign(NonTerminalSignType.EXPRESSION_STMT), [
                TerminalSign(TerminalSignType.SEMICOLON)
            ]
        ),
        # <33> 15(1). selection-stmt -> if ( expression ) statement selection-stmt2
        Production(
            NonTerminalSign(NonTerminalSignType.SELECTION_STMT), [
                TerminalSign(TerminalSignType.IF),
                TerminalSign(TerminalSignType.LEFT_PARENTHESES),
                NonTerminalSign(NonTerminalSignType.EXPRESSION),
                TerminalSign(TerminalSignType.RIGHT_PARENTHESES),
                NonTerminalSign(NonTerminalSignType.STATEMENT),
                NonTerminalSign(NonTerminalSignType.SELECTION_STMT2)
            ]
        ),
        # <34> 15(2) selection-stmt2 -> else statement | empty
        Production(
            NonTerminalSign(NonTerminalSignType.SELECTION_STMT2), [
                TerminalSign(TerminalSignType.ELSE),
                NonTerminalSign(NonTerminalSignType.STATEMENT)
            ]
        ),
        # <35>
        Production(
            NonTerminalSign(NonTerminalSignType.SELECTION_STMT2), [

            ]
        ),
        # <36> 16. iteration-stmt -> while ( expression ) statement
        Production(
            NonTerminalSign(NonTerminalSignType.ITERATION_STMT), [
                TerminalSign(TerminalSignType.WHILE),
                TerminalSign(TerminalSignType.LEFT_PARENTHESES),
                NonTerminalSign(NonTerminalSignType.EXPRESSION),
                TerminalSign(TerminalSignType.RIGHT_PARENTHESES),
                NonTerminalSign(NonTerminalSignType.STATEMENT)
            ]
        ),
        # <37> 17(1). return-stmt -> return return-stmt2
        Production(
            NonTerminalSign(NonTerminalSignType.RETURN_STMT), [
                TerminalSign(TerminalSignType.RETURN),
                NonTerminalSign(NonTerminalSignType.RETURN_STMT2)
            ]
        ),
        # <38> 17(2). return-stmt2 -> expression ; | ;
        Production(
            NonTerminalSign(NonTerminalSignType.RETURN_STMT2), [
                NonTerminalSign(NonTerminalSignType.EXPRESSION),
                TerminalSign(TerminalSignType.SEMICOLON)
            ]
        ),
        # <39>
        Production(
            NonTerminalSign(NonTerminalSignType.RETURN_STMT2), [
                TerminalSign(TerminalSignType.SEMICOLON)
            ]
        ),
        # <40> 18. expression -> var = expression | simple-expression
        Production(
            NonTerminalSign(NonTerminalSignType.EXPRESSION), [
                NonTerminalSign(NonTerminalSignType.VAR),
                TerminalSign(TerminalSignType.EVALUATE),
                NonTerminalSign(NonTerminalSignType.EXPRESSION)
            ]
        ),
        # <41>
        Production(
            NonTerminalSign(NonTerminalSignType.EXPRESSION), [
                NonTerminalSign(NonTerminalSignType.SIMPLE_EXPRESSION)
            ]
        ),
        # <42> 19(1). var -> ID var2
        Production(
            NonTerminalSign(NonTerminalSignType.VAR), [
                TerminalSign(TerminalSignType.ID),
                NonTerminalSign(NonTerminalSignType.VAR2)
            ]
        ),
        # <43> 19(2) var2 -> [ expression ] | empty
        Production(
            NonTerminalSign(NonTerminalSignType.VAR2), [
                TerminalSign(TerminalSignType.LEFT_BRACKET),
                NonTerminalSign(NonTerminalSignType.EXPRESSION),
                TerminalSign(TerminalSignType.RIGHT_BRACKET)
            ]
        ),
        # <44>
        Production(
            NonTerminalSign(NonTerminalSignType.VAR2), [

            ]
        ),
        # <45> 20(1). simple-expression -> additive-expression simple-expression2
        Production(
            NonTerminalSign(NonTerminalSignType.SIMPLE_EXPRESSION), [
                NonTerminalSign(NonTerminalSignType.ADDITIVE_EXPRESSION),
                NonTerminalSign(NonTerminalSignType.SIMPLE_EXPRESSION2)
            ]
        ),
        # <46> 20(2). simple-expression2 -> relop additive-expression | empty
        Production(
            NonTerminalSign(NonTerminalSignType.SIMPLE_EXPRESSION2), [
                NonTerminalSign(NonTerminalSignType.RELOP),
                NonTerminalSign(NonTerminalSignType.ADDITIVE_EXPRESSION)
            ]
        ),
        # <47>
        Production(
            NonTerminalSign(NonTerminalSignType.SIMPLE_EXPRESSION2), [

            ]
        ),
        # <48> 21. relop -> <= | < | > | >= | == | !=
        Production(
            NonTerminalSign(NonTerminalSignType.RELOP), [
                TerminalSign(TerminalSignType.SMALLER_EQUAL)
            ]
        ),
        # <49>
        Production(
            NonTerminalSign(NonTerminalSignType.RELOP), [
                TerminalSign(TerminalSignType.SMALLER)
            ]
        ),
        # <50>
        Production(
            NonTerminalSign(NonTerminalSignType.RELOP), [
                TerminalSign(TerminalSignType.BIGGER)
            ]
        ),
        # <51>
        Production(
            NonTerminalSign(NonTerminalSignType.RELOP), [
                TerminalSign(TerminalSignType.BIGGER_EQUAL)
            ]
        ),
        # <52>
        Production(
            NonTerminalSign(NonTerminalSignType.RELOP), [
                TerminalSign(TerminalSignType.EQUAL)
            ]
        ),
        # <53>
        Production(
            NonTerminalSign(NonTerminalSignType.RELOP), [
                TerminalSign(TerminalSignType.NOT_EQUAL)
            ]
        ),
        # <54> 22(1). additive-expression -> term additive-expression2
        Production(
            NonTerminalSign(NonTerminalSignType.ADDITIVE_EXPRESSION), [
                NonTerminalSign(NonTerminalSignType.TERM),
                NonTerminalSign(NonTerminalSignType.ADDITIVE_EXPRESSION2)
            ]
        ),
        # <55> 22(2). additive-expression2 -> addop term additive-expression2 | empty
        Production(
            NonTerminalSign(NonTerminalSignType.ADDITIVE_EXPRESSION2), [
                NonTerminalSign(NonTerminalSignType.ADDOP),
                NonTerminalSign(NonTerminalSignType.TERM),
                NonTerminalSign(NonTerminalSignType.ADDITIVE_EXPRESSION2)
            ]
        ),
        # <56>
        Production(
            NonTerminalSign(NonTerminalSignType.ADDITIVE_EXPRESSION2), [

            ]
        ),
        # <57> 23. addop -> + | -
        Production(
            NonTerminalSign(NonTerminalSignType.ADDOP), [
                TerminalSign(TerminalSignType.ADDITION)
            ]
        ),
        # <58>
        Production(
            NonTerminalSign(NonTerminalSignType.ADDOP), [
                TerminalSign(TerminalSignType.SUBTRACTION)
            ]
        ),
        # <59> 24(1). term -> factor term2
        Production(
            NonTerminalSign(NonTerminalSignType.TERM), [
                NonTerminalSign(NonTerminalSignType.FACTOR),
                NonTerminalSign(NonTerminalSignType.TERM2)
            ]
        ),
        # <60> 24(2). term2 -> mulop factor term2 | empty
        Production(
            NonTerminalSign(NonTerminalSignType.TERM2), [
                NonTerminalSign(NonTerminalSignType.MULOP),
                NonTerminalSign(NonTerminalSignType.FACTOR),
                NonTerminalSign(NonTerminalSignType.TERM2)
            ]
        ),
        # <61>
        Production(
            NonTerminalSign(NonTerminalSignType.TERM2), [

            ]
        ),
        # <62> 25. mulop -> * | /
        Production(
            NonTerminalSign(NonTerminalSignType.MULOP), [
                TerminalSign(TerminalSignType.MULTIPLICATION)
            ]
        ),
        # <63>
        Production(
            NonTerminalSign(NonTerminalSignType.MULOP), [
                TerminalSign(TerminalSignType.DIVISION)
            ]
        ),
        # <64> 26. factor -> ( expression ) | var | call | NUM
        Production(
            NonTerminalSign(NonTerminalSignType.FACTOR), [
                TerminalSign(TerminalSignType.LEFT_PARENTHESES),
                NonTerminalSign(NonTerminalSignType.EXPRESSION),
                TerminalSign(TerminalSignType.RIGHT_PARENTHESES)
            ]
        ),
        # <65>
        Production(
            NonTerminalSign(NonTerminalSignType.FACTOR), [
                NonTerminalSign(NonTerminalSignType.VAR)
            ]
        ),
        # <66>
        Production(
            NonTerminalSign(NonTerminalSignType.FACTOR), [
                NonTerminalSign(NonTerminalSignType.CALL)
            ]
        ),
        # <67>
        Production(
            NonTerminalSign(NonTerminalSignType.FACTOR), [
                TerminalSign(TerminalSignType.NUM)
            ]
        ),
        # <68> 27. call -> ID ( args )
        Production(
            NonTerminalSign(NonTerminalSignType.CALL), [
                TerminalSign(TerminalSignType.ID),
                TerminalSign(TerminalSignType.LEFT_PARENTHESES),
                NonTerminalSign(NonTerminalSignType.ARGS),
                TerminalSign(TerminalSignType.RIGHT_PARENTHESES)
            ]
        ),
        # <69> 28. args -> arg-list | empty
        Production(
            NonTerminalSign(NonTerminalSignType.ARGS), [
                NonTerminalSign(NonTerminalSignType.ARG_LIST)
            ]
        ),
        # <70>
        Production(
            NonTerminalSign(NonTerminalSignType.ARGS), [

            ]
        ),
        # <71> 29(1). arg-list -> expression arg-list2
        Production(
            NonTerminalSign(NonTerminalSignType.ARG_LIST), [
                NonTerminalSign(NonTerminalSignType.EXPRESSION),
                NonTerminalSign(NonTerminalSignType.ARG_LIST2)
            ]
        ),
        # <72> 29(2). arg-list2 -> , expression arg-list2 | empty
        Production(
            NonTerminalSign(NonTerminalSignType.ARG_LIST2), [
                TerminalSign(TerminalSignType.COMMA),
                NonTerminalSign(NonTerminalSignType.EXPRESSION),
                NonTerminalSign(NonTerminalSignType.ARG_LIST2)
            ]
        ),
        # <73>
        Production(
            NonTerminalSign(NonTerminalSignType.ARG_LIST2), [

            ]
        )
    ]


class PredictingAnalysisTable:
    """
    预测分析表
    """
    def __init__(self):
        """
        构造
        """
        # 预测分析表
        self.__table = list()
        # 所有非终结符
        self.__non_terminal_signs = [
            # TerminalSign(TerminalSignType.ELSE),
            # TerminalSign(TerminalSignType.IF),
            # TerminalSign(TerminalSignType.INT),
            # TerminalSign(TerminalSignType.RETURN),
            # TerminalSign(TerminalSignType.VOID),
            # TerminalSign(TerminalSignType.WHILE),
            # TerminalSign(TerminalSignType.ADDITION),
            # TerminalSign(TerminalSignType.SUBTRACTION),
            # TerminalSign(TerminalSignType.MULTIPLICATION),
            # TerminalSign(TerminalSignType.DIVISION),
            # TerminalSign(TerminalSignType.BIGGER),
            # TerminalSign(TerminalSignType.BIGGER_EQUAL),
            # TerminalSign(TerminalSignType.SMALLER),
            # TerminalSign(TerminalSignType.SMALLER_EQUAL),
            # TerminalSign(TerminalSignType.EQUAL),
            # TerminalSign(TerminalSignType.NOT_EQUAL),
            # TerminalSign(TerminalSignType.EVALUATE),
            # TerminalSign(TerminalSignType.SEMICOLON),
            # TerminalSign(TerminalSignType.COMMA),
            # TerminalSign(TerminalSignType.LEFT_PARENTHESES),
            # TerminalSign(TerminalSignType.RIGHT_PARENTHESES),
            # TerminalSign(TerminalSignType.LEFT_BRACKET),
            # TerminalSign(TerminalSignType.RIGHT_BRACKET),
            # TerminalSign(TerminalSignType.LEFT_BRACE),
            # TerminalSign(TerminalSignType.RIGHT_BRACE),
            # TerminalSign(TerminalSignType.ID),
            # TerminalSign(TerminalSignType.NUM),
            # TerminalSign(TerminalSignType.POUND),
            NonTerminalSign(NonTerminalSignType.PROGRAMS),
            NonTerminalSign(NonTerminalSignType.DECLARATION_LIST),
            NonTerminalSign(NonTerminalSignType.DECLARATION_LIST2),
            NonTerminalSign(NonTerminalSignType.DEClARATION),
            NonTerminalSign(NonTerminalSignType.VAR_DECLARATION),
            NonTerminalSign(NonTerminalSignType.VAR_DECLARATION2),
            NonTerminalSign(NonTerminalSignType.TYPE_SPECIDIER),
            NonTerminalSign(NonTerminalSignType.FUN_DECLARATION),
            NonTerminalSign(NonTerminalSignType.PARAMS),
            NonTerminalSign(NonTerminalSignType.PARAM_LIST),
            NonTerminalSign(NonTerminalSignType.PARAM_LIST2),
            NonTerminalSign(NonTerminalSignType.PARAM),
            NonTerminalSign(NonTerminalSignType.PARAM2),
            NonTerminalSign(NonTerminalSignType.COMPOUND_STMT),
            NonTerminalSign(NonTerminalSignType.LOCAL_DECLARATION),
            NonTerminalSign(NonTerminalSignType.STATEMENT_LIST),
            NonTerminalSign(NonTerminalSignType.STATEMENT),
            NonTerminalSign(NonTerminalSignType.EXPRESSION_STMT),
            NonTerminalSign(NonTerminalSignType.SELECTION_STMT),
            NonTerminalSign(NonTerminalSignType.SELECTION_STMT2),
            NonTerminalSign(NonTerminalSignType.ITERATION_STMT),
            NonTerminalSign(NonTerminalSignType.RETURN_STMT),
            NonTerminalSign(NonTerminalSignType.RETURN_STMT2),
            NonTerminalSign(NonTerminalSignType.EXPRESSION),
            NonTerminalSign(NonTerminalSignType.VAR),
            NonTerminalSign(NonTerminalSignType.VAR2),
            NonTerminalSign(NonTerminalSignType.SIMPLE_EXPRESSION),
            NonTerminalSign(NonTerminalSignType.SIMPLE_EXPRESSION2),
            NonTerminalSign(NonTerminalSignType.RELOP),
            NonTerminalSign(NonTerminalSignType.ADDITIVE_EXPRESSION),
            NonTerminalSign(NonTerminalSignType.ADDITIVE_EXPRESSION2),
            NonTerminalSign(NonTerminalSignType.ADDOP),
            NonTerminalSign(NonTerminalSignType.TERM),
            NonTerminalSign(NonTerminalSignType.TERM2),
            NonTerminalSign(NonTerminalSignType.MULOP),
            NonTerminalSign(NonTerminalSignType.FACTOR),
            NonTerminalSign(NonTerminalSignType.CALL),
            NonTerminalSign(NonTerminalSignType.ARGS),
            NonTerminalSign(NonTerminalSignType.ARG_LIST),
            NonTerminalSign(NonTerminalSignType.ARG_LIST2)
        ]
        # 所有终结符
        self.__terminal_signs = [
            TerminalSign(TerminalSignType.ELSE),
            TerminalSign(TerminalSignType.IF),
            TerminalSign(TerminalSignType.INT),
            TerminalSign(TerminalSignType.RETURN),
            TerminalSign(TerminalSignType.VOID),
            TerminalSign(TerminalSignType.WHILE),
            TerminalSign(TerminalSignType.ADDITION),
            TerminalSign(TerminalSignType.SUBTRACTION),
            TerminalSign(TerminalSignType.MULTIPLICATION),
            TerminalSign(TerminalSignType.DIVISION),
            TerminalSign(TerminalSignType.BIGGER),
            TerminalSign(TerminalSignType.BIGGER_EQUAL),
            TerminalSign(TerminalSignType.SMALLER),
            TerminalSign(TerminalSignType.SMALLER_EQUAL),
            TerminalSign(TerminalSignType.EQUAL),
            TerminalSign(TerminalSignType.NOT_EQUAL),
            TerminalSign(TerminalSignType.EVALUATE),
            TerminalSign(TerminalSignType.SEMICOLON),
            TerminalSign(TerminalSignType.COMMA),
            TerminalSign(TerminalSignType.LEFT_PARENTHESES),
            TerminalSign(TerminalSignType.RIGHT_PARENTHESES),
            TerminalSign(TerminalSignType.LEFT_BRACKET),
            TerminalSign(TerminalSignType.RIGHT_BRACKET),
            TerminalSign(TerminalSignType.LEFT_BRACE),
            TerminalSign(TerminalSignType.RIGHT_BRACE),
            TerminalSign(TerminalSignType.ID),
            TerminalSign(TerminalSignType.NUM),
            TerminalSign(TerminalSignType.POUND)
        ]
        # 非终结符的数量
        self.__non_terminal_num = 0
        # 终结符的数量
        self.__terminal_num = 0
        # 统计终结符和非终结符的数量
        for sign in self.__non_terminal_signs:
            self.__non_terminal_num += 1
        for sign in self.__terminal_signs:
            self.__terminal_num += 1
        # 根据非终结符的数量先为预测分析表分配空间并且为每一个格子预先填上 None
        for i in range(0, self.__non_terminal_num):
            self.__table.append(list())
        for i in range(0, self.__non_terminal_num):
            for j in range(0, self.__terminal_num):
                self.__table[i].append(None)
        # 为每一个非终结符建立 first 集和 follow 集
        self.__firsts = list()
        self.__follows = list()
        # 为每一个非终结符的 first 集和 follow 集分配空间
        for sign in self.__non_terminal_signs:
            self.__firsts.append(list())
            self.__follows.append(list())

    def compile(self):
        """
        编译预测分析表
        """
        # 对每一个文法元素求其 first 集
        self.__get_firsts()
        # 对每一个文法元素求其 follow 集
        self.__get_follows()
        # 根据 first 集和 follow 集生成预测分析表
        self.__generate_table()

    @classmethod
    def __set_add(cls, container, sign):
        """
        将 sign 添加到 container 中并返回 True，如果其中已经有该元素了则返回 False
        :param container: 要添加到的集合
        :param sign: 符号
        :return: 添加是否成功
        """
        exist = False
        for elem in container:
            if elem.type == sign.type:
                exist = True
        if not exist:
            container.append(sign)
        return not exist

    def __get_firsts(self):
        """
        对每一个文法元素求 first 集
        """
        # 立一个 flag，用来标志该次循环中 first 集是否增大了
        flag = True
        while flag:
            # 重置 flag
            flag = False
            # 对每一个非终结符执行如下操作
            for i in range(0, len(self.__non_terminal_signs)):
                # 遍历产生式
                for production in Grammar.productions:
                    # 如果产生式右边为空，那么则将空字添加到其 first 集中
                    if len(production.get_right()) == 0:
                        if self.__set_add(self.__firsts[i], TerminalSign(TerminalSignType.EMPTY)):
                            flag = True
                    # 如果不为空
                    else:
                        # 如果产生式右边以终结符开头，那么将其添加到 first 集中
                        if production.get_right()[0] is TerminalSign:
                            if self.__set_add(self.__firsts[i], production.get_right()[0]):
                                flag = True
                        # 如果产生式右边以非终结符 Y 开头
                        if production.get_right()[0] is NonTerminalSign:
                            # (1) 将 first(Y) 的所有非空字元素都添加到 first 集中
                            # 先找到 Y 的 first 集是哪一个
                            y_index = 0
                            for j in range(0, len(self.__non_terminal_signs)):
                                if self.__non_terminal_signs[j].type == production.get_right()[0].type:
                                    y_index = j
                            # 执行添加
                            # 该次判断中 first 集是否增大
                            bigger = False
                            for j in range(0, len(self.__firsts[y_index])):
                                # 如果不是空字
                                if self.__firsts[y_index][j].type != TerminalSignType.EMPTY:
                                    if self.__set_add(self.__firsts[i], self.__firsts[y_index][j]):
                                        bigger = True
                            if bigger:
                                flag = True

                            # (2) 寻找产生式右侧第一个 first 集中不包含空字的非终结符
                            # first 集中包含空字的最后一个非终结符在产生式中的索引
                            last = -1
                            for j in range(0, len(production.get_right())):
                                # 首先先判断是不是非终结符
                                if production.get_right()[j] is NonTerminalSign:
                                    # 找到该非终结符的 first 集
                                    index = 0
                                    for k in range(0, len(self.__non_terminal_signs)):
                                        if self.__non_terminal_signs[k].type == production.get_right()[j].type:
                                            index = k
                                    # 判断其 first 集中是否有空字
                                    empty_find = False
                                    for k in range(0, len(self.__firsts[index])):
                                        if self.__firsts[index][k].type == TerminalSignType.EMPTY:
                                            empty_find = True
                                            break
                                    # 如果含有空字，那么将 last 更新
                                    if empty_find:
                                        last = j
                                # 如果不是直接跳出
                                else:
                                    break
                            if last != -1:
                                # 如果 last 后边还有元素
                                if last < len(production.get_right()) - 1:
                                    # 如果 last 后面是终结符
                                    if production.get_right()[last + 1] is TerminalSign:
                                        if self.__set_add(self.__firsts[i], production.get_right()[last + 1]):
                                            flag = True
                                    # 如果是非终结符
                                    elif production.get_right()[last + 1] is NonTerminalSign:
                                        # 先找到后面那玩意的 first 集
                                        index = 0
                                        for j in range(0, len(self.__non_terminal_signs)):
                                            if self.__non_terminal_signs[j].type == production.get_right()[last + 1].type:
                                                index = j
                                        # 将其 first 集中的所有非空字元素添加到 first 集中
                                        bigger = False
                                        for j in range(0, len(self.__firsts[index])):
                                            # 如果不是空字
                                            if self.__firsts[index][j].type != TerminalSignType.EMPTY:
                                                if self.__set_add(self.__firsts[i], self.__firsts[index][j]):
                                                    bigger = True
                                        if bigger:
                                            flag = True
                                # 如果 last 是最后一个元素了
                                else:
                                    if self.__set_add(self.__firsts[i], TerminalSign(TerminalSignType.EMPTY)):
                                        flag = True

    def __get_follows(self):
        """
        对每一个文法元素求 follow 集
        """
        # 立一个 flag，用来标志 follow 集是否还在继续增大
        flag = True
        while flag:
            # 重置 flag
            flag = False
            # 对每一个非终结符 X 执行如下操作
            for i in range(0, len(self.__non_terminal_signs)):
                # 如果 X 是文法的开始符号，那么则将 # 至于其 follow 集中
                if self.__non_terminal_signs[i].type == NonTerminalSignType.PROGRAMS:
                    if self.__set_add(self.__follows[i], TerminalSign(TerminalSignType.POUND)):
                        flag = True
                # 开始遍历产生式
                for production in Grammar.productions:
                    # 先寻找 X 在产生式中的位置，如果为 -1 则说明没有找到
                    x_index = -1
                    for j in range(0, len(production.get_right())):
                        if self.__non_terminal_signs[i].type == production.get_right()[j].type:
                            x_index = j
                    # 如果找到了
                    if x_index != -1:
                        # 如果 X 不在产生式的末尾
                        if x_index < len(production.get_right()) - 1:
                            # 先看看 X 后面的兄弟 B 的 first 集中有没有空字
                            b_index = 0
                            # 寻找 B 的索引
                            for j in range(0, len(self.__non_terminal_signs)):
                                if self.__non_terminal_signs[j].type == production.get_left()[x_index + 1].type:
                                    b_index = j
                                    break
                            # 查看其 first 集
                            empty_find = False
                            for j in range(0, len(self.__firsts[b_index])):
                                if self.__firsts[b_index][j].type == TerminalSignType.EMPTY:
                                    empty_find = True
                                    break

                            # (1) 如果 X 后边的兄弟的 first 集中有空字
                            if empty_find:
                                # 把 follow(left) 添加到 follow(X) 中去
                                # 先寻找产生式左边非终结符的 follow 集
                                left_index = 0
                                for j in range(0, len(self.__non_terminal_signs)):
                                    if self.__non_terminal_signs[j].type == production.get_left().type:
                                        left_index = j
                                # 执行添加
                                bigger = False
                                for j in range(0, len(self.__follows[left_index])):
                                    if self.__set_add(self.__follows[i], self.__follows[left_index][j]):
                                        bigger = True
                                if bigger:
                                    flag = True
                            # (2) 如果 X 后边的兄弟的 first 集中没有空字
                            else:
                                bigger = False
                                # 将 X 后边的兄弟的 first 集中不是空字的元素添加到 follow(X) 中
                                for j in range(0, len(self.__firsts[b_index])):
                                    if self.__firsts[b_index][j].type != TerminalSignType.EMPTY:
                                        if self.__set_add(self.__follows[i], self.__firsts[b_index][j]):
                                            bigger = True
                                if bigger:
                                    flag = True
                        # 如果 X 在产生式的末尾
                        else:
                            # 把 follow(left) 添加到 follow(X) 中去
                            # 先寻找产生式左边非终结符的 follow 集
                            left_index = 0
                            for j in range(0, len(self.__non_terminal_signs)):
                                if self.__non_terminal_signs[j].type == production.get_left().type:
                                    left_index = j
                            # 执行添加
                            bigger = False
                            for j in range(0, len(self.__follows[left_index])):
                                if self.__set_add(self.__follows[i], self.__follows[left_index][j]):
                                    bigger = True
                            if bigger:
                                flag = True

    def __insert_to_table(self, production, terminal):
        """
        将产生式插入预测分析表
        :param non_terminal: 非终结符
        :param terminal: 终结符
        """
        # 先判断应该插入到的位置
        x = 0
        y = 0
        for i in range(0, len(self.__non_terminal_signs)):
            if production.get_left().type == self.__non_terminal_signs[i].type:
                x = i
                break
        for i in range(0, len(self.__terminal_signs)):
            if terminal.type == self.__terminal_signs[i].type:
                y = i

        # 执行插入
        del self.__table[x][y]
        self.__table[x].insert(y, production)

    def __generate_table(self):
        """
        根据 first 集和 follow 集构建预测分析表
        """
        # 对文法中的每一个产生式 A->a 执行如下操作
        for production in Grammar.productions:
            # 如果产生式右边不为空
            if len(production.get_right()) > 0:
                # 如果产生式首位是终结符
                if production.get_right()[0] is TerminalSign:
                    # first 集就是他本身，将其添加到 M[A,a] 中
                    self.__insert_to_table(production, production.get_right()[0])
                # 如果产生式首位是非终结符
                else:
                    # 求产生式右边的 first 集
                    index = 0
                    for i in range(0, len(self.__non_terminal_signs)):
                        if production.get_right()[0].type == self.__non_terminal_signs[i].type:
                            index = i
                            break
                    # 将这个 first 集中的所有非终结符添加到 M[A,a] 中去
                    for i in range(0, len(self.__firsts[index])):
                        if self.__firsts[index][i].type != TerminalSignType.EMPTY:
                            self.__insert_to_table(production, self.__firsts[index][i])

                    # 另外，如果这个 first 集中包括空字，那么对于 b in follow(A)，把 A->a 添加到 M[A,b] 中去
                    # 先寻找 A 的 follow 集
                    a_index = 0
                    for i in range(0, len(self.__non_terminal_signs)):
                        if self.__non_terminal_signs[i].type == production.get_left().type:
                            a_index = i
                            break
                    # 执行操作
                    for i in range(0, len(self.__follows[a_index])):
                        if self.__follows[a_index][i].type != TerminalSignType.EMPTY:
                            self.__insert_to_table(production, self.__follows[a_index][i])
            # 如果产生式右边为空
            else:
                # 对于 b in follow(A)，把 A->a 添加到 M[A,b] 中
                # 先寻找 A 的 follow 集
                a_index = 0
                for i in range(0, len(self.__non_terminal_signs)):
                    if self.__non_terminal_signs[i].type == production.get_left().type:
                        a_index = i
                        break
                # 执行操作
                for i in range(0, len(self.__follows[a_index])):
                    if self.__follows[a_index][i].type != TerminalSignType.EMPTY:
                        self.__insert_to_table(production, self.__follows[a_index][i])

    def get_production(self, non_terminal_sign, terminal_sign):
        """
        获取产生式
        :param non_terminal_sign: 非终结符
        :param terminal_sign: 终结符
        :return: 产生式
        """
        return self.__table[non_terminal_sign][terminal_sign]


class Syntax:
    """
    语法分析器
    """
    def __init__(self):
        """
        构造
        """
        self.__source = list()
        self.__grammar_tree = None
        self.__error = None

    def __put_source(self, source):
        """
        载入 tokens
        :param source: 词法分析得到的 token 列表
        """
        # 清空 __source
        self.__source.clear()
        # 将 tokens 转换成终结符并添加到 __source 中
        for s in source:
            self.__source.append(TerminalSign(s.type, s.str, s.line))

    def execute(self):
        """
        执行语法分析
        :return: 语法分析是否通过
        """
        # 新建语法树
        grammar_tree = Tree(TreeNode(NonTerminalSign(NonTerminalSignType.PROGRAMS)))
        # 新建栈
        stack = Stack()
        # 新建一个输入串，并且将 __source 中的内容拷贝到其中
        inputs = list()
        for s in self.__source:
            inputs.append(s)
        # 在输入串的末尾添加一个 # 终结符
        inputs.append(TerminalSign(TerminalSignType.POUND, '#', -1))

        # 将一个 # 入栈
        stack.push(TerminalSign(TerminalSignType.POUND, '#', -1))
        # 将语法树的根节点入栈
        stack.push(grammar_tree.root)
        # 当前读入的符号的索引
        input_index = 0
        # 立下一个 flag
        flag = True

        # 开始循环
        while flag:
            # 获取栈顶节点
            top = stack.top()
            # 如果 top 是终结符
            if top.data is TerminalSign:
                # 如果 top = inputs[input_index]
                if top.data.type == inputs[input_index].type:
                    # 如果 top == '#'
                    if top.data.type == TerminalSignType.POUND:
                        # 宣布分析成功，停止分析
                        flag = False
                    # 如果 top != '#'
                    else:
                        # 将 inputs[input_index] 的 str 和 line 数据拷贝到树的相应位置中
                        top.data.str = inputs[input_index].str
                        top.data.line = inputs[input_index].line
                        # 把 top 从栈中移除
                        stack.pop()
                        # 让 input_index 自增
                        input_index += 1
                else:
                    # TODO 报错
                    return False
            # 如果 top 是非终结符
            else:
                # 获取预测分析表中对应位置的产生式
                production = PredictingAnalysisTable.get_production(top.data.type, inputs[input_index].type)
                # 如果获取到了产生式
                if production:
                    # 将语法树按照产生式生长
                    for r in production.get_right():
                        top.data.chilren.append(r)
                    # 将栈顶元素出栈
                    stack.pop()
                    # 把 top 的孩子节点按照反序入栈
                    for i in range(len(top.data.chilren) - 1, -1):
                        stack.push(top.data.chilren[i])
                # 如果没能获取到产生式，说明存放着的是错误标志，报错
                else:
                    # TODO 报错
                    return False
        # 分析成功，返回 True
        return True
