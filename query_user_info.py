import xlrd
import xlwings
import re
import  query_addr_region


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
    # 设备地址
    user_addvice_addr = first_row.index('设备地址')
    user_addvice_addr_list = sheet1.col_values(user_addvice_addr)
    # 设备类别
    user_type = first_row.index('设备类别')
    user_type_list = sheet1.col_values(user_type)

    user_info_map = {}
    for i in range(1, len(user_name_id_list)):
        user_name_id = user_name_id_list[i]
        #如果单位名称已存在，更新电话号码和设备数量
        if user_info_map.get(user_name_id):
            #更新电话号码
            user_info_map[user_name_id][0].update((user_phone_1_list[i], user_phone_2_list[i],
                          user_phone_3_list[i]))
            #统计设备数量
            if user_info_map[user_name_id][2].get(user_type_list[i]):
                user_type_num = user_info_map[user_name_id][2][user_type_list[i]]
                user_info_map[user_name_id][2][user_type_list[i]] = user_type_num + 1
            else:
                user_info_map[user_name_id][2][user_type_list[i]] = 1
        else:
            user_phone= set((user_phone_1_list[i], user_phone_2_list[i],
                          user_phone_3_list[i]))
            user_info_map[user_name_id] = [user_phone, user_addvice_addr_list[i], {user_type_list[i]:1}]

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
        region_list = list(query_addr_region.load_addr_region('region_info.xlsx'))
        
        for i in range(2, nrow + 1):
            user_name = load_sheet.range(i, 1).value

            #设备地址
            user_info = user_info_map.get(user_name, '')
            if user_info:
                load_sheet['{}{}'.format('D', i)].value = '/'.join(user_info[0])
                #过滤娄桥之前的地址信息
                user_advice_addr = user_info[1]
                user_advice_addr = re.sub(pat, '', user_advice_addr)
                load_sheet['{}{}'.format('E', i)].value = user_advice_addr
                load_sheet['{}{}'.format('F', i)].value = str(user_info[2])
                #查询地址所属片区
                load_sheet['{}{}'.format(
                    'G', i)].value = query_addr_region.query_region(
                        user_advice_addr, region_list)

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
    user_info_map = load_user_info('excelExport20210723.xlsx')
    load_user_phone('7.23未分类评价单位整理.xls', user_info_map)
