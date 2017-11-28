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
        self.str = sign_str
        self.line = sign_line

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
# 26.     factor -> ( expression ) | var-or-call | NUM
26(1).  factor -> 
27.     call -> ID ( args )
28.     args -> arg-list | empty
29(1).  arg-list -> expression arg-list-follow
29(2).  arg-list-follow -> , expression arg-list-follow | empty
30(1).  var-or-call -> ID var-or-call-follow
30(2).  var-or-call-follow -> var-follow | fun-follow
30(3).  fun-follow -> ( args )
"""

"""
重新写的文法
1.  program -> define-list
2.  define-list -> define define-list | empty
3.  define -> type ID define-type
4.  define-type -> var-define-follow | fun-define-follow
5.  var-define-follow -> ; | [ NUM ] ;
6.  type -> int | void
7.  fun-define-follow -> ( params ) code-block
8.  params -> param-list | empty
9.  param-list -> param param-follow
10. param-follow -> , param param-follow | empty
11. param -> type ID array-subscript
12. array-subscript -> [ ] | empty
13. code-block -> { local-define-list code-list }
14. local-define-list -> local-var-define local-define-list | empty
15. local-var-define -> type ID var-define-follow
16. code-list -> code code-list | empty
17. code -> normal-statement | selection-statement | iteration-statement | return-statement
#   normal-statement -> ; | ID var-follow = expression ; | ID call-follow ;
    normal-statement -> ; | ID normal-statement-follow
    normal-statement-follow -> var-follow = expression ; | call-follow ;
    call-follow -> ( call-params )
    call-params -> call-param-list | empty
    call-param-list -> expression call-param-follow
    call-param-follow -> , expression call-param-follow | empty
19. selection-statement -> if ( expression ) { code-list } selection-follow
20. selection-follow -> else { code-list } | empty
21. iteration-statement -> while ( expression ) iteration-follow
22. iteration-follow -> { code-list } | code
23. return-statement -> return return-follow
24. return-follow -> ; | expression ;
#   eval-statement -> var = expression
#   var -> ID var-follow
27. var-follow -> [ expression ] | empty
28. expression -> additive-expr expression-follow
29. expression-follow -> rel-op additive-expr | empty
30. rel-op -> <= | < | > | >= | == | !=
31. additive-expr -> term additive-expr-follow
32. additive-expr-follow -> add-op term additive-expr-follow | empty
33. add-op -> + | -
34. term -> factor term-follow
35. term-follow -> mul-op factor term-follow | empty
36. mul-op -> * | /
37. factor -> ( expression ) | ID id-factor-follow | NUM
38. id-factor-follow -> var-follow | ( args )
39. args -> arg-list | empty
40. arg-list -> expression arg-list-follow
41. arg-list-follow -> , expression arg-list-follow | empty
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
    'num',
    # 在这之前添加非终结符类型，请务必不要动 'pound'
    'pound'
]

# 所有非终结符的类型
non_terminal_sign_type = [
    'program',
    'define-list',
    'define',
    'define-type',
    'var-define-follow',
    'type',
    'fun-define-follow',
    'params',
    'param-list',
    'param-follow',
    'param',
    'array-subscript',
    'code-block',
    'local-define-list',
    'local-var-define',
    'code-list',
    'code',
    'normal-statement',
    'normal-statement-follow',
    'call-follow',
    'call-params',
    'call-param-list',
    'call-param-follow',
    'selection-statement',
    'selection-follow',
    'iteration-statement',
    'iteration-follow',
    'return-statement',
    'return-follow',
    # 'eval-statement',
    # 'var',
    'var-follow',
    'expression',
    'expression-follow',
    'rel-op',
    'additive-expr',
    'additive-expr-follow',
    'add-op',
    'term',
    'term-follow',
    'mul-op',
    'factor',
    'id-factor-follow',
    'args',
    'arg-list',
    'arg-list-follow'
]

