import re


class TokenType:
    """Token 的类型"""
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
    LEFT_NOTE = 26              # /*
    RIGHT_NOTE = 27             # */
    ID = 28                     # 标识符
    NUM = 29                    # 数字


class Token:
    """Token"""
    def __init__(self, kind=TokenType.SPACE, string=''):
        self.type = kind
        self.str = string


class RegexTable:
    """Token 正则表达式表"""
    __token_regex = [
        r'',                        # 0 空格
        r'',                        # 1 else
        r'',                        # 2 if
        r'',                        # 3 int
        r'',                        # 4 return
        r'',                        # 5 void
        r'',                        # 6 while
        r'',                        # 7 +
        r'',                        # 8 -
        r'',                        # 9 *
        r'',                        # 10 /
        r'',                        # 11 >
        r'',                        # 12 >=
        r'',                        # 13 <
        r'',                        # 14 <=
        r'',                        # 15 ==
        r'',                        # 16 !=
        r'',                        # 17 =
        r'',                        # 18 ;
        r'',                        # 19 ,
        r'',                        # 20 (
        r'',                        # 21 )
        r'',                        # 22 [
        r'',                        # 23 ]
        r'',                        # 24 {
        r'',                        # 25 }
        r'/\*',                     # 26 /*
        r'\*/',                     # 27 */
        r'',                        # 28 标识符
        r''                         # 29 数字
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
    def __init__(self, source=''):
        self.__error = ''
        self.__source = source
        self.__tokens = list()

    def put_source(self, source):
        self.__source = source

    def __del_useless_char(self):
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
            left_note_start = buffer_start + match.start()
            if match:
                # 开始匹配 */
                match2 = RegexTable.get_regex_instance(TokenType.RIGHT_NOTE).search(buffer)
                # 如果匹配到了
                if match2:
                    right_note_end = buffer_start + match.end()
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
                    self.__tokens.append(Token(i, match.group(0)))
                    # 更新缓冲区剩余字符
                    buffer = buffer[match.end():len(buffer) - 1]
                    # 更新 token_match
                    token_match = True
                    break
                # 如果没有匹配到
                else:
                    continue

            # 如果匹配到了 Token，则继续匹配，如果没有匹配到，则说明失败了
            if not token_match:
                if len(buffer) < 5:
                    self.__error = '词法错误,在程序末尾'
                else:
                    self.__error = '词法错误' + '\''+ buffer[0:5] + '\''
                return False

    def __pre_deal(self):
        if self.__del_useless_char():
            if self.__del_notes():
                return True
            else:
                return False
        else:
            return False

    def __deal(self):
        return self.__split_token()

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


lexical = Lexical(open('test.c').read())
lexical.execute()
