class Symbol:
    """
    符号单项
    """
    def __init__(self, symbol_name):
        """
        构造
        :param symbol_name: 符号名
        """
        self.name = symbol_name


class SymbolTable:
    """
    符号表
    """
    def __init__(self):
        """
        构造
        """
        self.__table = list()

    def exist(self, symbol_name):
        """
        给定名字，查询此名字是否已经在表中
        :param symbol_name: 符号名
        :return: True/False
        """
        for symbol in self.__table:
            if symbol.name == symbol_name:
                return True
        return False

    def append(self, symbol):
        """
        填入一个新符号
        :param symbol: 符号
        :return: 如果已经有这个符号了，返回 False，否则返回 True
        """
        if self.exist(symbol.name):
            return False
        else:
            self.__table.append(symbol)
            return True

    def query(self, symbol_name):
        """
        根据符号名访问内容
        :param symbol_name: 符号名
        :return: 符号
        """
        for symbol in self.__table:
            if symbol.name == symbol_name:
                return symbol
        return None

    def update(self, symbol):
        """
        根据给出的新内容更新原有的符号
        :param symbol: 新符号
        :return: 如果符号不存在，返回 False，如果存在，更新之后返回 True
        """
        if self.exist(symbol.name):
            index = 0
            for i in range(0, len(self.__table)):
                if self.__table[i].name == symbol.name:
                    index = i

            # 执行更新
            del self.__table[index]
            self.__table.insert(index, symbol)
            return True
        else:
            return False

    def delete(self, symbol_name):
        """
        根据名字删除符号
        :param symbol_name: 符号名
        :return: 如果符号不存在，返回 False，存在则删除之后返回 True
        """
        if self.exist(symbol_name):
            index = 0
            for i in range(0, len(self.__table)):
                if self.__table[i].name == symbol_name:
                    index = i

            del self.__table[index]
            return True
        else:
            return False