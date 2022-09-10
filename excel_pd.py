import pandas as pd


''' 
    excel pandas 操作基础模块 by zhujz
'''

# 导入excel数据源 pandas版本 可以将多个文件合并
def read_excel_pd(flist, query_list, index_col=0):
    '''
        flist 文件列表或者可迭代对象
        query_list  查询的列名称
        index_col Index列名或者索引
        返回一个合并的DataFrame
    '''
    df_list = []
    for fname in flist:
        df_list.append(pd.read_excel(fname, index_col=index_col, usecols=query_list))
    return pd.concat(df_list)