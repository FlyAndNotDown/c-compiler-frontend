class Symbol:
    """
    符号单项
    """
    TYPE_NORMAL_VAR = 0
    TYPE_ARRAY = 1

    def __init__(self, symbol_name, s_type, width):
        """
        构造
        :param symbol_name: 符号名
        """
        self.name = symbol_name
        self.type = s_type
        self.offset = 0
        self.width = width


class SymbolTable:
    """
    符号表
    """
    TYPE_GLOBAL_VAR = 0
    TYPE_LOCAL_VAR = 1

    def __init__(self, st_type, st_name):
        """
        构造
        """
        self.__table = list()
        self.type = st_type
        self.name = st_name
        self.offset = 0
        self.width = 0

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
            self.__table[-1].offset = self.width
            self.width += self.__table[-1].width
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

            width_t = self.__table[index].width
            for i in range(index, len(self.__table)):
                self.__table[i].offset -= width_t
            self.width -= width_t
            del self.__table[index]
            return True
        else:
            return False


class SymbolTablePool:
    """
    符号表池
    """
    def __init__(self):
        """
        构造
        """
        self.__pool = list()

    def exist(self, name):
        """
        查找某一个符号表是否存在
        :param name: 符号表名
        :return: 对应的符号表
        """
        for symbol_table in self.__pool:
            if symbol_table.name == name:
                return True
        return False

    def query(self, name):
        """
        查询一个符号表
        :param name: 符号表名
        :return 对应的符号表
        """
        for symbol_table in self.__pool:
            if symbol_table.name == name:
                return symbol_table
        return None

    def append(self, symbol_table):
        """
        添加一张新表
        :param symbol_table: 符号表
        """
        self.__pool.append(symbol_table)
