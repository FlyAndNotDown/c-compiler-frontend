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
原文法
1. program -> declaration-list
2. declaration-list -> declaration-list declaration | declaration
3. declaration -> var-declaration | fun-declaration
4. var-declaration -> type-specifier ID ; | type-specifier ID [ NUM ] ;
5. type-specifier -> int | void
6. fun-declaration -> type-specifier ID ( params ) | compound-stmt
7. params -> params-list | void
8. param-list -> param-list , param | param
9. param -> type-specifier ID | type-specifier ID [ ]
10. compound-stmt -> { local-declaration statement-list }
11. local-declaration -> local-declaration var-declaration | empty
12. statement-list -> statement-list statement | empty
13. statement -> expression-stmt | compound-stmt | selection-stmt
    | iteration-stmt | return-stmt
14. expression-stmt -> expression ; | ;
15. selection-stmt -> if ( expression ) statement
                  | if ( expression ) statement else statement
16. iteration-stmt -> while ( expression ) statement
17. return-stmt -> return ; | return expression ;
18. expression -> var = expression | simple-expression
19. var -> ID | ID [ expression ]
20. simple-expression -> additive-expression relop additive-expression
                        | additive-expression
21. relop -> <= | < | > | >= | == | !=
22. additive-expression -> additive-expression addop term | term
23. addop -> + | -
24. term -> term mulop factor | factor
25. mulop -> * | /
26. factor -> ( expression ) | var | call | NUM
27. call -> ID ( args )
28. args -> arg-list | empty
29. arg-list -> arg-list , expression | expression
"""

"""
修改之后的文法
1. program -> declaration-list
# 2. declaration-list -> declaration-list declaration | declaration
2(1). declaration-list -> declaration declaration-list-follow
2(2). declaration-list-follow -> declaration declaration-list-follow | empty
3. declaration -> var-declaration | fun-declaration
# 4. var-declaration -> type-specifier ID ; | type-specifier ID [ NUM ] ;
4(1). var-declaration -> type-specifier ID var-declaration-follow
4(2). var-declaration-follow -> ; | [ NUM ] ;
5. type-specifier -> int | void
6. fun-declaration -> type-specifier ID ( params ) | compound-stmt
7. params -> params-list | void
# 8. param-list -> param-list , param | param
8(1). param-list -> param param-list-follow
8(2). param-list-follow -> , param param-list-follow | empty
# 9. param -> type-specifier ID | type-specifier ID [ ]
9(1). param -> type-specifier ID param-follow
9(2). param-follow -> [ ] | empty
10. compound-stmt -> { local-declaration statement-list }
# 11. local-declaration -> local-declaration var-declaration | empty
11(1). local-declaration -> var-declaration local-declaration | empty
# 12. statement-list -> statement-list statement | empty
12(1). statement-list -> statement statement-list | empty
13. statement -> expression-stmt | compound-stmt | selection-stmt
    | iteration-stmt | return-stmt
14. expression-stmt -> expression ; | ;
# 15. selection-stmt -> if ( expression ) statement
                  | if ( expression ) statement else statement
15(1). selection-stmt -> if ( expression ) statement
16. iteration-stmt -> while ( expression ) statement
# 17. return-stmt -> return ; | return expression ;
17(1). return-stmt -> return return-stmt-follow
17(2). return-stmt-follow -> expression ; | ;
18. expression -> var = expression | simple-expression
# 19. var -> ID | ID [ expression ]
19(1). var -> ID var-follow
19(2). var-follow -> [ expression ] | empty
# 20. simple-expression -> additive-expression relop additive-expression
                        | additive-expression
20(1). simple-expression -> additive-expression simple-expression-follow
20(2). simple-expression-follow -> relop additive-expression | empty
21. relop -> <= | < | > | >= | == | !=
# 22. additive-expression -> additive-expression addop term | term
22(1). additive-expression -> term additive-expression-follow
22(2). additive-expression-follow -> addop term additive-expression-follow | empty
23. addop -> + | -
# 24. term -> term mulop factor | factor
24(1) term -> factor term-follow
24(2) term-follow -> mulop factor term-follow | empty
25. mulop -> * | /
26. factor -> ( expression ) | var | call | NUM
27. call -> ID ( args )
28. args -> arg-list | empty
# 29. arg-list -> arg-list , expression | expression
29(1). arg-list -> expression arg-list-follow
29(2). arg-list-follow -> , expression arg-list-follow | empty
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
    'arg-list-follow'
]

# 文法产生式
productions = [
    Production('programs', 'declaration-list')
]

# 文法开始符号
grammar_start = Sign('programs')

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
