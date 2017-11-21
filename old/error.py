"""
错误相关
"""


class Error:
    """
    错误的基类
    """
    def __init__(self, error_str):
        """
        构造
        :param error_str: 错误信息
        """
        self.str = error_str


class LexicalError(Error):
    """
    词法错误
    """
    def __init__(self, error_str, error_line=-1):
        """
        构造
        :param error_str: 错误信息
        :param error_line: 错误行数
        """
        super().__init__(error_str)
        self.line = error_line


class GrammarError(Error):
    """
    文法错误
    """
    def __init__(self, error_str):
        super().__init__(error_str)
