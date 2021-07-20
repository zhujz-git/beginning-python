import sys
import xlrd
import xlwings
import get_user_filepath


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


def check_comb_info(filepath, comb_id_name_list):
    try:
        app = xlwings.App(add_book=False)
        workbook = app.books.open(filepath)

        load_sheet = workbook.sheets[0]

        # 获取 行与列
        info = load_sheet.used_range
        nrow = info.last_cell.row

        range_val = load_sheet.range(
            (2, 1),  # 获取 第2行 第1列
            (nrow, 2)  # 获取 第 nrow 行 第 ncol 列
        ).value
        comb_data = {value[0]: value[1] for value in range_val}

        row_num = nrow + 1
        for comb_val in comb_id_name_list:
            if comb_data.get(comb_val[0]) is None:
                load_sheet['{}{}'.format('A', row_num)].value = comb_val[0]
                load_sheet['{}{}'.format('B', row_num)].value = comb_val[1]
                row_num += 1

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

comb_info = lead_comb_info(filepath + '\\combination_info.xlsx')

check_comb_info(filepath + '\\combination_weight.xlsx',
                               comb_info)
