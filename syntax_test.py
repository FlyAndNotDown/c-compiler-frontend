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
        return self.__left

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
    start = NonTerminalSign(NonTerminalSignType.E)


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
            TerminalSign(TerminalSignType.POUND),
            TerminalSign(TerminalSignType.EMPTY)
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
        success = self.__generate_table()
        return success

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
            # 遍历产生式 X -> Y
            for production in Grammar.productions:
                # 寻找 x 在非终结符集中的位置
                x_index = 0
                for i in range(0, len(self.__non_terminal_signs)):
                    if production.get_left().type == self.__non_terminal_signs[i].type:
                        x_index = i
                        break
                # 如果产生式右边为空，那么则将空字添加到其 first 集中
                if len(production.get_right()) == 0:
                    if self.__set_add(self.__firsts[x_index], TerminalSign(TerminalSignType.EMPTY)):
                        flag = True
                # 如果不为空
                else:
                    # 如果产生式右边以终结符开头，那么将其添加到 first 集中
                    if type(production.get_right()[0]) == TerminalSign:
                        if self.__set_add(self.__firsts[x_index], production.get_right()[0]):
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
                                if self.__set_add(self.__firsts[x_index], self.__firsts[y_index][j]):
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
                                        break
                                # 判断其 first 集中是否有空字
                                empty_find = False
                                for k in range(0, len(self.__firsts[index])):
                                    if self.__firsts[index][k].type == TerminalSignType.EMPTY:
                                        empty_find = True
                                        break
                                # 如果含有空字，那么将 last 更新
                                if empty_find:
                                    last = j
                                else:
                                    break
                            # 如果不是直接跳出
                            else:
                                break
                        if last != -1:
                            # 如果 last 后边还有元素
                            if last < len(production.get_right()) - 1:
                                # 如果 last 后面是终结符
                                if type(production.get_right()[last + 1]) == TerminalSign:
                                    if self.__set_add(self.__firsts[x_index], production.get_right()[last + 1]):
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
                                            if self.__set_add(self.__firsts[x_index], self.__firsts[index][j]):
                                                bigger = True
                                    if bigger:
                                        flag = True
                            # 如果 last 是最后一个元素了
                            else:
                                if self.__set_add(self.__firsts[x_index], TerminalSign(TerminalSignType.EMPTY)):
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
            # 遍历产生式 A -> aBb 进行操作
            for production in Grammar.productions:
                # 查找 A 的位置
                a_index = 0
                for i in range(0, len(self.__non_terminal_signs)):
                    if production.get_left().type == self.__non_terminal_signs[i].type:
                        a_index = i
                        break

                # 如果产生式的左边是文法的开始符号
                if production.get_left().type == Grammar.start.type:
                    # 将 # 添加到 follow(A) 中去
                    if self.__set_add(self.__follows[a_index], TerminalSign(TerminalSignType.POUND)):
                        flag = True

                # 开始检测产生式右边的非终结符
                for i in range(0, len(production.get_right())):
                    # 如果不是非终结符，直接进入下次循环
                    if type(production.get_right()[i]) == TerminalSign:
                        continue
                    # 如果是非终结符
                    else:
                        # 查找当前指向的非终结符的位置
                        index = 0
                        for j in range(0, len(self.__non_terminal_signs)):
                            if production.get_right()[i].type == self.__non_terminal_signs[j].type:
                                index = j
                                break
                        # 如果该非终结符后面已经没有东西了，则将 follow(A) 添加到其 follow 集中
                        if i == len(production.get_right()) - 1:
                            bigger = False
                            for j in range(0, len(self.__follows[a_index])):
                                if self.__set_add(self.__follows[index], self.__follows[a_index][j]):
                                    bigger = True
                            if bigger:
                                flag = True
                        # 如果该非终结符后面还有东西，那么
                        else:
                            # 如果该非终结符后面是一个终结符
                            if type(production.get_right()[i + 1]) == TerminalSign:
                                # 将该终结符添加到 follow(B) 中
                                if self.__set_add(self.__follows[index], production.get_right()[i + 1]):
                                    flag = True
                            # 如果该非终结符后面是一个非终结符
                            else:
                                # 将 first(i + 1) 中的非空字元素添加到该非终结符的 follow 集中
                                # 查找 i + 1 的位置
                                index2 = 0
                                for j in range(0, len(self.__non_terminal_signs)):
                                    if production.get_right()[i + 1].type == self.__non_terminal_signs[j].type:
                                        index2 = j
                                        break
                                # 执行添加，同时判断是否有空字
                                empty_find = False
                                bigger = False
                                for j in range(0, len(self.__firsts[index2])):
                                    if self.__firsts[index2][j].type != TerminalSignType.EMPTY:
                                        if self.__set_add(self.__follows[index], self.__firsts[index2][j]):
                                            bigger = True
                                    else:
                                        empty_find = True
                                if bigger:
                                    flag = True

                                # 如果其 first 集中含有空字，则将 follow(A) 添加到 follow(B) 中
                                if empty_find:
                                    bigger = False
                                    for j in range(0, len(self.__follows[a_index])):
                                        if self.__set_add(self.__follows[index], self.__follows[a_index][j]):
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

        # 如果那个位置里面本来就已经有产生式了，报错，说明给出的文法并不是 LL(1) 文法
        if self.__table[x][y]:
            return False
        # 如果那个位置里面为空，则说明可以填入
        else:
            # 执行插入
            del self.__table[x][y]
            self.__table[x].insert(y, production)
            return True

    def __generate_table(self):
        """
        根据 first 集和 follow 集构建预测分析表
        """
        # 临时 first 集
        first = list()
        # 对文法中的每一个产生式 A->a 进行如下操作
        for production in Grammar.productions:
            # 清空 a 的临时 first 集
            first.clear()

            # 寻找 A 的位置
            a_index = 0
            for i in range(0, len(self.__non_terminal_signs)):
                if production.get_left().type == self.__non_terminal_signs[i].type:
                    a_index = i
                    break

            # 求 a 的 first 集
            # 如果 a 为空
            if len(production.get_right()) == 0:
                # 将空字添加到 a 的 first 集中去
                self.__set_add(first, TerminalSign(TerminalSignType.EMPTY))
            # 如果 a 不为空
            else:
                # 如果 a 的开头是终结符
                if type(production.get_right()[0]) == TerminalSign:
                    # 将开头的终结符添加到 a 的 first 集合中去
                    self.__set_add(first, production.get_right()[0])
                # 如果 a 的开头是非终结符
                else:
                    # (1) 将开头的非终结符的 first 集的所有非空字元素添加到 a 的 first 集中去
                    for i in range(0, len(self.__firsts[a_index])):
                        if self.__firsts[a_index][i].type != TerminalSignType.EMPTY:
                            self.__set_add(first, self.__firsts[a_index][i])

                    # (2) 寻找产生式右边的第一个 first 集中不包含空字的非终结符
                    # first 集中包含空字的最后一个非终结符在产生式中的索引
                    last = -1
                    for i in range(0, len(production.get_right())):
                        # 首先判断是不是非终结符
                        if type(production.get_right()[i]) == NonTerminalSign:
                            # 找到该终结符的 first 集
                            index = 0
                            for j in range(0, len(self.__non_terminal_signs)):
                                if self.__non_terminal_signs[j].type == production.get_right()[i].type:
                                    index = j
                                    break

                            # 判断其 first 集中是否有空字
                            empty_find = False
                            for j in range(0, len(self.__firsts[index])):
                                if self.__firsts[index][j].type == TerminalSignType.EMPTY:
                                    empty_find = True
                                    break

                            # 如果含有空字，则将 last 更新
                            if empty_find:
                                last = i
                            else:
                                break
                        # 如果不是直接跳出
                        else:
                            break

                    if last != -1:
                        # 如果 last 后面还有元素
                        if last < len(production.get_right()) - 1:
                            # 如果 last 后面是终结符
                            if type(production.get_right()[last + 1]) == TerminalSign:
                                self.__set_add(first, production.get_right()[last + 1])
                            # 如果是非终结符
                            else:
                                # 先找到后面那个非终结符的 first 集
                                index = 0
                                for i in range(0, len(self.__non_terminal_signs)):
                                    if self.__non_terminal_signs[i].type == production.get_right()[last + 1]:
                                        index = i

                                # 将其 first 集中的所有非空字元素添加到 first 集中去
                                for i in range(0, len(self.__firsts[index])):
                                    if self.__firsts[index][i].type != TerminalSignType.EMPTY:
                                        self.__set_add(first, self.__firsts[index][i])
                        # 如果 last 是最后一个元素了
                        else:
                            self.__set_add(first, TerminalSign(TerminalSignType.EMPTY))

            # 对于每一个终结符 in first(a)，将产生式添加到 M[A, a] 中去
            empty_find = False
            for terminal in first:
                if terminal.type != TerminalSignType.EMPTY:
                    if not self.__insert_to_table(production, terminal):
                        return False
                else:
                    empty_find = True

            # 若空字也在 first(a) 中，对于任何 b in follow(A)，将产生式添加到 M[A, b] 中去
            if empty_find:
                for terminal in self.__follows[a_index]:
                    if terminal.type != TerminalSignType.EMPTY:
                        if not self.__insert_to_table(production, terminal):
                            return False
        return True

    def get_production(self, non_terminal_sign, terminal_sign):
        """
        获取产生式
        :param non_terminal_sign: 非终结符
        :param terminal_sign: 终结符
        :return: 产生式
        """
        # 寻找非终结符的位置
        x = 0
        for i in range(0, len(self.__non_terminal_signs)):
            if self.__non_terminal_signs[i].type == non_terminal_sign.type:
                x = i
                break
        # 寻找终结符的位置
        y = 0
        for i in range(0, len(self.__terminal_signs)):
            if self.__terminal_signs[i].type == terminal_sign.type:
                y = i
                break
        return self.__table[x][y]


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
        self.__error = list()

    def put_source(self, source):
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
        # 新建一张预测分析表
        pa_table = PredictingAnalysisTable()
        # 编译预测分析表
        if not pa_table.compile():
            self.__error.append(Error("文法是非LL(1)的"))
            return False
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
            if type(top.data) == TerminalSign:
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
                production = pa_table.get_production(top.data, inputs[input_index])
                # 如果获取到了产生式
                if production:
                    # 将语法树按照产生式生长
                    for r in production.get_right():
                        top.children.append(TreeNode(r, list()))
                    # 将栈顶元素出栈
                    stack.pop()
                    # 把 top 的孩子节点按照反序入栈
                    for child in top.children[::-1]:
                        stack.push(child)
                # 如果没能获取到产生式，说明存放着的是错误标志，报错
                else:
                    # TODO 报错
                    return False
        # 分析成功，返回 True
        return True
