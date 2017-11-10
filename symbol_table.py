class SymbolAttr:
    VARIABLE = 0
    FUNCTION = 1


class Symbol:
    def __init__(self, name='', attr=''):
        self.__name = name
        self.__attr = attr


class SymbolTable:
    def __init__(self):
        self.__table = list()

    def __exist(self, name):
        for symbol in self.__table:
            if symbol.name == name:
                return True
        return False

    def add(self, symbol):
        # 如果已经存在了，就直接返回失败
        if self.__exist(symbol.name):
            return False
        # 如果不存在，那么则将其添加到符号表中
        else:
            self.__table.append(symbol)

    def find(self, name):
        for symbol in self.__table:
            if symbol.name == name:
                return symbol
        return None

    def remove(self, name):
        for symbol in self.__table:
            if symbol.name == name:
                self.__table.remove(symbol)
                return True
        return False
