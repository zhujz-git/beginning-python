# Python 数据科学手册 python data science handbook
【美】Jake VanderPlas著 陶俊杰 陈小莉 译

## 第一章 IPython:超越Python
- ipython中help()和?可以获取相关文档，??可以获取源代码。
- %paste %cpaste 粘贴代码块 %magic %lsmagic 魔法函数的帮助
- IPython 的输入输出对象 In Out 列表 可以利用之前的结果参与后续的运算
- 使用!可以IPython中执行shell命令 可以将结果赋值给python变量

## 第二章 Numpy入门
- numpy初始化函数：zeros,ones, full, arange, lispace, random.random, random.normal, randint, eye;
- ndarray的属性有 ndim(维度), shape(维度的大小，形状), size(总大小), dtype(类型), itemsize(元素大小), nbytes(总大小)
- 数组切片返回的是视图而非副本
- np.newaxis 来进行reshape np.concatenate,np.vstack,np.hstack可以拼接数组 np.split, np.hsplit, np.vsplit可以分裂数组
- python(CPython)处理有些操作是非常慢，因为操作时需要做数据类型检查和函数调度
- numpy的通用函数可以指定输出(out参数) 聚合函数通用函数都可以调用reduce函数对对象进行聚合运算。accumulate可以保存中间结果
- 任何通用函数都可以用outer方法获得两个不同输入数组所有元素对的函数运算结果。
- axis关键字指定的是数组将会呗折叠的维度，而不是将要返回的维度。
- numpy广播的可视化图标，很好理解p57
- 广播规则 
   - 规则1：如果两个数组的维度不同，那么小维度数组的形状将会在最左边补1
   - 规则2：如果两个数组的形状在任何一个维度上都不匹配，那么数组的形状会沿着维度为1的维度扩展以匹配另外一个数组的形状
   - 规则3：如果两个数组的形状在任何一个维度上都不匹配并且没有任何一个维度等于1，那么会引发异常。
- 关键字and/or(整个对象)逻辑操作运算符%/|(每个对象中的比特位)的区别 

## Pandas数据处理
- 你可以把Pandas的Series对象看成一种特殊的python字典，(一种将类型键映射到一组类型值的数据结构)
- pandas的append()不直接更新原有对象的值，而是为合并后的数据创建一个新对象。如果你需要进行多个append操作，建议先创建一个DataFrame列表，然后用concat函数一次性解决所有合并任务。
- 