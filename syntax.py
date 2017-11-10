from lexical import *
from symbol_table import *


class Element:
    """语法元素"""
    def __init__(self, kind):
        self.type = kind


class TerminalElement(Element):
    """终结符"""


class NonTerminalElement(Element):
    """非终结符"""


class TerminalElementType(TokenType):
    """终结符种类"""


class NonTerminalElementType:
    """非终结符种类"""
    PROGRAMS = 0
    DECLARATION_LIST = 1
    DECLARATION = 2
    VAR_DECLARATION = 3
    FUN_DECLARATION = 4

    @classmethod
    def get_start(cls):
        return cls.PROGRAMS


class Derivation:
    """推导"""
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst


class DerivationTable:
    """所有推导的表"""
    def __init__(self):
        self.__derivations = [

        ]

    def length(self):
        return len(self.__derivations)

    def get(self, index):
        if index >= self.length():
            return None
        else:
            return self.__derivations[index]


class SyntaxTreeNode:
    """语法树节点"""
    def __init__(self, is_terminal, kind, children=list()):
        self.is_terminal = is_terminal
        self.type = kind
        self.children = children


class SyntaxTree:
    """语法树"""
    def __init__(self):
        self.root = SyntaxTreeNode(True, NonTerminalElementType.get_start())


class Syntax:
    """语法分析器"""
    def __init__(self):
        self.__source = list()
        self.__error = ''
        self.__symbol_table = None
        self.__syntax_tree = SyntaxTree()

    def put_source(self, tokens):
        self.__source = tokens

    def put_symbol_table(self, symbol_table):
        self.__symbol_table = symbol_table

    def execute(self):
        # TODO
        return