# 文法产生式
productions = [
    Production('program', ['define-list']),
    Production('define-list', ['define', 'define-list']),
    Production('define-list', []),
    Production('define', ['type', 'id', 'define-type']),
    Production('define-type', ['var-define-follow']),
    Production('define-type', ['fun-define-follow']),
    Production('var-define-follow', ['semicolon']),
    Production('var-define-follow', ['left-bracket', 'num', 'right-bracket', 'semicolon']),
    Production('type', ['int']),
    Production('type', ['void']),
    Production('fun-define-follow', ['left-parentheses', 'params', 'right-parentheses', 'code-block']),
    Production('params', ['param-list']),
    Production('params', []),
    Production('param-list', ['param', 'param-follow']),
    Production('param-follow', ['comma', 'param', 'param-follow']),
    Production('param-follow', []),
    Production('param', ['type', 'id', 'array-subscript']),
    Production('array-subscript', ['left-bracket', 'right-bracket']),
    Production('array-subscript', []),
    Production('code-block', ['left-brace', 'local-define-list', 'code-list', 'right-brace']),
    Production('local-define-list', ['local-var-define', 'local-define-list']),
    Production('local-define-list', []),
    Production('local-var-define', ['type', 'id', 'var-define-follow']),
    Production('code-list', ['code', 'code-list']),
    Production('code-list', []),
    Production('code', ['normal-statement']),
    Production('code', ['selection-statement']),
    Production('code', ['iteration-statement']),
    Production('code', ['return-statement']),
    # Production('normal-statement', ['eval-statement', 'semicolon']),
    # Production('normal-statement', ['semicolon']),
    Production('normal-statement', ['semicolon']),
    Production('normal-statement', ['id', 'normal-statement-follow']),
    Production('normal-statement-follow', ['var-follow', 'evaluate', 'expression', 'semicolon']),
    Production('normal-statement-follow', ['call-follow', 'semicolon']),
    Production('call-follow', ['left-parentheses', 'call-params', 'right-parentheses']),
    Production('call-params', ['call-param-list']),
    Production('call-params', []),
    Production('call-param-list', ['expression', 'call-param-follow']),
    Production('call-param-follow', ['comma', 'expression', 'call-param-follow']),
    Production('call-param-follow', []),
    Production('selection-statement',
               ['if', 'left-parentheses', 'expression', 'right-parentheses','left-brace',
                'code-list', 'right-brace', 'selection-follow']),
    Production('selection-follow', ['else', 'left-brace', 'code-list', 'right-brace']),
    Production('selection-follow', []),
    Production('iteration-statement', ['while', 'left-parentheses', 'expression',
                                       'right-parentheses', 'iteration-follow']),
    Production('iteration-follow', ['left-brace', 'code-list', 'right-brace']),
    Production('iteration-follow', ['code']),
    Production('return-statement', ['return', 'return-follow']),
    Production('return-follow', ['semicolon']),
    Production('return-follow', ['expression', 'semicolon']),
    # Production('eval-statement', ['var', 'evaluate', 'expression']),
    # Production('var', ['id', 'var-follow']),
    Production('var-follow', ['left-bracket', 'expression', 'right-bracket']),
    Production('var-follow', []),
    Production('expression', ['additive-expr', 'expression-follow']),
    Production('expression-follow', ['rel-op', 'additive-expr']),
    Production('expression-follow', []),
    Production('rel-op', ['smaller-equal']),
    Production('rel-op', ['smaller']),
    Production('rel-op', ['bigger']),
    Production('rel-op', ['bigger-equal']),
    Production('rel-op', ['equal']),
    Production('rel-op', ['not-equal']),
    Production('additive-expr', ['term', 'additive-expr-follow']),
    Production('additive-expr-follow', ['add-op', 'term', 'additive-expr-follow']),
    Production('additive-expr-follow', []),
    Production('add-op', ['addition']),
    Production('add-op', ['subtraction']),
    Production('term', ['factor', 'term-follow']),
    Production('term-follow', ['mul-op', 'factor', 'term-follow']),
    Production('term-follow', []),
    Production('mul-op', ['multiplication']),
    Production('mul-op', ['division']),
    Production('factor', ['left-parentheses', 'expression', 'right-parentheses']),
    Production('factor', ['id', 'id-factor-follow']),
    Production('factor', ['num']),
    Production('id-factor-follow', ['var-follow']),
    Production('id-factor-follow', ['left-parentheses', 'args', 'right-parentheses']),
    Production('args', ['arg-list']),
    Production('args', []),
    Production('arg-list', ['expression', 'arg-list-follow']),
    Production('arg-list-follow', ['comma', 'expression', 'arg-list-follow']),
    Production('arg-list-follow', [])
]

# 文法开始符号
grammar_start = Sign('program')