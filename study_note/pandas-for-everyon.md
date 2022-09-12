# Python数据分析 活用pandas库
【美】Daniel Y.Chen 著 武传海 译
2022-9-4 buy from tb
2022-09-10 start read

## 第一部分 简介
- 可以把DataFrame看做由Series对象组成的字典，其中每个键是列名，值是Series
- 行索引可以用DataFrame.loc['行名'], 列索引可以用DataFrame['列名']
- series的一些方法p28 series[可以用bool子集选取] DataFrame相同
- DataFrame子集的一些方法 df[bool] 获取的是行，不是列 df[start:stop:step]获取的也是行切片
- 给DataFrame['列名']赋值可以创建一个新列

## 第二部分 数据处理
- 整洁数据：
-- 每个观测值成一行
-- 每个变量成一列
-- 每种观测单元构成一张表格

