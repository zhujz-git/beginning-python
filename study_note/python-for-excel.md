# Excel + Python 飞速搞定数据分析与处理
python for excel 【瑞士】Felix Zumstein 著 冯黎 译
2022-9-4 buy from tb

## 第三章
+ Ctrl + / 注释快捷键
+ 用bool构造器来检查一下对象是True还是False bool(some expression)
+ f字符串 f"{变量名}"来处理字符串包含的变量
+ 第三方库文档可以在PyPI中搜索对应的包 
+ 字典解包(unpack)
    {**dict_name1, **dict_name2} python3.9引入了管道符号 dict_name1 | dict_name2
+ 条件表达式或者三元运算符
    print('') if is_pre else xxx
+ 迭代时需要用到计数器 enumerate
    for i, item in enumerate(items): print(i, item47887)
+ 增强复制 n += 1, n -= 1
+ python允许返回以逗号隔开的多个返回值，方便使用
+ PEP（Python Enhancement Proposals)Python改进提案

## 第四章Numpy基础
+ 导入惯例：import numpy as np
+ 通用函数（universal function) ufunc 会对Numpy数组中的每个元素执行操作
+ axis=0 表示以行为轴，axis=1表示以列为轴 (轴的意思就是 只剩这一维)
+ Numpy数组切片时，返回的是视图(view) arrar.copy 函数可以返回一个副本

## 第五章 使用pandas进行数据分析
- 可以用Jupter笔记本和pandas将Excel取而代之
- DataFrame Series
- 与python内置切片语法不同，pandas的标签切片(df.loc)是闭区间(包含区间首尾)
- iloc(整数位置切片, 标准的半开半闭区间)
- lambda表达式: lambda arg1, arg2,...:return_value
- DataFrame的方法返回的是副本，需要将返回值赋值 例： df_xl = df_xl.set_index('时间')

## 第六章 使用pandas进行时序分析
- 时序分析暂时还用不到，如果有金融或者其他领域的需求可以再深入了解

## 第七章 实用pandas操作Excel文件
- 遍历文件夹里的文件可以用 pathlib的 Path类 rglob方法（p127)
- read_excel参数表格(p132) 
- 写入有to_excel和ExcelWriter类

## 第八章 实用读写包操作Excel文件
第四部分内容暂时还用不到，略过了。
2022-9-9

