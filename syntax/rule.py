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
    def __init__(self, left_type, right_types, semantic_start, semantic_children, semantic_end):
        """
        产生式左边
        :param left_type: 产生式左边的符号类型
        :param right_types: 产生式右边的符号类型列表
        :param semantic_start: 语义操作关键字 - 开始
        :param semantic_children: 语义操作关键字 - 孩子
        :param semantic_end: 语义操作关键字 - 结束
        """
        self.left = Sign(left_type)
        self.right = list()
        for i in right_types:
            self.right.append(Sign(i))

        # 调试用的
        self.str = self.left.type + ' ->'
        for i in self.right:
            self.str += ' ' + i.type

        # 语义操作关键字
        self.semantic_start = semantic_start
        self.semantic_children = list()
        for c in semantic_children:
            self.semantic_children.append(c)
        self.semantic_end = semantic_end


"""
1.  program -> define-list
2.  define-list -> define define-list
                 | empty
3.  define -> type ID define-type
4.  define-type -> var-define-follow
                 | fun-define-follow
5.  var-define-follow -> ;
                 | [ NUM ] ;
6.  type ->    int
             | void
7.  fun-define-follow -> ( params ) code-block
8.  params -> param-list
                | empty
9.  param-list -> param param-follow
10. param-follow -> , param param-follow
                | empty
11. param -> type ID array-subscript
12. array-subscript -> [ ]
                | empty
13. code-block -> { local-define-list code-list }
14. local-define-list -> local-var-define local-define-list
                | empty
15. local-var-define -> type ID var-define-follow
16. code-list -> code code-list
                | empty
17. code -> normal-statement
                | selection-statement
                | iteration-statement
                | return-statement
18. normal-statement -> ;
                | ID normal-statement-follow
19. normal-statement-follow -> var-follow = expression ;
                | call-follow ;
20. call-follow -> ( call-params )
21. call-params -> call-param-list
                | empty
22. call-param-list -> expression call-param-follow
23. call-param-follow -> , expression call-param-follow
                | empty
24. selection-statement -> if ( expression ) { code-list } selection-follow
25. selection-follow -> else { code-list }
                | empty
26. iteration-statement -> while ( expression ) iteration-follow
27. iteration-follow -> { code-list }
                | code
28. return-statement -> return return-follow
29. return-follow -> ;
                | expression ;
30. var-follow -> [ expression ]
                | empty
31. expression -> additive-expr expression-follow
32. expression-follow -> rel-op additive-expr
                | empty
33. rel-op ->     <=
                | <
                | >
                | >=
                | ==
                | !=
34. additive-expr -> term additive-expr-follow
35. additive-expr-follow -> add-op term additive-expr-follow
                | empty
36. add-op ->     +
                | -
37. term -> factor term-follow
38. term-follow -> mul-op factor term-follow
                | empty
39. mul-op ->     *
                | /
40. factor -> ( expression )
                | ID id-factor-follow | NUM
41. id-factor-follow -> var-follow
                | ( args )
42. args -> arg-list
                | empty
43. arg-list -> expression arg-list-follow
44. arg-list-follow -> , expression arg-list-follow
                | empty
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
    # 0
    Production('program', ['define-list'],
               'Program0S', [None], 'Program0E'),
    # 1
    Production('define-list', ['define', 'define-list'],
               None, [None, None], 'DefineList0E'),
    Production('define-list', [],
               None, [], 'DefineList1E'),
    # 2
    Production('define', ['type', 'id', 'define-type'],
               None, [None, None, 'Define0C2'], 'Define0E'),
    # 3
    Production('define-type', ['var-define-follow'],
               'DefineType0S', ['DefineType0C0'], 'DefineType0E'),
    Production('define-type', ['fun-define-follow'],
               'DefineType1S', ['DefineType1C0'], 'DefineType1E'),
    # 4
    Production('var-define-follow', ['semicolon'],
               None, [None], 'VarDefineFollow0E'),
    Production('var-define-follow', ['left-bracket', 'num', 'right-bracket', 'semicolon'],
               None, [None, None, None, None], 'VarDefineFollow1E'),
    # 5
    Production('type', ['int'],
               'Type0S', [None], None),
    Production('type', ['void'],
               'Type1S', [None], None),
    # 6
    Production('fun-define-follow', ['left-parentheses', 'params', 'right-parentheses', 'code-block'],
               None, [None, 'FunDefineFollow0C1', None, 'FunDefineFollow0C3'], 'FunDefineFollow0E'),
    # 7
    Production('params', ['param-list'],
               'Params0S', ['Params0C0'], None),
    Production('params', [],
               'Params1S', [], None),
    # 8
    Production('param-list', ['param', 'param-follow'],
               None, ['ParamList0C0', 'ParamList0C1'], None),
    # 9
    Production('param-follow', ['comma', 'param', 'param-follow'],
               None, [None, 'ParamFollow0C1', 'ParamFollow0C2'], None),
    Production('param-follow', [],
               None, [], None),
    # 10
    Production('param', ['type', 'id', 'array-subscript'],
               None, [None, None, None], 'Param0E'),
    # 11
    Production('array-subscript', ['left-bracket', 'right-bracket'],
               'ArraySubscript0S', [None, None], None),
    Production('array-subscript', [],
               'ArraySubscript1S', [], None),
    # 12
    Production('code-block', ['left-brace', 'local-define-list', 'code-list', 'right-brace'],
               None, [None, 'CodeBlock0C1', 'CodeBlock0C2', None], 'CodeBlock0E'),
    # 13
    Production('local-define-list', ['local-var-define', 'local-define-list'],
               None, ['LocalVarDefine0C0', 'LocalVarDefineFollow0C1'], None),
    Production('local-define-list', [],
               None, [], None),
    # 14
    Production('local-var-define', ['type', 'id', 'var-define-follow'],
               None, [None, None, None], 'LocalVarDefine0E'),
    # 15
    Production('code-list', ['code', 'code-list'],
               None, ['CodeList0C0', 'CodeList0C1'], 'CodeList0E'),
    Production('code-list', [],
               None, [], 'CodeList1E'),
    # 16
    Production('code', ['normal-statement'],
               None, ['Code0C0'], 'Code0E'),
    Production('code', ['selection-statement'],
               None, ['Code1C0'], 'Code1E'),
    Production('code', ['iteration-statement'],
               None, ['Code2C0'], 'Code2E'),
    Production('code', ['return-statement'],
               None, ['Code3C0'], 'Code3E'),
    # Production('normal-statement', ['eval-statement', 'semicolon']),
    # Production('normal-statement', ['semicolon']),
    # 17
    Production('normal-statement', ['semicolon'],
               None, [None], 'NormalStatement0E'),
    Production('normal-statement', ['id', 'normal-statement-follow'],
               None, [None, 'NormalStatement1C1'], 'NormalStatement1E'),
    # 18
    Production('normal-statement-follow', ['var-follow', 'evaluate', 'expression', 'semicolon'],
               None, ['NormalStatementFollow0C0', None, 'NormalStatementFollow0C2', None], 'NormalStatementFollow0E'),
    Production('normal-statement-follow', ['call-follow', 'semicolon'],
               None, ['NormalStatementFollow1C0', None], 'NormalStatementFollow1E'),
    # 19
    Production('call-follow', ['left-parentheses', 'call-params', 'right-parentheses'],
               None, [None, 'CallFollow0C1', None], 'CallFollow0E'),
    # 20
    Production('call-params', ['call-param-list'],
               None, ['CallParams0C0'], 'CallParams0E'),
    Production('call-params', [],
               None, [], 'CallParams1E'),
    # 21
    Production('call-param-list', ['expression', 'call-param-follow'],
               None, ['CallParamList0C0', 'CallParamList0C1'], 'CallParamList0E'),
    # 22
    Production('call-param-follow', ['comma', 'expression', 'call-param-follow'],
               None, [None, 'CallParamFollow0C1', 'CallParamFollow0C2'], 'CallParamFollow0E'),
    Production('call-param-follow', [],
               None, [], 'CallParamFollow1E'),
    # 23
    Production('selection-statement',
               ['if', 'left-parentheses', 'expression', 'right-parentheses', 'left-brace',
                'code-list', 'right-brace', 'selection-follow'],
               None, [None, None, 'SelectionStatement0C2', None, None, None, None, None], 'SelectionStatement0E'),
    # 24
    Production('selection-follow', ['else', 'left-brace', 'code-list', 'right-brace'],
               None, [None, None, None, None], 'SelectionFollow0E'),
    Production('selection-follow', [],
               None, [], 'SelectionFollow1E'),
    # 25
    Production('iteration-statement', ['while', 'left-parentheses', 'expression',
                                       'right-parentheses', 'iteration-follow'],
               None, [None, None, 'IterationStatement0C2', None, None], 'IterationStatement0E'),
    # 26
    Production('iteration-follow', ['left-brace', 'code-list', 'right-brace'],
               None, [None, None, None], 'IterationFollow0E'),
    Production('iteration-follow', ['code'],
               None, [None], 'IterationFollow1E'),
    # 27
    Production('return-statement', ['return', 'return-follow'],
               None, [None, 'ReturnStatement0C1'], 'ReturnStatement0E'),
    # 28
    Production('return-follow', ['semicolon'],
               None, [None], 'ReturnFollow0E'),
    Production('return-follow', ['expression', 'semicolon'],
               None, ['ReturnFollow1C0', None], 'ReturnFollow1E'),
    # Production('eval-statement', ['var', 'evaluate', 'expression']),
    # Production('var', ['id', 'var-follow']),
    # 29
    Production('var-follow', ['left-bracket', 'expression', 'right-bracket'],
               None, [None, 'VarFollow0C1', None], 'VarFollow0E'),
    Production('var-follow', [],
               None, [], 'VarFollow1E'),
    # 30
    Production('expression', ['additive-expr', 'expression-follow'],
               None, ['Expression0C0', 'Expression0C1'], 'Expression0E'),
    # 31
    Production('expression-follow', ['rel-op', 'additive-expr'],
               None, [None, 'ExpressionFollow0C1'], 'ExpressionFollow0E'),
    Production('expression-follow', [],
               None, [], 'ExpressionFollow1E'),
    # 32
    Production('rel-op', ['smaller-equal'],
               None, [None], 'RelOp0E'),
    Production('rel-op', ['smaller'],
               None, [None], 'RelOp1E'),
    Production('rel-op', ['bigger'],
               None, [None], 'RelOp2E'),
    Production('rel-op', ['bigger-equal'],
               None, [None], 'RelOp3E'),
    Production('rel-op', ['equal'],
               None, [None], 'RelOp4E'),
    Production('rel-op', ['not-equal'],
               None, [None], 'RelOp5E'),
    # 33
    Production('additive-expr', ['term', 'additive-expr-follow'],
               None, ['AdditiveExpr0C0', 'AdditiveExpr0C1'], 'AdditiveExpr0E'),
    # 34
    Production('additive-expr-follow', ['add-op', 'term', 'additive-expr-follow'],
               None, [None, 'AdditiveExprFollow0C1', 'AdditiveExprFollow0C2'], 'AdditiveExprFollow0E'),
    Production('additive-expr-follow', [],
               None, [], 'AdditiveExprFollow1E'),
    # 35
    Production('add-op', ['addition'],
               None, [None], 'AddOp0E'),
    Production('add-op', ['subtraction'],
               None, [None], 'AddOp1E'),
    # 36
    Production('term', ['factor', 'term-follow'],
               None, ['Term0C0', 'Term0C1'], 'Term0E'),
    # 37
    Production('term-follow', ['mul-op', 'factor', 'term-follow'],
               None, [None, 'TermFollow0C1', 'TermFollow0C2'], 'TermFollow0E'),
    Production('term-follow', [],
               None, [], None),
    # 38
    Production('mul-op', ['multiplication'],
               None, [None], 'MulOp0E'),
    Production('mul-op', ['division'],
               None, [None], 'MulOp1E'),
    # 39
    Production('factor', ['left-parentheses', 'expression', 'right-parentheses'],
               None, [None, 'Factor0C1', None], 'Factor0E'),
    Production('factor', ['id', 'id-factor-follow'],
               None, [None, 'Factor1C1'], 'Factor1E'),
    Production('factor', ['num'],
               None, [None], 'Factor2E'),
    # 40
    Production('id-factor-follow', ['var-follow'],
               None, [None], 'IdFactorFollow0E'),
    Production('id-factor-follow', ['left-parentheses', 'args', 'right-parentheses'],
               None, [None, None, None], 'IdFactorFollow1E'),
    # 41
    Production('args', ['arg-list'],
               None, [None], 'Args0E'),
    Production('args', [],
               None, [], 'Args1E'),
    # 42
    Production('arg-list', ['expression', 'arg-list-follow'],
               None, ['ArgList0C0', 'ArgList0C1'], 'ArgList0E'),
    Production('arg-list-follow', ['comma', 'expression', 'arg-list-follow'],
               None, [None, 'ArgListFollow0C1', 'ArgListFollow0C2'], 'ArgListFollow0E'),
    Production('arg-list-follow', [],
               None, [], 'ArgListFollow1E')
]

# 文法开始符号
grammar_start = Sign('program')