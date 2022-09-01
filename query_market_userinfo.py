import xlrd
import xlwings


def load_user_info(filepath):
    workbook = xlrd.open_workbook(filepath)
    sheet1 = workbook.sheet_by_index(0)
    first_row = sheet1.row_values(0)

    #查询信息列，第一列为搜索键
    query_list = ['企业名称', '法定代表人', '电话', '经营地址']
    col_values = []
    for col_name in query_list:
        colid = first_row.index(col_name)
        val_list = sheet1.col_values(colid)
        col_values.append(val_list)
 
    #筛选查询数据 后续用pandas或者numpy改进
    user_info_map = {}
    for i in range(1, len(col_values[0])):
        user_name_id = col_values[0][i]
        user_info_map[user_name_id] = [col_values[j][i]
                                       for j in range(1, len(col_values))]

    return user_info_map


def load_user_phone(filepath, user_info_map):
    try:
        app = xlwings.App(add_book=False)
        workbook = app.books.open(filepath)

        load_sheet = workbook.sheets[0]

        # 获取 行与列
        info = load_sheet.used_range
        nrow = info.last_cell.row

        for i in range(2, nrow + 1):
            user_name = load_sheet.range(i, 1).value.strip()

            #设备地址
            user_info = user_info_map.get(user_name, '')

            if user_info:
                #根据查询条件 将要查询的数据填充
                load_sheet['{}{}'.format('I', i)].value = user_info[0]
                load_sheet['{}{}'.format('J', i)].value = user_info[1]
                load_sheet['{}{}'.format('K', i)].value = user_info[2] 
            else:
                load_sheet['{}{}'.format('I', i)].value = '未查到该单位'

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

if __name__ == '__main__':
    user_info_map = load_user_info('./pydata/20220901/娄桥-房屋介绍2022.8.15.xls')
    user_info_map.update(
        load_user_info('./pydata/20220901/娄桥-教育培训公司2022.8.15.xls'))
    user_info_map.update(
        load_user_info('./pydata/20220901/娄桥-装修装饰公司2022.8.15.xls'))
    user_info_map.update(load_user_info('./pydata/20220901/汽车销售-娄桥市场主体名单.xls'))

    load_user_phone('./pydata/20220901/名单汇总.xlsx', user_info_map)
