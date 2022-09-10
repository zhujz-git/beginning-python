import sys
import xlrd
import xlwings
import get_user_filepath
import excel_pd
import pandas as pd

'''
    将ERP里导出的组合商品信息，导入到组合商品信息列表，手工设置好重量
'''
def lead_comb_info(filepath):
    workbook = xlrd.open_workbook(filepath)
    sheet1 = workbook.sheet_by_index(0)
    first_row = sheet1.row_values(0)
    # 组合商品编码
    index_comb_id = first_row.index('组合商品编码')
    comb_id_list = sheet1.col_values(index_comb_id)
    # 组合商品名称
    index_comb_name = first_row.index('组合商品名称')
    comb_name_list = sheet1.col_values(index_comb_name)
    # 去掉空行, 第一行不用
    comb_info_list = [(comb_id_list[i], comb_name_list[i])
                      for i in range(1, len(comb_id_list))
                      if comb_name_list[i] != '']
    return comb_info_list


def check_comb_info(filepath, df_comb):
    try:
         # 默认查询关键字列在第一列
        df_dest = pd.read_excel(filepath, index_col=0)
        df_update = df_dest.append(df_comb).drop_duplicates(['组合商品名称']).dropna()
        

        app = xlwings.App(add_book=False)
        workbook = app.books.open(filepath)
        load_sheet = workbook.sheets[0]        

        load_sheet['A1'].value = df_update     
        #格式复制  
        #load_sheet['A2:B3'].copy()
        #load_sheet.range('A2', load_sheet.used_range.last_cell).paste('formats')

        # 保存文件
        workbook.save()
        # 关闭工作表
        workbook.close()
    except Exception as e:
        print(e)
        # 退出程序
        app.quit()
        return
    app.quit()


filepath = get_user_filepath.get_file_path_addmonth()
filelist = [filepath + '\\combination_info1.xlsx']
df_comb = excel_pd.read_excel_pd(filelist, ['组合商品编码', '组合商品名称'])
df_comb.dropna()

check_comb_info(filepath + '\\combination_weight.xlsx',
                               df_comb)
