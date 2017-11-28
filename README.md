# C(缩减版)语言编译器前端
## 是什么
NUAA 2017年编译原理课设，词法分析使用正则表达式，语法分析使用LL(1)文法分析器，语义分析使用自上而下翻译，使用 Python 语言编写，面向配置化，稍加改造可以适用其他文法

## 怎么使用
```
git clone https://github.com/FlyAndNotDown/CSub-CompilerFrontend.git
```
在 PyCharm 中打开新建项目导入代码即可，Python 使用版本为 3 以上，请不要使用 Python2 运行该项目

## 代码结构说明
* main.py 编译器主程序
* error.py 存放错误相关的类和代码
* test.c 要编译的文件
* lexical 词法分析
* syntax 语法分析
* semantic 语义分析

另外，三大分析中 rule.py 即是支持编译器的所有文法、词法、语义规则，加以改动即可面向一些其他的文法和语言使用
