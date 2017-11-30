class Symbol:
    """
    符号基类
    """
    def __init__(self, name):
        self.name = name


class SymbolTable:
    """
    符号表
    """
    def __init__(self):
        self.__table = list()

    def exist(self, name):
        """
        给定名字的符号是否存在
        :param name:
        :return: True/False
        """
        for s in self.__table:
            if s.name == name:
                return True
        return False

    def query(self, name):
        """
        查询特定名字的符号
        :param name: 名字
        :return: 符号
        """
        for symbol in self.__table:
            if symbol.name == name:
                return symbol
        return None

    def append(self, symbol):
        """
        填入符号
        :param symbol: 符号
        """
        pass

    def num(self):
        """
        获取符号总数
        :return: 符号总数
        """
        return len(self.__table)

    def get(self, index):
        """
        根据索引来获取符号
        :param index: 索引
        :return: 符号
        """
        return self.__table[index]


class SymbolTablePool:
    """
    符号表池
    """
    def __init__(self):
        self.__global_var_table = GlobalVarTable()
        self.__fun_table = FunTable()
        self.__local_var_tables = list()

    def query_local_var_table(self, table_name):
        """
        给定名字查找局部变量表
        :param table_name: 表名
        :return: 局部变量表
        """
        for table in self.__local_var_tables:
            if table.name == table_name:
                return table
        return None

    def new_local_var_table(self, name):
        """
        新建一张局部变量表
        :param name: 表名
        """
        self.__local_var_tables.append(LocalVarTable(name))
        # 将所有的全局变量添加到表中
        for i in range(0, self.get_global_var_table().num()):
            self.query_local_var_table(name).append(
                LocalVarRecord(
                    self.get_global_var_table().get(i).name,
                    self.get_global_var_table().get(i),
                    self.get_global_var_table()
                )
            )

    def get_global_var_table(self):
        """
        获取全局变量表
        :return: 全局变量表
        """
        return self.__global_var_table

    def get_fun_table(self):
        """
        获取函数表
        :return: 函数表
        """
        return self.__fun_table


class GlobalVarTable(SymbolTable):
    """
    全局变量表
    """
    def __init__(self):
        super().__init__()
        # 等实际装填了再更改地址
        self.__address = 0
        self.__width = 0

    def append(self, symbol):
        """
        添加一个全局变量
        :param symbol: 符号
        """
        self.__table.append(symbol)
        self.__table[-1].offset = self.__width
        self.__width += self.__table[-1].width

    def get_var_address(self, name):
        """
        获取变量的实际地址
        :param name: 变量名
        :return: 变量的实际地址
        """
        return self.__address + self.query(name).offset


class GlobalVarItem(Symbol):
    """
    全局变量表项
    """
    def __init__(self, g_name, g_type, g_width):
        super().__init__(g_name)
        self.type = g_type
        self.width = g_width
        self.offset = None


class LocalVarTable(SymbolTable):
    """
    局部变量表
    """
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.__address = 0
        self.__width = 0

    def append(self, symbol_record, is_record=False):
        """
        添加一个符号或记录到符号表
        :param symbol_record: 符号或记录
        :param is_record: 是否为记录
        """
        if is_record:
            self.__table.append(symbol_record)
        else:
            self.__table.append(symbol_record)
            self.__table[-1].offset = self.__width
            self.__width += self.__table[-1].width

    def get_var_address(self, name):
        """
        获取变量的实际地址
        :param name: 变量名
        :return: 变量的实际地址
        """
        return self.__address + self.query(name).offset


class LocalVarItem(Symbol):
    """
    局部变量表项
    """
    def __init__(self, l_name, l_type, l_width, l_is_param):
        super().__init__(l_name)
        self.type = l_type
        self.width = l_width
        self.offset = None
        # 是否为形参
        self.is_param = l_is_param


class LocalVarRecord(Symbol):
    """
    局部变量表引用
    """
    def __init__(self, l_name, l_symbol, l_table):
        super().__init__(l_name)
        self.symbol = l_symbol
        self.table = l_table


class FunTable(SymbolTable):
    """
    函数表
    """
    def __init__(self):
        super().__init__()

    def append(self, symbol):
        """
        填入一个新的函数
        :param symbol: 函数
        """
        self.__table.append(symbol)


class FunItem(Symbol):
    """
    函数表项
    """
    def __init__(self, f_name, f_type):
        super().__init__(f_name)
        self.type = f_type
