import xlrd
import xlwings


def load_user_info(filepath):
    workbook = xlrd.open_workbook(filepath)
    sheet1 = workbook.sheet_by_index(0)
    first_row = sheet1.row_values(0)
    # 使用单位名称
    user_name_id = first_row.index('使用单位')
    user_name_id_list = sheet1.col_values(user_name_id)
    # 法人(负责人)电话
    user_phone_1 = first_row.index('法人(负责人)电话')
    user_phone_1_list = sheet1.col_values(user_phone_1)
    # 安管人员电话
    user_phone_2 = first_row.index('安管人员电话')
    user_phone_2_list = sheet1.col_values(user_phone_2)
    # 安管人员手机
    user_phone_3 = first_row.index('安管人员手机')
    user_phone_3_list = sheet1.col_values(user_phone_3)

    user_info_map = {
        user_name_id_list[i]:
        '{}/{}/{}'.format(user_phone_1_list[i], user_phone_2_list[i],
                          user_phone_3_list[i])
        for i in range(1, len(user_name_id_list))
    }

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
            user_name = load_sheet.range(i, 4).value
            print(user_info_map.get(user_name, ''))
            load_sheet['{}{}'.format('I', i)].value = user_info_map.get(
                user_name, '')

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


user_info_map = load_user_info('excelExport.xlsx')

load_user_phone('20210705 超期未检.xlsx', user_info_map)
