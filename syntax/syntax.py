"""
语法分析
"""
from syntax.rule import terminal_sign_type, non_terminal_sign_type
from error import SyntaxRuleError

class Sign:
    """
    终结符和非终结符的基类
    """
    def __init__(self, sign_type, sign_str='', sign_line=-1):
        """
        构造
        :param sign_type: 符号的类型
        :param sign_str: 符号的内容(可以为空)
        :param sign_line: 符号所在行数(可以为空)
        """
        self.type = sign_type

    def is_terminal(self):
        """
        是不是终结符
        :return: True/False
        """
        for i in terminal_sign_type:
            if i.type == self.type:
                return True
        return False

    def is_non_terminal(self):
        """
        是不是非终结符
        :return: True/False
        """
        for i in non_terminal_sign_type:
            if i.type == self.type:
                return True
        return False


class Production:
    """
    产生式
    """
    def __init__(self, left_type, right_types):
        """
        产生式左边
        :param left: 产生式左边的符号类型
        :param right: 产生式右边的符号类型列表
        """
        self.left = Sign(left_type)
        self.right = list()
        for i in right_types:
            self.right.append(Sign(i))


class PredictingAnalysisTable:
    """
    预测分析表
    """
    def __init__(self):
        """
        构造
        """
        # 错误
        self.__error = None

        # 预测分析表
        self.__table = list()

        # 所有的非终结符
        self.__non_terminal_signs = list()
        # 所有的终结符
        self.__terminal_signs = list()

        # 载入所有的符号
        for i in non_terminal_sign_type:
            self.__non_terminal_signs.append(Sign(i))
        for i in terminal_sign_type:
            self.__terminal_signs.append(Sign(i))

        # 根据非终结符和终结符的数量为预测分析表分配空间，并且为每一个格子预先填上 None
        for i in non_terminal_sign_type:
            self.__table.append(list())
        for i in non_terminal_sign_type:
            for j in terminal_sign_type:
                self.__table[i].append(None)

        # 为每一个非终结符建立 first 集和 follow 集
        self.__firsts = list()
        self.__follows = list()

        # 为每一个非终结符的 first 集和 follow 集分配空间
        for i in non_terminal_sign_type:
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

    def __get_terminal_index(self, terminal_sign):
        """
        获取终结符的索引
        :param terminal_sign: 终结符
        :return: 索引(寻找失败返回 -1)
        """
        for i in range(0, len(self.__terminal_signs)):
            if terminal_sign.type == self.__terminal_signs[i].type:
                return i
        return -1

    def __get_non_terminal_index(self, non_terminal_sign):
        """
        获取非终结符的索引
        :param non_terminal_sign: 非终结符
        :return: 索引(寻找失败返回 -1)
        """
        for i in range(0, len(self.__non_terminal_signs)):
            if non_terminal_sign.type == self.__non_terminal_signs[i].type:
                return i
        return -1

    def __get_first_elem_no_empty(self, index):
        """
        按照索引获取对应的非终结符的 first 集的所有非空元素
        :param index: 非终结符索引
        :return: 索引对应的非终结符的 first 集的所有非空元素
        """

    def __get_first_elem(self, index):
        """
        按照索引获取对应的非终结符的 first 集的所有元素
        :param index: 非终结符索引
        :return: 索引对应的非终结符的 first 集的所有元素
        """

    def __first_have_empty(self, index):
        """
        判断索引对应的非终结符的 first 集中是否包含空字
        :param index: 索引
        :return: 索引对应的非终结符的 first 集中是否包含空字
        """

    def __get_follow_elem(self, index):
        """
        获取索引对应的非终结符的 follow 集中的元素
        :param index: 索引
        :return: 索引对应的非终结符的 follow 集中的元素
        """

    def __get_follow_elem_no_empty(self, index):
        """
        获取索引对应的非终结符的 follow 集中的非空元素
        :param index: 索引
        :return: 索引对应的非终结符的 follow 集中的非空元素
        """

    def __get_firsts(self):
        """
        求所有的 first 集
        """

    def __get_follows(self):
        """
        求所有的 follow 集
        """

    def __insert_to_table(self, production, terminal):
        """
        将产生式插入预测分析表对应位置
        :param production: 产生式
        :param terminal: 终结符
        :return: 是否插入成功
        """
        # 先判断应该插入到的位置
        x = self.__get_non_terminal_index(production.left)
        y = self.__get_terminal_index(terminal)

        # 如果那个位置已经有产生式了
        if self.__table[x][y]:
            # 判断两个产生式是否一样
            left_same = production.left.type == self.__table[x][y].left.type
            right_same = True
            if len(production.right) != len(self.__table[x][y].right):
                right_same = False
            if right_same:
                for i in range(production.right):
                    if production.right[i].type != self.__table[x][y].right[i].type:
                        right_same = False
            # 如果一样
            if left_same and right_same:
                return True
            # 如果不一样，报错
            else:
                self.__error = SyntaxRuleError("文法不是LL(1)的")
        # 如果那个位置为空，说明可以填入
        else:
            # 执行插入
            del self.__table[x][y]
            self.__table[x].insert(y, production)
            return True

    def __generate_table(self):
        """
        根据 first 集和 follow 集生成预测分析表
        :return: 是否生成成功
        """
        return False

    def get_production(self, non_terminal_sign, terminal_sign):
        """
        从预测分析表中获取产生式
        :param non_terminal_sign: 非终结符
        :param terminal_sign: 终结符
        :return: 产生式
        """