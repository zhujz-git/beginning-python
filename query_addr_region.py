import xlrd

def load_addr_region(filepath):
    workbook = xlrd.open_workbook(filepath)
    sheet1 = workbook.sheet_by_index(0)
    first_row = sheet1.row_values(0)

    # 地址关键词
    user_addr_key = first_row.index('地址关键词')
    user_addr_key_list = sheet1.col_values(user_addr_key)
    # 片区
    user_region = first_row.index('片区责任人')
    user_region_list = sheet1.col_values(user_region)
    return zip(user_addr_key_list, user_region_list)

#查询地址是否匹配关键词，返回片区
def query_region(advice_addr ,region_list):
    for i in range(1, len(region_list)):
        if advice_addr.find(region_list[i][0]) >= 0:
            return region_list[i][1]

    return ''

if __name__ == '__main__':
    region_list = load_addr_region('region_info.xlsx')
    print(query_region('瓯海区娄桥街道安下村', region_list))