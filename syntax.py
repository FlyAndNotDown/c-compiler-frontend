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
8(2). param-list2 -> param-list , param-list2 | empty
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
    def __init__(self, terminal_sign_type, terminal_sign_str, terminal_sign_line):
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


class NonTerminalSignType:
    """
    所有非终结符的类型
    """
    PROGRAMS = 0                            # programs
    DECLARATION_LIST = 1                    # declaration-list
    DECLARATION_LIST2 = 2                   # declaration-list2
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
    __productions = [
        # TODO
    ]

    @classmethod
    def __getitem__(cls, item):
        """
        复写 [] 运算符
        :param item: 索引
        :return: 产生式
        """
        return cls.__productions[item]


class PredictingAnalysisTable:
    """
    预测分析表
    """
    __table = [
        # 测试用例，到时候删掉
        [Production(NonTerminalSign(NonTerminalSignType.PROGRAMS), [])]
        # TODO，填完所有的产生式
    ]

    @classmethod
    def get_production(cls, non_terminal_sign, terminal_sign):
        """
        获取产生式
        :param non_terminal_sign: 非终结符
        :param terminal_sign: 终结符
        :return: 产生式
        """
        return cls.__table[non_terminal_sign][terminal_sign]


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