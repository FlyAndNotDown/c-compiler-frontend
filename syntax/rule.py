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

    def is_terminal_sign(self):
        """
        是不是终结符
        :return: True/False
        """
        if self.type == 'empty':
            return True
        else:
            for i in terminal_sign_type:
                if i == self.type:
                    return True
            return False

    def is_non_terminal_sign(self):
        """
        是不是非终结符
        :return: True/False
        """
        for i in non_terminal_sign_type:
            if i == self.type:
                return True
        return False

    def is_empty_sign(self):
        """
        是不是空字
        :return: True/False
        """
        return self.type == 'empty'


class Production:
    """
    产生式
    """
    def __init__(self, left_type, right_types):
        """
        产生式左边
        :param left_type: 产生式左边的符号类型
        :param right_types: 产生式右边的符号类型列表
        """
        self.left = Sign(left_type)
        self.right = list()
        for i in right_types:
            self.right.append(Sign(i))

        # 调试用的
        self.__str = self.left.type + ' ->'
        for i in self.right:
            self.__str += ' ' + i.type


# 所有终结符的类型
terminal_sign_type = [
    'else',
    'if',
    'int',
    'return',
    'void',
    'while',
    'addition',
    'subtraction',
    'multiplication',
    'division',
    'bigger',
    'bigger_equal',
    'smaller',
    'smaller_equal',
    'equal',
    'not_equal',
    'evaluate',
    'semicolon',
    'comma',
    'left_parentheses',
    'right_parentheses',
    'left_bracket',
    'right_bracket',
    'left_brace',
    'right_brace',
    'id',
    'num',
    # 在这之前添加非终结符类型，请务必不要动 'pound'
    'pound'
]

# 所有非终结符的类型
non_terminal_sign_type = [

]

# 文法产生式
productions = [
    Production('programs', 'declaration-list')
]

# 文法开始符号
grammar_start = Sign('programs')

##############################################################

# 所有终结符的类型
terminal_sign_type1 = [
    'addition',
    'multiplication',
    'left_p',
    'right_p',
    'i',
    # 在这之前添加非终结符类型，请务必不要动 'pound'
    'pound'
]

# 所有非终结符的类型
non_terminal_sign_type1 = [
    'E',
    'E1',
    'T',
    'T1',
    'F',
]

# 文法产生式
productions1 = [
    Production('E', ['T', 'E1']),
    Production('E1', ['addition', 'T', 'E1']),
    Production('E1', []),
    Production('T', ['F', 'T1']),
    Production('T1', ['multiplication', 'F', 'T1']),
    Production('T1', []),
    Production('F', ['left_p', 'E', 'right_p']),
    Production('F', ['i'])
]

# 文法开始符号
grammar_start1 = Sign('E')
