import xlrd
import xlwings
import re
import  query_addr_region


def load_user_info(filepath):
    workbook = xlrd.open_workbook(filepath)
    sheet1 = workbook.sheet_by_index(0)
    first_row = sheet1.row_values(0)
    # 企业名称
    user_name_id = first_row.index('企业名称')
    user_name_id_list = sheet1.col_values(user_name_id)
    # 法人(负责人)电话
    user_phone = first_row.index('电话')
    user_phone_list = sheet1.col_values(user_phone)
    # 设备地址
    user_addr = first_row.index('经营地址')
    user_addr_list = sheet1.col_values(user_addr)
    # 设备类别
    user_addr_2 = first_row.index('经营地址1')
    user_addr_2_list = sheet1.col_values(user_addr_2)

    user_info_map = {}
    for i in range(1, len(user_name_id_list)):
        user_name_id = user_name_id_list[i]
        user_info_map[user_name_id] = [
            #0:手机号码 1:住所 2:经营地址
            user_phone_list[i], user_addr_list[i], user_addr_2_list[i]
        ]

    return user_info_map


def load_user_phone(filepath, user_info_map):
    try:
        app = xlwings.App(add_book=False)
        workbook = app.books.open(filepath)

        load_sheet = workbook.sheets[0]

        # 获取 行与列
        info = load_sheet.used_range
        nrow = info.last_cell.row
        pat = r'浙江省|温州市|瓯海区|娄桥街道'
        #导入片区信息
        #region_list = list(query_addr_region.load_addr_region('region_info.xlsx'))

        for i in range(2, nrow + 1):
            user_name = load_sheet.range(i, 2).value

            #设备地址
            user_info = user_info_map.get(user_name, '')
            if user_info:
                #0:手机号码 1:住所 2:经营地址
                load_sheet['{}{}'.format('I', i)].value = user_info[0]
                #过滤娄桥之前的地址信息
                user_advice_addr = user_info[1]
                user_advice_addr = re.sub(pat, '', user_advice_addr)
                load_sheet['{}{}'.format('J', i)].value = user_advice_addr
                user_advice_addr = user_info[2]
                user_advice_addr = re.sub(pat, '', user_advice_addr)
                load_sheet['{}{}'.format('K', i)].value = user_advice_addr
            else:
                load_sheet['{}{}'.format('J', i)].value = '未查到该单位'

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
    user_info_map = load_user_info('Book1.xls')
    #user_info_map.update(load_user_info('娄桥市场主体名单2.xls'))
    load_user_phone('9-14系统导出未激活.xlsx', user_info_map)
