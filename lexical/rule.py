# 所有的 token 的类型
token_type = [
    'else',
    'if',
    'int',
    'return',
    'void',
    'while',
    'addition',
    'subtraction',
    'multiplication',
    'division',
    'bigger',
    'bigger_equal',
    'smaller',
    'smaller_equal',
    'equal',
    'not_equal',
    'evaluate',
    'semicolon',
    'comma',
    'left_parentheses',
    'right_parentheses',
    'left_bracket',
    'right_bracket',
    'left_brace',
    'right_brace',
    'id',
    'num'
]

# 分隔符号
split_char_type = [
    'space'
]

# 注释
note_char_type = (
    'note_start',
    'note_end'
)

# 正则表达式字典
regex_dict = {
    'space': r' +',
    'note_start': r'/\*',
    'note_end': r'\*/',
    'else': r'else',
    'if': r'if',
    'int': r'int',
    'return': r'return',
    'void': r'void',
    'while': r'while',
    'addition': r'\+',
    'subtraction': r'-',
    'multiplication': r'\*',
    'division': r'/',
    'bigger': r'>',
    'bigger_equal': r'>=',
    'smaller': r'<',
    'smaller_equal': r'<=',
    'equal': r'==',
    'not_equal': r'!=',
    'evaluate': r'=',
    'semicolon': r';',
    'comma': r',',
    'left_parentheses': r'\(',
    'right_parentheses': r'\)',
    'left_bracket': r'\[',
    'right_bracket': r'\]',
    'left_brace': r'\{',
    'right_brace': r'\}',
    'id': r'[a-zA-Z][a-zA-Z]*',
    'num': r'[1-9][0-9]*|0'
}
