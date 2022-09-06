import xlrd
import xlwings


# 查询excel文件里的数据，返回一个字典
def load_source_data(filename, key_vol, query_list):
    workbook = xlrd.open_workbook(filename)
    sheet1 = workbook.sheet_by_index(0)
    first_row = sheet1.row_values(0)

    # 查询关键字列数据
    col_values = []
    key_id = first_row.index(key_vol)
    key_values = sheet1.col_values(key_id)

    # 查询需要的数据列
    for col_name in query_list:
        colid = first_row.index(col_name)
        val_list = sheet1.col_values(colid)
        col_values.append(val_list)

    # 筛选查询数据 后续用pandas或者numpy改进
    user_info_map = {}
    # for i in range(1, len(key_values)):
    for i, key_value in enumerate(key_values[1:]):
        user_info_map[key_value] = [
            col_values[j][i] for j in range(0, len(col_values))
        ]

    print('success query source data.')
    return user_info_map


def set_dest_data(filename, user_info_map, vol_list, query_list):
    try:
        app = xlwings.App(add_book=False)
        workbook = app.books.open(filename)
        load_sheet = workbook.sheets[0]

        # 关键字在第几列
        key_vol = 1
        # 从第几行开始（排除标题行）
        start_row = 2

        for i, vol_id in enumerate(vol_list):
            load_sheet['{}{}'.format(vol_id, 1)].value = query_list[i]
        # 获取 行与列
        info = load_sheet.used_range
        nrow = info.last_cell.row

        for i in range(start_row, nrow + 1):
            user_name = load_sheet.range(i, key_vol).value.strip()

            # 关键字查询
            user_info = user_info_map.get(user_name, '')

            if user_info:
                # 根据查询条件 将要查询的数据填充
                for vol_id in range(len(vol_list)):
                    load_sheet['{}{}'.format(vol_list[vol_id],
                                             i)].value = user_info[vol_id]
            else:
                load_sheet['{}{}'.format(vol_list[0], i)].value = '未查到该单位'

        # 保存文件
        workbook.save()
        # 关闭工作表
        workbook.close()
        print('success set dest data file.')
    except Exception as e:
        print(e)
        # 退出程序
        app.quit()
        return
    app.quit()


def query_market_excel():
    # 查询信息列，第一列为搜索键
    key_vol = '企业名称'
    query_list = ['法定代表人', '电话', '经营地址']
    vol_list = ['I', 'J', 'K']

    user_info_map = {}
    # 原文件
    flist = [
        './pydata/20220901/娄桥-房屋介绍2022.8.15.xls',
        './pydata/20220901/娄桥-教育培训公司2022.8.15.xls',
        './pydata/20220901/娄桥-装修装饰公司2022.8.15.xls',
        './pydata/20220901/汽车销售-娄桥市场主体名单.xls'
    ]
    # 目标文件
    set_filename = './pydata/20220901/名单汇总.xlsx'

    # 获取表格数据
    for fname in flist:
        user_info_map.update(load_source_data(fname, key_vol, query_list))

    # 根据源数据，写入目标文件
    set_dest_data(set_filename, user_info_map, vol_list, query_list)


if __name__ == '__main__':
    query_market_excel()
