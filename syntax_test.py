from lexical import *


"""
原文法
E -> E + T | T
T -> T * F | F
F -> ( E ) | i
"""


"""
消除左递归和回溯之后的文法
E -> T E2
E2 -> + T E2 | empty
T -> F T2
T2 -> * F T2 | empty
F -> ( E ) | i
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


class TerminalSignType:
    """
    所有终结符的类型
    """
    ADDITION = 0
    MULTIPLICATION = 1
    LEFT_PARENTHESES = 2
    RIGHT_PARENTHESES = 3
    I = 4
    POUND = 5                              # #
    EMPTY = 6                              # 空字


class NonTerminalSignType:
    """
    所有非终结符的类型
    """
    E = 0
    E2 = 1
    T = 2
    T2 = 3
    F = 4


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
        Production(
            NonTerminalSign(NonTerminalSignType.E), [
                NonTerminalSign(NonTerminalSignType.T),
                NonTerminalSign(NonTerminalSignType.E2)
            ]
        ),
        Production(
            NonTerminalSign(NonTerminalSignType.E2), [
                TerminalSign(TerminalSignType.ADDITION),
                NonTerminalSign(NonTerminalSignType.T),
                NonTerminalSign(NonTerminalSignType.E2)
            ]
        ),
        Production(
            NonTerminalSign(NonTerminalSignType.E2), [

            ]
        ),
        Production(
            NonTerminalSign(NonTerminalSignType.T), [
                NonTerminalSign(NonTerminalSignType.F),
                NonTerminalSign(NonTerminalSignType.T2)
            ]
        ),
        Production(
            NonTerminalSign(NonTerminalSignType.T2), [
                TerminalSign(TerminalSignType.MULTIPLICATION),
                NonTerminalSign(NonTerminalSignType.F),
                NonTerminalSign(NonTerminalSignType.T2)
            ]
        ),
        Production(
            NonTerminalSign(NonTerminalSignType.T2), [

            ]
        ),
        Production(
            NonTerminalSign(NonTerminalSignType.F), [
                TerminalSign(TerminalSignType.LEFT_PARENTHESES),
                NonTerminalSign(NonTerminalSignType.E),
                TerminalSign(TerminalSignType.RIGHT_PARENTHESES)
            ]
        ),
        Production(
            NonTerminalSign(NonTerminalSignType.F), [
                TerminalSign(TerminalSignType.I)
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
            NonTerminalSign(NonTerminalSignType.E),
            NonTerminalSign(NonTerminalSignType.E2),
            NonTerminalSign(NonTerminalSignType.T),
            NonTerminalSign(NonTerminalSignType.T2),
            NonTerminalSign(NonTerminalSignType.F)
        ]
        # 所有终结符
        self.__terminal_signs = [
            TerminalSign(TerminalSignType.ADDITION),
            TerminalSign(TerminalSignType.MULTIPLICATION),
            TerminalSign(TerminalSignType.LEFT_PARENTHESES),
            TerminalSign(TerminalSignType.RIGHT_PARENTHESES),
            TerminalSign(TerminalSignType.I),
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
                        if type(production.get_right()[0]) == TerminalSign:
                            if self.__set_add(self.__firsts[i], production.get_right()[0]):
                                flag = True
                        # 如果产生式右边以非终结符 Y 开头
                        if type(production.get_right()[0]) == NonTerminalSign:
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
                                if type(production.get_right()[j]) == NonTerminalSign:
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
                                    if type(production.get_right()[last + 1]) == TerminalSign:
                                        if self.__set_add(self.__firsts[i], production.get_right()[last + 1]):
                                            flag = True
                                    # 如果是非终结符
                                    elif type(production.get_right()[last + 1]) == NonTerminalSign:
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
                if self.__non_terminal_signs[i].type == NonTerminalSignType.E:
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
                if type(production.get_right()[0]) == TerminalSign:
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
        # 新建预测分析表
        pa_table = PredictingAnalysisTable()
        # 编译预测分析表
        pa_table.compile()

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
