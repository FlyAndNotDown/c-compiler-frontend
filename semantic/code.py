current_var_num = 0


def gen_temp_var_name():
    """
    获取一个新的临时变量名
    :return: 临时变量名
    """
    global current_var_num
    name = '_t' + str(current_var_num)
    current_var_num += 1
    return name
