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
    'bigger-equal',
    'smaller',
    'smaller-equal',
    'equal',
    'not-equal',
    'evaluate',
    'semicolon',
    'comma',
    'left-parentheses',
    'right-parentheses',
    'left-bracket',
    'right-bracket',
    'left-brace',
    'right-brace',
    'id',
    'num'
]

# 分隔符号
split_char_type = [
    'space'
]

# 注释
note_char_type = (
    'note-start',
    'note-end'
)

# 正则表达式字典
regex_dict = {
    'space': r' +',
    'note-start': r'/\*',
    'note-end': r'\*/',
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
    'bigger-equal': r'>=',
    'smaller': r'<',
    'smaller-equal': r'<=',
    'equal': r'==',
    'not-equal': r'!=',
    'evaluate': r'=',
    'semicolon': r';',
    'comma': r',',
    'left-parentheses': r'\(',
    'right-parentheses': r'\)',
    'left-bracket': r'\[',
    'right-bracket': r'\]',
    'left-brace': r'\{',
    'right-brace': r'\}',
    'id': r'[a-zA-Z][a-zA-Z]*',
    'num': r'[1-9][0-9]*|0'
}
