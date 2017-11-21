"""
词法分析相关
"""


import re

from old.error import LexicalError

from old.symbol_table import *


class TokenType:
    """
    Token 的类型
    """
    SPACE = 0                   # 空格
    ELSE = 1                    # else
    IF = 2                      # if
    INT = 3                     # int
    RETURN = 4                  # return
    VOID = 5                    # void
    WHILE = 6                   # while
    ADDITION = 7                # +
    SUBTRACTION = 8             # -
    MULTIPLICATION = 9          # *
    DIVISION = 10               # /
    BIGGER = 11                 # >
    BIGGER_EQUAL = 12           # >=
    SMALLER = 13                # <
    SMALLER_EQUAL = 14          # <=
    EQUAL = 15                  # ==
    NOT_EQUAL = 16              # !=
    EVALUATE = 17               # =
    SEMICOLON = 18              # ;
    COMMA = 19                  # ,
    LEFT_PARENTHESES = 20       # (
    RIGHT_PARENTHESES = 21      # )
    LEFT_BRACKET = 22           # [
    RIGHT_BRACKET = 23          # ]
    LEFT_BRACE = 24             # {
    RIGHT_BRACE = 25            # }
    ID = 26                     # 标识符
    NUM = 27                    # 数字
    LEFT_NOTE = 28              # /*
    RIGHT_NOTE = 29             # */
    NONE = -1                   # 空


class Token:
    """
    Token
    """
    def __init__(self, token_type=TokenType.NONE, token_str='', token_line=-1):
        """
        构造
        :param token_type: Token 的类型
        :param token_str: Token 的内容
        :param token_line: Token 所在的行数
        """
        self.type = token_type
        self.str = token_str
        self.line = token_line


class RegexTable:
    """
    正则表达式表
    """
    __token_regex = [
        r' +',                      # 0 空格
        r'else',                    # 1 else
        r'if',                      # 2 if
        r'int',                     # 3 int
        r'return',                  # 4 return
        r'void',                    # 5 void
        r'while',                   # 6 while
        r'\+',                      # 7 +
        r'-',                       # 8 -
        r'\*',                      # 9 *
        r'/',                       # 10 /
        r'>',                       # 11 >
        r'>=',                      # 12 >=
        r'<',                       # 13 <
        r'<=',                      # 14 <=
        r'==',                      # 15 ==
        r'!=',                      # 16 !=
        r'=',                       # 17 =
        r';',                       # 18 ;
        r',',                       # 19 ,
        r'\(',                      # 20 (
        r'\)',                      # 21 )
        r'\[',                      # 22 [
        r'\]',                      # 23 ]
        r'\{',                      # 24 {
        r'\}',                      # 25 }
        r'[a-zA-Z][a-zA-Z]*',       # 26 标识符
        r'[1-9][0-9]*|0',           # 27 数字
        r'/\*',                     # 28 /*
        r'\*/',                     # 29 */
    ]

    @classmethod
    def get_len(cls):
        """
        获取正则表达式表中正常正则表达式的数量
        :return: 正则表达式表中正常正则表达式的数量
        """
        return len(cls.__token_regex) - 2

    @classmethod
    def get_regex(cls, token_type):
        """
        获取编译好的正常正则表达式
        :param token_type: token 的类型
        :return: 编译好的正则表达式
        """
        if 0 <= token_type < cls.get_len():
            return re.compile(cls.__token_regex[token_type])
        else:
            return None

    @classmethod
    def get_special_regex(cls, token_type):
        """
        获取正则表达式表中的特殊正则表达式 (尤指注释符号)
        :param token_type: token 的类型
        :return: 编译好的正则表达式
        """
        if cls.get_len() <= token_type < cls.get_len() + 2:
            return re.compile(cls.__token_regex[token_type])
        else:
            return None


