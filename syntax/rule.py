class Sign:
    """
    终结符和非终结符的基类
    """
    def __init__(self, sign_type, sign_str='', sign_line=-1):
        """
        构造
        :param sign_type: 符号的类型
        :param sign_str: 符号的内容(可以为空)
        :param sign_line: 符号所在行数(可以为空)
        """
        self.type = sign_type

    def is_terminal_sign(self):
        """
        是不是终结符
        :return: True/False
        """
        if self.type == 'empty':
            return True
        else:
            for i in terminal_sign_type:
                if i == self.type:
                    return True
            return False

    def is_non_terminal_sign(self):
        """
        是不是非终结符
        :return: True/False
        """
        for i in non_terminal_sign_type:
            if i == self.type:
                return True
        return False

    def is_empty_sign(self):
        """
        是不是空字
        :return: True/False
        """
        return self.type == 'empty'


class Production:
    """
    产生式
    """
    def __init__(self, left_type, right_types):
        """
        产生式左边
        :param left_type: 产生式左边的符号类型
        :param right_types: 产生式右边的符号类型列表
        """
        self.left = Sign(left_type)
        self.right = list()
        for i in right_types:
            self.right.append(Sign(i))

        # 调试用的
        self.str = self.left.type + ' ->'
        for i in self.right:
            self.str += ' ' + i.type


"""
修改之后的文法
1.      program -> declaration-list
2(1).   declaration-list -> declaration declaration-list-follow
2(2).   declaration-list-follow -> declaration declaration-list-follow | empty
3.      declaration -> var-declaration | fun-declaration
4(1).   var-declaration -> type-specifier ID var-declaration-follow
4(2).   var-declaration-follow -> ; | [ NUM ] ;
5.      type-specifier -> int | void
6.      fun-declaration -> type-specifier ID ( params ) | compound-stmt
7.      params -> param-list | void
8(1).   param-list -> param param-list-follow
8(2).   param-list-follow -> , param param-list-follow | empty
9(1).   param -> type-specifier ID param-follow
9(2).   param-follow -> [ ] | empty
10.     compound-stmt -> { local-declaration statement-list }
11(1).  local-declaration -> var-declaration local-declaration | empty
12(1).  statement-list -> statement statement-list | empty
13.     statement -> expression-stmt | compound-stmt | selection-stmt
                    | iteration-stmt | return-stmt
14.     expression-stmt -> expression ; | ;
15(1).  selection-stmt -> if ( expression ) statement
16.     iteration-stmt -> while ( expression ) statement
17(1).  return-stmt -> return return-stmt-follow
17(2).  return-stmt-follow -> expression ; | ;
18.     expression -> var = expression | simple-expression
19(1).  var -> ID var-follow
19(2).  var-follow -> [ expression ] | empty
20(1).  simple-expression -> additive-expression simple-expression-follow
20(2).  simple-expression-follow -> relop additive-expression | empty
21.     relop -> <= | < | > | >= | == | !=
22(1).  additive-expression -> term additive-expression-follow
22(2).  additive-expression-follow -> addop term additive-expression-follow | empty
23.     addop -> + | -
24(1)   term -> factor term-follow
24(2)   term-follow -> mulop factor term-follow | empty
25.     mulop -> * | /
26.     factor -> ( expression ) | var-or-call | NUM
27.     call -> ID ( args )
28.     args -> arg-list | empty
29(1).  arg-list -> expression arg-list-follow
29(2).  arg-list-follow -> , expression arg-list-follow | empty
30(1).  var-or-call -> ID var-or-call-follow
30(2).  var-or-call-follow -> var-follow | ( args )
"""

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
    'num',
    # 在这之前添加非终结符类型，请务必不要动 'pound'
    'pound'
]

