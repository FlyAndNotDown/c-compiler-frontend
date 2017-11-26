"""
语法分析
"""
from syntax.rule import Sign, Production, terminal_sign_type, non_terminal_sign_type, productions, grammar_start
from error import SyntaxRuleError


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
        for i in range(0, len(non_terminal_sign_type)):
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
        self.__calculate_firsts()
        # 对每一个文法元素求其 follow 集
        self.__calculate_follows()
        # 根据 first 集和 follow 集生成预测分析表
        success = self.__generate_table()
        return success

    def get_production(self, non_terminal_sign, terminal_sign):
        """
        从预测分析表中获取产生式
        :param non_terminal_sign: 非终结符
        :param terminal_sign: 终结符
        :return: 产生式
        """
        x = self.__get_non_terminal_sign_index(non_terminal_sign)
        y = self.__get_terminal_sign_index(terminal_sign)
        return self.__table[x][y]

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

    def __get_terminal_sign_index(self, terminal_sign):
        """
        获取终结符的索引
        :param terminal_sign: 终结符
        :return: 索引(寻找失败返回 -1)
        """
        for i in range(0, len(self.__terminal_signs)):
            if terminal_sign.type == self.__terminal_signs[i].type:
                return i
        return -1

    def __get_non_terminal_sign_index(self, non_terminal_sign):
        """
        获取非终结符的索引
        :param non_terminal_sign: 非终结符
        :return: 索引(寻找失败返回 -1)
        """
        for i in range(0, len(self.__non_terminal_signs)):
            if non_terminal_sign.type == self.__non_terminal_signs[i].type:
                return i
        return -1

    def __get_non_terminal_sign_first(self, non_terminal_sign):
        """
        获取目标非终结符的 first 集的引用
        :param non_terminal_sign: 目标非终结符
        :return: 其 first 集的引用
        """
        return self.__firsts[self.__get_non_terminal_sign_index(non_terminal_sign)]

    def __get_non_terminal_sign_first_no_empty(self, non_terminal_sign):
        """
        获取目标非终结符的 first 集的非空拷贝
        :param non_terminal_sign: 目标非终结符
        :return: 其 first 集的非空拷贝
        """
        result = list()
        for i in self.__get_non_terminal_sign_first(non_terminal_sign):
            if not i.is_empty_sign():
                result.append(i)
        return result

    def __is_empty_in_non_terminal_sign_first(self, non_terminal_sign):
        """
        目标非终结符的 first 集中是否有空字
        :param non_terminal_sign: 目标非终结符
        :return: True/False
        """
        for i in self.__get_non_terminal_sign_first(non_terminal_sign):
            if i.is_empty_sign():
                return True
        return False

    def __get_non_terminal_sign_follow(self, non_terminal_sign):
        """
        获取非终结符的 follow 集
        :param non_terminal_sign: 非终结符
        :return: 其 follow 集
        """
        return self.__follows[self.__get_non_terminal_sign_index(non_terminal_sign)]

    def __calculate_firsts(self):
        """
        求所有的 first 集
        """
        # 立一个 flag，用来标志 firsts 集是否增大
        flag = True
        # 开始循环
        while flag:
            flag = False
            # 在每一次循环之中遍历所有产生式
            for production in productions:
                # 如果产生式右边为空
                if len(production.right) == 0:
                    # 将空字加入其 first 集
                    if self.__set_add(self.__get_non_terminal_sign_first(production.left), Sign('empty')):
                        flag = True
                # 如果产生式右边不为空
                else:
                    # 如果是以终结符开头，将终结符添加到其 first 集
                    if production.right[0].is_terminal_sign():
                        if self.__set_add(self.__get_non_terminal_sign_first(production.left), production.right[0]):
                            flag = True
                    # 如果是以非终结符开头
                    elif production.right[0].is_non_terminal_sign():
                        # (1) 将开头非终结符的 first 集中的所有非空元素添加到产生式左边非终结符的 first 集中
                        bigger = False
                        for i in self.__get_non_terminal_sign_first_no_empty(production.right[0]):
                            if self.__set_add(self.__get_non_terminal_sign_first(production.left), i):
                                bigger = True
                        if bigger:
                            flag = True

                        # (2) 从第一个非终结符开始循环，如果其 first 集中包含空字，那么将它下一个符号的 first
                        # 集添加到产生式左边非终结符的 first 集中去
                        for i in range(0, len(production.right)):
                            if production.right[i].is_non_terminal_sign():
                                # 如果包含空字
                                if self.__is_empty_in_non_terminal_sign_first(production.right[i]):
                                    # 如果它是最后一个，将空字填入
                                    if i == len(production.right) - 1:
                                        if self.__set_add(self.__get_non_terminal_sign_first(production.left),
                                                          Sign('empty')):
                                            flag = True
                                    # 如果不是最后一个
                                    else:
                                        # 如果它之后是终结符
                                        if production.right[i + 1].is_terminal_sign():
                                            if self.__set_add(self.__get_non_terminal_sign_first(production.left),
                                                              production[i + 1]):
                                                flag = True
                                        # 如果它之后是非终结符
                                        elif production.right[i + 1].is_non_terminal_sign():
                                            bigger = False
                                            for j in self.__get_non_terminal_sign_first_no_empty(
                                                    production.right[i + 1]):
                                                if self.__set_add(
                                                        self.__get_non_terminal_sign_first(production.left), j):
                                                    bigger = True
                                            if bigger:
                                                flag = True
                                        else:
                                            self.__error = SyntaxRuleError('终结符或非终结符类型错误')
                                            return False
                                # 如果不包含空字
                                else:
                                    break
                            else:
                                break
                    # 否则报错
                    else:
                        self.__error = SyntaxRuleError('终结符或非终结符类型错误')
                        return False

    def __calculate_follows(self):
        """
        求所有的 follow 集
        """
        first = list()
        flag = True
        while flag:
            flag = False
            # 遍历所有产生式
            for production in productions:
                # 如果产生式左边是开始符号
                if production.left.type == grammar_start.type:
                    if self.__set_add(self.__get_non_terminal_sign_follow(production.left), Sign('pound')):
                        flag = True

                # 遍历产生式右边
                for i in range(0, len(production.right)):
                    # 如果是非终结符
                    if production.right[i].is_non_terminal_sign():
                        # 如果它是产生式最后一个符号
                        if i == len(production.right) - 1:
                            # 将产生式左边非终结符的 follow 集添加到这个符号的 follow 集中
                            bigger = False
                            for j in self.__get_non_terminal_sign_follow(production.left):
                                if self.__set_add(self.__get_non_terminal_sign_follow(production.right[i]), j):
                                    bigger = True
                            if bigger:
                                flag = True
                        # 否则观察其之后的元素
                        else:
                            # 求他之后所有符号集合的 first 集
                            first.clear()
                            first += self.__calculate_set_first(production.right[i + 1:])
                            # (1) 将 first 中所有非空元素填入 follow
                            empty_find = False
                            for f in first:
                                if not f.is_empty_sign():
                                    self.__set_add(self.__get_non_terminal_sign_follow(production.right[i]), f)
                                else:
                                    empty_find = True

                            # (2) 如果 first 中含有空
                            if empty_find:
                                # 将产生式左边非终结符的 follow 集添加到这个符号的 follow 集中
                                bigger = False
                                for j in self.__get_non_terminal_sign_follow(production.left):
                                    if self.__set_add(self.__get_non_terminal_sign_follow(production.right[i]), j):
                                        bigger = True
                                if bigger:
                                    flag = True

                            # # 如果他后面是一个终结符
                            # if production.right[i + 1].is_terminal_sign():
                            #     if self.__set_add(self.__get_non_terminal_sign_follow(production.right[i]),
                            #                       production.right[i + 1]):
                            #         flag = True
                            # # 如果他后面是一个非终结符
                            # elif production.right[i + 1].is_non_terminal_sign():
                            #     # (1) 将后面非终结符的 first 集中的所有非空元素填入
                            #     bigger = False
                            #     for j in self.__get_non_terminal_sign_first_no_empty(production.right[i + 1]):
                            #         if self.__set_add(self.__get_non_terminal_sign_follow(production.right[i]), j):
                            #             bigger = True
                            #     if bigger:
                            #         flag = True
                            #
                            #     # (2) 如果后面所有的非终结符 first 集都包含空
                            #     # 那么，则将产生式左边的 follow 集添加到该非终结符的 follow 集中去
                            #     all_empty_in_first = True
                            #     for j in range(i + 1, len(production.right)):
                            #         if not self.__is_empty_in_non_terminal_sign_first(production.right[j]):
                            #             all_empty_in_first = False
                            #             break
                            #     if all_empty_in_first:
                            #         bigger = False
                            #         for j in self.__get_non_terminal_sign_follow(production.left):
                            #             if self.__set_add(self.__get_non_terminal_sign_follow(production.right[i]), j):
                            #                 bigger = True
                            #         if bigger:
                            #             flag = True
                            # # 否则报错
                            # else:
                            #     self.__error = SyntaxRuleError('终结符或非终结符类型错误')
                            #     return False
                    # 如果是终结符
                    elif production.right[i].is_terminal_sign():
                        continue
                    # 否则报错
                    else:
                        self.__error = SyntaxRuleError('终结符或非终结符类型错误')
                        return False

    def __calculate_set_first(self, container):
        """
        计算一系列符号的 first 集
        :param container: 符号集合
        :return: first 集
        """
        first = list()

        # 开始求 first 集
        # 如果集合为空
        first = list()

        # 开始求 first 集
        # 如果产生式右边为空
        if len(container) == 0:
            # 将空字加入其 first 集
            self.__set_add(first, Sign('empty'))
        # 如果产生式右边补位空
        else:
            # 如果是以终结符开头，将终结符添加到 first 集
            if container[0].is_terminal_sign():
                self.__set_add(first, container[0])
            # 如果是以非终结符开头
            elif container[0].is_non_terminal_sign():
                # (1) 将开头非终结符的 first 集中的所有非空元素添加到 first 中
                for i in self.__get_non_terminal_sign_first_no_empty(container[0]):
                    self.__set_add(first, i)

                # (2) 从第一个非终结符开始循环，如果其 first 集中包含空字，那么将它的下一个符号的 first
                # 集添加到 first 中
                for i in range(0, len(container)):
                    if container[i].is_non_terminal_sign():
                        # 如果包含空字
                        if self.__is_empty_in_non_terminal_sign_first(container[i]):
                            # 如果它是最后一个，将空字填入
                            if i == len(container) - 1:
                                self.__set_add(first, Sign('empty'))
                            # 如果不是最后一个
                            else:
                                # 如果它之后是终结符
                                if container[i + 1].is_terminal_sign():
                                    self.__set_add(first, container[i + 1])
                                # 如果它之后是非终结符
                                elif container[i + 1].is_non_terminal_sign():
                                    for j in self.__get_non_terminal_sign_first_no_empty(container[i + 1]):
                                        self.__set_add(first, j)
                                # 否则报错
                                else:
                                    self.__error = SyntaxRuleError('终结符或非终结符类型错误')
                                    return False
                        # 如果不含空字
                        else:
                            break
                    else:
                        break
            # 否则报错
            else:
                self.__error = SyntaxRuleError('终结符或非终结符类型错误')
                return False

        return first

    def __insert_to_table(self, production, terminal):
        """
        将产生式插入预测分析表对应位置
        :param production: 产生式
        :param terminal: 终结符
        :return: 是否插入成功
        """
        # 先判断应该插入到的位置
        x = self.__get_non_terminal_sign_index(production.left)
        y = self.__get_terminal_sign_index(terminal)

        # 如果那个位置已经有产生式了
        if self.__table[x][y]:
            # 判断这个产生式是不是与要插入的产生式一样
            same_left = production.left.type == self.__table[x][y].left.type
            if same_left:
                same_right = True
                if len(production.right) != len(self.__table[x][y].right):
                    self.__error = SyntaxRuleError("文法非LL(1)" + production.str)
                    return False
                else:
                    for i in range(0, len(production.right)):
                        if production.right[i].type != self.__table[x][y].right[i].type:
                            same_right = False
                    if same_right:
                        # 执行插入
                        del self.__table[x][y]
                        self.__table[x].insert(y, production)
                        return True
                    else:
                        self.__error = SyntaxRuleError("文法非LL(1)" + production.str)
                        return False
            else:
                self.__error = SyntaxRuleError("文法非LL(1)" + production.str)
                return False
        # 如果那个位置为空，说明可以填入
        else:
            # 执行插入
            del self.__table[x][y]
            self.__table[x].insert(y, production)
            return True

    @classmethod
    def __set_have_repeat(cls, set1, set2):
        """
        判断两个集合是否有交集
        :param set1: 集合1
        :param set2: 集合2
        :return: 是否有交集
        """
        for i in set1:
            for j in set2:
                if i.type == j.type:
                    return True
        return False

    def __grammar_rule_debug(self):
        """
        调试使用，求一个非终结符对应的所有产生式右边的 first 集中是否有相交元素
        """
        # 一个非终结符对应的所有产生式
        his_productions = list()
        # 那些产生式对应的 first 集
        firsts = list()
        # 错误
        errors = list()

        # 对于所有的非终结符
        for non_terminal_sign in self.__non_terminal_signs:
            # 寻找他对应的所有产生式
            his_productions.clear()
            firsts.clear()
            for production in productions:
                if non_terminal_sign.type == production.left.type:
                    his_productions.append(production)

            # 对于那些产生式，分别求 first 集
            for production in his_productions:
                firsts.append(self.__calculate_set_first(production.right))

            # 是否有交集
            have_repeat = False
            # 查看这些产生式的 first 集两两之间是否有交集
            for i in range(0, len(his_productions) - 1):
                for j in range(i + 1, len(his_productions)):
                    if self.__set_have_repeat(firsts[i], firsts[j]):
                        have_repeat = True
                        break

            # 如果有交集
            if have_repeat:
                errors.append('产生式 First 集重叠 ' + '非终结符: ' + non_terminal_sign.type)

            # 如果非终结符的 First 集中包含空字
            if self.__is_empty_in_non_terminal_sign_first(non_terminal_sign):
                # 如果他的 First 集和 Follow 集有交集
                if self.__set_have_repeat(self.__get_non_terminal_sign_first(non_terminal_sign),
                                          self.__get_non_terminal_sign_follow(non_terminal_sign)):
                    errors.append('产生式 First 集和 Follow 集重叠 ' + '非终结符: ' + non_terminal_sign.type)
        return

    def __generate_table(self):
        """
        根据 first 集和 follow 集生成预测分析表
        :return: 是否生成成功
        """
        # 调试
        self.__grammar_rule_debug()

        # 对每一条产生式应用规则
        for production in productions:
            # 先求出该产生式右边部分的 first 集
            first = self.__calculate_set_first(production.right)

            # 对每一个 first 集中的每一个终结符执行操作
            empty_find = False
            for i in list(first):
                if i.type == 'empty':
                    empty_find = True
                else:
                    if not self.__insert_to_table(production, i):
                        return False

            # 如果其 first 集中有空字，则对 follow 集中的每一个终结符执行操作
            if empty_find:
                for i in self.__get_non_terminal_sign_follow(production.left):
                    if not self.__insert_to_table(production, i):
                        return False

        return True
