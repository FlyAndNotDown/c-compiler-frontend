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
        给定名字的表是否存在
        :param name:
        :return:
        """