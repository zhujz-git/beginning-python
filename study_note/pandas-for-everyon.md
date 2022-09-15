# Python数据分析 活用pandas库
【美】Daniel Y.Chen 著 武传海 译
2022-9-4 buy from tb
2022-09-10 start read

## 第一部分 简介
- 可以把DataFrame看做由Series对象组成的字典，其中每个键是列名，值是Series
- 行索引可以用DataFrame.loc['行名'], 列索引可以用DataFrame['列名']
- series的一些方法p28 series[可以用bool子集选取] DataFrame相同
- DataFrame子集的一些方法 df[bool] 获取的是行，不是列 df[start:stop:step]获取的也是行切片

## 第二部分 数据处理
- pandas的许多函数和方法都有inplace参数，用于控制是否基于原对象复制操作。
- 插值-interpolate方法
- melt函数（数据融合） DataFrame.列名 可以访问相应列
- split之后可以用.str方法的get方法获取想要的新列
- *操作符可以对容器拆包
- pivot_table展开方法
- 用rang函数给一个列赋值，可以设置好索引
- glob模块的glob.glob可以获得文件夹里的所有数据

## 第三部分 数据整理
@装饰器可以将普通函数向量化 @np.vectorize