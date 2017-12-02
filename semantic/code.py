current_var_num = 0
current_block_num = 0


def get_temp_var_name():
    """
    获取一个新的临时变量名
    :return: 临时变量名
    """
    global current_var_num
    name = '_v' + str(current_var_num)
    current_var_num += 1
    return name


def get_temp_block_name():
    """
    获取一个新的代码块名
    :return: 代码块名
    """
    global current_block_num
    name = '__b' + str(current_block_num)
    current_block_num += 1
    return name