class Lexical:
    """
    词法分析器
    """
    def __init__(self):
        """
        构造
        """
        self.__error = None
        self.__source = ''
        self.__lines = list()
        self.__tokens = list()
        self.__symbol_table = SymbolTable()

    def put_source(self, source):
        """
        装载源代码
        :param source: 源代码
        """
        self.__source = source

    def execute(self):
        """
        执行词法分析
        :return: 词法分析是否成功
        """
        self.__replace_useless_chars()
        if self.__del_notes():
            self.__split_lines()
            if self.__split_tokens():
                self.__del_spaces()
                return True
            else:
                return False
        else:
            return False

    def get_result(self):
        """
        获取结果
        :return: token 列表
        """
        return self.__tokens

    def __replace_useless_chars(self):
        """
        替换无用的字符
        """
        # 将 \r 替换成 \n
        self.__source = self.__source.replace('\r', '\n')
        # 将 \t 替换成四个空格
        self.__source = self.__source.replace('\t', '    ')

    def __del_notes(self):
        """
        删除注释
        :return: 是否删除成功
        """
        # 计数器，用来确认注释开始符和注释结束符的数量是否相等
        note_count = 0
        # 缓冲区
        buffer = self.__source
        # 结果
        result = self.__source

        # 判断是否匹配到了末尾
        while True:
            # 尝试匹配 */
            match = RegexTable.get_special_regex(TokenType.LEFT_NOTE).search(buffer)
            # 如果匹配到了
            if match:
                left_note_start = match.start()
                # 开始匹配 */
                match2 = RegexTable.get_special_regex(TokenType.RIGHT_NOTE).search(buffer)
                # 如果匹配到了
                if match2:
                    right_note_end = match2.end()
                    # 判断匹配到的区间中有几行
                    line_count = result[left_note_start:right_note_end].count('\n')
                    # 执行删除
                    result = result.replace(result[left_note_start:right_note_end], '\n' * line_count)
                    # 删除完毕之后进入下一次循环
                    buffer = result
                    continue
                # 如果没有匹配到，说明两者数量不匹配，报错
                else:
                    # 判断错误所在的行数
                    enter_location = list()
                    enter_location.append(0)
                    for i in range(0, len(result)):
                        if result[i] == '\n':
                            enter_location.append(i)
                    find = False

                    error_line = 0
                    for i in range(0, len(enter_location) - 1):
                        if enter_location[i] < left_note_start < enter_location[i + 1]:
                            error_line = i + 1
                            find = True
                            break
                    if not find:
                        error_line = len(enter_location)

                    # 报错
                    self.__error = LexicalError('/* 没有相匹配的 */', error_line)
                    return False
            # 如果没有匹配到
            else:
                # 尝试寻找有没有落单的 */
                match2 = RegexTable.get_special_regex(TokenType.RIGHT_NOTE).search(buffer)
                # 如果找到了说明错误了
                if match2:
                    right_note_start = match2.start()
                    # 判断错误所在的行数
                    enter_location = list()
                    enter_location.append(0)
                    for i in range(0, len(result)):
                        if result[i] == '\n':
                            enter_location.append(i)
                    find = False

                    error_line = 0
                    for i in range(0, len(enter_location) - 1):
                        if enter_location[i] < right_note_start < enter_location[i + 1]:
                            error_line = i + 1
                            find = True
                            break
                    if not find:
                        error_line = len(enter_location)

                    # 报错
                    self.__error = LexicalError('多余的 */', error_line)
                    return False
                # 如果没有找到那就说明已经找完了，跳出
                else:
                    break

        # 将 result 保存到 __source 中
        self.__source = result
        return True

    def __split_lines(self):
        """
        将完成源代码分割成行序列
        """
        # 清空 __tokens
        self.__tokens.clear()
        # 按行分割
        temp = self.__source.split('\n')
        # 将分割出来的行序列添加到 __tokens 中
        for t in temp:
            self.__lines.append(' ' + t)

    def __split_tokens(self):
        """
        从行序列中分割出 token
        :return: 是否分割成功
        """
        # 先将 __lines 拷贝一份到临时变量中
        lines = list()
        for line in self.__lines:
            lines.append(line)
        # 缓冲区
        buffer = ''
        # 当前所在行数
        current_line_num = 0
        # 结果
        tokens = list()

        while len(lines) > 0:
            # 当前循环中是否匹配成功
            match_this_time = False

            # 如果缓冲区中没有数据了，就填充一行到缓冲区
            if buffer == '':
                buffer = lines[0]
                lines = lines[1:]
                # 行号自增
                current_line_num += 1

            # 开始匹配
            # 尝试用所有的正则表达式来匹配
            for i in range(0, RegexTable.get_len()):
                match = RegexTable.get_regex(i).match(buffer)
                # 如果匹配到了
                if match:
                    # 将其添加到 tokens 中
                    tokens.append(Token(i, buffer[match.start():match.end()], current_line_num))
                    # buffer 去除已经匹配的部分
                    buffer = buffer[match.end():]
                    match_this_time = True
                    break
            # 如果匹配完所有的正则表达式都不成功
            if not match_this_time:
                # 报错
                self.__error = LexicalError('词法错误', current_line_num)
                # 返回失败
                return False
        # 循环正常结束则说明完全匹配成功，将结果保存到 __tokens 中，返回成功
        for token in tokens:
            self.__tokens.append(token)
        return True

    def __del_spaces(self):
        """
        删除 __tokens 中的空格
        """
        # 新建临时变量
        tokens = list()
        # 将 __tokens 中的内容拷贝到 tokens 中
        for token in self.__tokens:
            tokens.append(token)
        # 清空 __tokens
        self.__tokens.clear()
        # 如果不是空格就添加进原来的 __tokens，相当于从原来的列表中去除了空格
        for token in tokens:
            if token.type != TokenType.SPACE:
                self.__tokens.append(token)
