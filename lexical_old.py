import re
from symbol_table import *


class TokenType:
    """Token 的类型"""
    SPACE = 0                   # 空格
    NEWLINE = 1                 # 换行
    ELSE = 2                    # else
    IF = 3                      # if
    INT = 4                     # int
    RETURN = 5                  # return
    VOID = 6                    # void
    WHILE = 7                   # while
    ADDITION = 8                # +
    SUBTRACTION = 9             # -
    MULTIPLICATION = 10          # *
    DIVISION = 11               # /
    BIGGER = 12                 # >
    BIGGER_EQUAL = 13           # >=
    SMALLER = 14                # <
    SMALLER_EQUAL = 15          # <=
    EQUAL = 16                  # ==
    NOT_EQUAL = 17              # !=
    EVALUATE = 18               # =
    SEMICOLON = 19              # ;
    COMMA = 20                  # ,
    LEFT_PARENTHESES = 21       # (
    RIGHT_PARENTHESES = 22      # )
    LEFT_BRACKET = 23           # [
    RIGHT_BRACKET = 24          # ]
    LEFT_BRACE = 25             # {
    RIGHT_BRACE = 26            # }
    LEFT_NOTE = 27              # /*
    RIGHT_NOTE = 28             # */
    ID = 29                     # 标识符
    NUM = 30                    # 数字


class Token:
    """Token"""
    def __init__(self, kind=TokenType.SPACE, string=''):
        self.type = kind
        self.str = string


class RegexTable:
    """Token 正则表达式表"""
    __token_regex = [
        r' +',                      # 0 空格
        r'\\n',                     # 1 换行
        r'else',                    # 2 else
        r'if',                      # 3 if
        r'int',                     # 4 int
        r'return',                  # 5 return
        r'void',                    # 6 void
        r'while',                   # 7 while
        r'\+',                      # 8 +
        r'-',                       # 9 -
        r'\*',                      # 10 *
        r'/',                       # 11 /
        r'>',                       # 12 >
        r'>=',                      # 13 >=
        r'<',                       # 14 <
        r'<=',                      # 15 <=
        r'==',                      # 16 ==
        r'!=',                      # 17 !=
        r'=',                       # 18 =
        r';',                       # 19 ;
        r',',                       # 20 ,
        r'\(',                      # 21 (
        r'\)',                      # 22 )
        r'\[',                      # 23 [
        r'\]',                      # 24 ]
        r'\{',                      # 25 {
        r'\}',                      # 26 }
        r'/\*',                     # 27 /*
        r'\*/',                     # 28 */
        r'[a-zA-Z][a-zA-Z]*',       # 29 标识符
        r'[1-9][0-9]*|0'            # 30 数字
    ]

    @classmethod
    def get_regex(cls, kind):
        return cls.__token_regex[kind]

    @classmethod
    def get_regex_instance(cls, kind):
        return re.compile(cls.__token_regex[kind])

    @classmethod
    def get_num(cls):
        return len(cls.__token_regex)


class Lexical:
    """词法分析器"""
    def __init__(self):
        self.__error = ''
        self.__source = ''
        self.__tokens = list()
        self.__symbol_table = None

    def put_source(self, source):
        self.__source = source

    def put_symbol_table(self, symbol_table):
        self.__symbol_table = symbol_table

    def __del_useless_char(self):
        self.__source = self.__source.replace('\\', ' ')
        self.__source = self.__source.replace('\r', ' ')
        self.__source = self.__source.replace('\n', ' ')
        self.__source = self.__source.replace('\t', ' ')
        return True

    def __del_notes(self):
        # 计数器，用来确认注释开始符和注释结束符号的数量是否匹配
        note_symbol_count = 0
        # 缓冲区
        buffer = self.__source
        # 结果
        result = self.__source
        # 当前缓冲区的开头字符在 source 中的位置
        buffer_start = 0

        # 开始匹配
        while True:
            # 判断是否已经到了末尾，如果到了末尾直接跳出
            if buffer_start >= len(self.__source):
                break

            # 先匹配 /*
            match = RegexTable.get_regex_instance(TokenType.LEFT_NOTE).search(buffer)
            # 如果匹配到了
            if match:
                left_note_start = buffer_start + match.start()
                # 开始匹配 */
                match2 = RegexTable.get_regex_instance(TokenType.RIGHT_NOTE).search(buffer)
                # 如果匹配到了
                if match2:
                    right_note_end = buffer_start + match2.end()
                    # 执行删除
                    result = result.replace(self.__source[left_note_start:right_note_end], '')
                    # 删除完了之后进入下次循环
                    buffer_start_old = buffer_start
                    buffer_start = right_note_end
                    buffer = buffer[buffer_start - buffer_start_old:len(buffer) - 1]
                    continue
                # 如果没有匹配到，说明两者数量不匹配，报错
                else:
                    self.__error = '多余的注释符'
                    return False
            # 如果没匹配到就寻找有没有多余的 */
            else:
                match2 = RegexTable.get_regex_instance(TokenType.RIGHT_NOTE).search(buffer)
                if match2:
                    self.__error = '多余的注释结束符'
                    return False
                else:
                    break
        self.__source = result
        return True

    def __split_token(self):
        # 建立缓冲区
        buffer = self.__source
        # 是否成功
        success = False

        # 当缓冲区还存在数据的时候，不断进行循环匹配
        while len(buffer) > 0:
            # 当前循环是否成功匹配到 Token
            token_match = False
            # 在正则表达式表中尝试所有的正则表达式进行匹配
            for i in range(0, RegexTable.get_num()):
                match = RegexTable.get_regex_instance(i).match(buffer)
                # 如果匹配到了
                if match:
                    # 如果匹配到的是 id，则将其添加到符号表
                    if i == TokenType.ID:
                        # 如果添加失败，说明肯定是重复了
                        if not self.__symbol_table.add(match.group(0)):
                            self.__error = '重复的标识符' + match.group(0)
                            return False

                    self.__tokens.append(Token(i, match.group(0)))
                    # 更新缓冲区剩余字符
                    buffer = buffer[match.end():len(buffer) - 1]
                    # 更新 token_match
                    token_match = True
                    break
                # 如果没有匹配到
                else:
                    continue

            # 如果没有匹配到，则说明失败了
            if not token_match:
                if len(buffer) < 5:
                    self.__error = '词法错误,在程序末尾'
                else:
                    self.__error = '词法错误' + '\'' + buffer[0:5] + '\''
                return False
        return True

    def __del_spaces(self):
        new_tokens = list()
        for token in self.__tokens:
            # 如果不是空格就添加到新的 token 列表中
            if token.type != TokenType.SPACE:
                new_tokens.append(token)

        # 最后把老的 token 列表替换成新的 token 列表
        self.__tokens.clear()
        for token in new_tokens:
            self.__tokens.append(token)

    def __pre_deal(self):
        if self.__del_useless_char():
            return self.__del_notes()
        else:
            return False

    def __deal(self):
        if self.__split_token():
            return self.__del_spaces()
        else:
            return False

    def execute(self):
        if self.__pre_deal():
            if self.__deal():
                return True
            else:
                return False
        else:
            return False

    def get_error(self):
        return self.__error

    def get_result(self):
        return self.__tokens