# 所有非终结符的类型
non_terminal_sign_type = [
    'program',
    'declaration-list',
    'declaration-list-follow',
    'declaration',
    'var-declaration',
    'var-declaration-follow',
    'type-specifier',
    'fun-declaration',
    'params',
    'param-list',
    'param-list-follow',
    'param',
    'param-follow',
    'compound-stmt',
    'local-declaration',
    'statement-list',
    'statement',
    'expression-stmt',
    'selection-stmt',
    'iteration-stmt',
    'return-stmt',
    'return-stmt-follow',
    'expression',
    'var',
    'var-follow',
    'simple-expression',
    'simple-expression-follow',
    'relop',
    'additive-expression',
    'additive-expression-follow',
    'addop',
    'term',
    'term-follow',
    'mulop',
    'factor',
    'call',
    'args',
    'arg-list',
    'arg-list-follow',
    'var-or-call',
    'var-or-call-follow'
]

# 文法产生式
productions = [
    # 1. program -> declaration-list
    Production('program', ['declaration-list']),
    # 2(1). declaration-list -> declaration declaration-list-follow
    Production('declaration-list', ['declaration', 'declaration-list-follow']),
    # 2(2). declaration-list-follow -> declaration declaration-list-follow | empty
    Production('declaration-list-follow', ['declaration', 'declaration-list-follow']),
    Production('declaration-list-follow', []),
    # 3. declaration -> var-declaration | fun-declaration
    Production('declaration', ['var-declaration']),
    Production('declaration', ['fun-declaration']),
    # 4(1). var-declaration -> type-specifier ID var-declaration-follow
    Production('var-declaration', ['type-specifier', 'id', 'var-declaration-follow']),
    # 4(2). var-declaration-follow -> ; | [ NUM ] ;
    Production('var-declaration-follow', ['semicolon']),
    Production('var-declaration-follow', ['left_bracket', 'num', 'right_bracket', 'semicolon']),
    # 5. type-specifier -> int | void
    Production('type-specifier', ['int']),
    Production('type-specifier', ['void']),
    # 6. fun-declaration -> type-specifier ID ( params ) | compound-stmt
    Production('fun-declaration', ['type-specifier', 'id', 'left_parentheses', 'params', 'right_parentheses']),
    Production('fun-declaration', ['compound-stmt']),
    # 7. params -> param-list | void
    Production('params', ['param-list']),
    Production('params', ['void']),
    # 8(1). param-list -> param param-list-follow
    Production('param-list', ['param', 'param-list-follow']),
    # 8(2). param-list-follow -> , param param-list-follow | empty
    Production('param-list-follow', ['comma', 'param', 'param-list-follow']),
    Production('param-list-follow', []),
    # 9(1). param -> type-specifier ID param-follow
    Production('param', ['type-specifier', 'id', 'param-follow']),
    # 9(2). param-follow -> [ ] | empty
    Production('param-follow', ['left_bracket', 'right_bracket']),
    Production('param-follow', []),
    # 10. compound-stmt -> { local-declaration statement-list }
    Production('compound-stmt', ['left_brace', 'local-declaration', 'statement-list', 'right_brace']),
    # 11(1). local-declaration -> var-declaration local-declaration | empty
    Production('local-declaration', ['var-declaration', 'local-declaration']),
    Production('local-declaration', []),
    # 12(1). statement-list -> statement statement-list | empty
    Production('statement-list', ['statement', 'statement-list']),
    Production('statement-list', []),
    # 13. statement -> expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt
    Production('statement', ['expression-stmt']),
    Production('statement', ['compound-stmt']),
    Production('statement', ['selection-stmt']),
    Production('statement', ['iteration-stmt']),
    Production('statement', ['return-stmt']),
    # 14. expression-stmt -> expression ; | ;
    Production('expression-stmt', ['expression', 'semicolon']),
    Production('expression-stmt', ['semicolon']),
    # 15(1). selection-stmt -> if ( expression ) statement
    Production('selection-stmt', ['if', 'left_parentheses', 'expression', 'right_parentheses', 'statement']),
    # 16. iteration-stmt -> while ( expression ) statement
    Production('iteration-stmt', ['while', 'left_parentheses', 'expression', 'right_parentheses', 'statement']),
    # 17(1). return-stmt -> return return-stmt-follow
    Production('return-stmt', ['return', 'return-stmt-follow']),
    # 17(2). return-stmt-follow -> expression ; | ;
    Production('return-stmt-follow', ['expression', 'semicolon']),
    Production('return-stmt-follow', ['semicolon']),
    # 18. expression -> var = expression | simple-expression
    Production('expression', ['var', 'evaluate', 'expression']),
    Production('expression', ['simple-expression']),
    # 19(1). var -> ID var-follow
    Production('var', ['id', 'var-follow']),
    # 19(2). var-follow -> [ expression ] | empty
    Production('var-follow', ['left_bracket', 'expression', 'right_bracket']),
    Production('var-follow', []),
    # 20(1). simple-expression -> additive-expression simple-expression-follow
    Production('simple-expression', ['additive-expression', 'simple-expression-follow']),
    # 20(2). simple-expression-follow -> relop additive-expression | empty
    Production('simple-expression-follow', ['relop', 'additive-expression']),
    Production('simple-expression-follow', []),
    # 21. relop -> <= | < | > | >= | == | !=
    Production('relop', ['smaller_equal']),
    Production('relop', ['smaller']),
    Production('relop', ['bigger']),
    Production('relop', ['bigger_equal']),
    Production('relop', ['equal']),
    Production('relop', ['not_equal']),
    # 22(1). additive-expression -> term additive-expression-follow
    Production('additive-expression', ['term', 'additive-expression-follow']),
    # 22(2). additive-expression-follow -> addop term additive-expression-follow | empty
    Production('additive-expression-follow', ['addop', 'term', 'additive-expression-follow']),
    Production('additive-expression-follow', []),
    # 23. addop -> + | -
    Production('addop', ['addition']),
    Production('addop', ['subtraction']),
    # 24(1). term -> factor term-follow
    Production('term', ['factor', 'term-follow']),
    # 24(2). term-follow -> mulop factor term-follow | empty
    Production('term-follow', ['mulop', 'factor', 'term-follow']),
    Production('term-follow', []),
    # 25. mulop -> * | /
    Production('mulop', ['multiplication']),
    Production('mulop', ['division']),
    # 26. factor -> ( expression ) | var-or-call | num
    Production('factor', ['left_parentheses', 'expression', 'right_parentheses']),
    Production('factor', ['var-or-call']),
    Production('factor', ['num']),
    # 27. call -> ID ( args )
    Production('call', ['id', 'left_parentheses', 'args', 'right_parentheses']),
    # 28. args -> arg-list | empty
    Production('args', ['arg-list']),
    Production('args', []),
    # 29(1). arg-list -> expression arg-list-follow
    Production('arg-list', ['expression', 'arg-list-follow']),
    # 29(2). arg-list-follow -> , expression arg-list-follow | empty
    Production('arg-list-follow', ['comma', 'expression', 'arg-list-follow']),
    Production('arg-list-follow', []),
    # 30(1). var-or-call -> ID var-or-call-follow
    Production('var-or-call', ['id', 'var-or-call-follow']),
    # 30(2). var-or-call-follow -> var-follow | ( args )
    Production('var-or-call-follow', ['var-follow']),
    Production('var-or-call-follow', ['left_parentheses', 'args', 'right_parentheses'])
]

# 文法开始符号
grammar_start = Sign('program')

##############################################################

# 所有终结符的类型
terminal_sign_type1 = [
    'addition',
    'multiplication',
    'left_p',
    'right_p',
    'i',
    # 在这之前添加非终结符类型，请务必不要动 'pound'
    'pound'
]

# 所有非终结符的类型
non_terminal_sign_type1 = [
    'E',
    'E1',
    'T',
    'T1',
    'F',
]

# 文法产生式
productions1 = [
    Production('E', ['T', 'E1']),
    Production('E1', ['addition', 'T', 'E1']),
    Production('E1', []),
    Production('T', ['F', 'T1']),
    Production('T1', ['multiplication', 'F', 'T1']),
    Production('T1', []),
    Production('F', ['left_p', 'E', 'right_p']),
    Production('F', ['i'])
]

# 文法开始符号
grammar_start1 = Sign('E')
