from syntax.syntax import Production

# 所有终结符的类型
terminal_sign_type = [
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

# 所有非终结符的类型
non_terminal_sign_type = [
    'pound'
]

# 工具类型
util_sign_type = [
    'empty'
]

# 文法产生式
productions = [
    Production('programs', 'declaration-list')
]

# 文法开始符号
grammar_start = 'programs'
