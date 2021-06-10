import re
import sys
import xlwings
import xlrd

def read_comb_list(filepath):
    # 组合以start_combation 并指定组合尺码数量和总行数
    start_comb_pat = re.compile(r'\[start_combation\]:(\d+)%(\d+)')

    # 标签名+标签内容
    comb_list_pat = re.compile(r'\[(\w+)\]:(\w+)')

    comb_data = {}
    comb_list = []
    with open(filepath, encoding='utf-8') as comb_file:
        match_obj = re.match(start_comb_pat, comb_file.readline())
        # 尺码数量
        comb_num = int(match_obj.group(1))
        # 总的SKU数量
        line_num = int(match_obj.group(2))

        # 读取基础信息
        for i in range(3):
            match_obj = re.match(comb_list_pat, comb_file.readline())
            comb_data[match_obj.group(1)] = match_obj.group(2)

        # 读取所有组合列表
        for i in range(line_num):
            comb_list.append(comb_file.readline().rstrip().split(':'))

        # 颜色数量
        color_num = int(line_num / comb_num)
        for i in range(color_num):
            # 一个组合里面的商品数量
            goods_num = int(
                re.match(comb_list_pat, comb_file.readline()).group(2))
            goods_id_list = []
            for j in range(goods_num):
                tmpline = comb_file.readline().split(':')
                # 不分尺码
                if len(tmpline) == 1:
                    goods_id_list.append([tmpline[0].rstrip()] * comb_num)
                # 根据冒号后面的尺码列表进行拼接
                else:
                    kclist = tmpline[1].rstrip().split()
                    goods_id_list.append(
                        [tmpline[0] + kclist[k] for k in range(comb_num)])
            # 将拼接好的商品编码ID放入每个组合编码后面
            for lnum in range(comb_num):
                comb_list[(i * comb_num) + lnum].append(
                    [goodsid[lnum] for goodsid in goods_id_list])
    comb_data['comblist'] = comb_list
    return comb_data


def write_data_to_excel(filepath, comb_data, goods_data):
    # 打开excel文件
    try:
        app = xlwings.App(add_book=False)
        workbook = app.books.open(filepath)

        load_sheet = workbook.sheets[0]

        str_brand = comb_data['brand']
        str_classify = comb_data['classify']
        str_sellingprice = comb_data['sellingprice']
        comb_list = comb_data['comblist']
        line_num = 2
        for comb in comb_list:
            # <必填>组合商品编码
            load_sheet['{}{}'.format('A', line_num)].value = comb[0]
            # 条码
            load_sheet['{}{}'.format('B', line_num)].value = comb[0]
            # <必填>组合商品名称
            load_sheet['{}{}'.format('C', line_num)].value = comb[1]
            # 品牌
            load_sheet['{}{}'.format('D', line_num)].value = str_brand
            # 分类
            load_sheet['{}{}'.format('E', line_num)].value = str_classify
            # 标准售价
            load_sheet['{}{}'.format('F', line_num)].value = str_sellingprice
            for goodsid in comb[2]:
                # <必填>子商品编码
                load_sheet['{}{}'.format('H', line_num)].value = goodsid
                load_sheet['{}{}'.format('I',
                                         line_num)].value = goods_data[goodsid]
                # <必填>子商品数量
                load_sheet['{}{}'.format('J', line_num)].value = 1

                line_num += 1
        # 保存文件
        workbook.save()
        # 关闭工作表
        workbook.close()
    except IndexError as e:
        print(e)
        # 退出程序
        app.quit()
        return
    app.quit()

def read_goods_info(filepath):
    workbook = xlrd.open_workbook(filepath)
    sheet1 = workbook.sheet_by_index(0)
    first_row = sheet1.row_values(0)
    # 商品编码
    goods_id = first_row.index('商品编码')
    goods_id_list = sheet1.col_values(goods_id)
    # 商品名称
    goods_name = first_row.index('商品名称')
    goods_name_list = sheet1.col_values(goods_name)
    # 规格编码
    spec_id = first_row.index('规格编码')
    spec_id_list = sheet1.col_values(spec_id)
    # 规格值2
    spec_name = first_row.index('规格值2')
    spec_name_list = sheet1.col_values(spec_name)

    goods_data = {}
    last_str_goods_name = ''
    ishavespec = False
    isfirstspec = False
    for row_num in range(1, len(goods_id_list)):
        str_spec_id = spec_id_list[row_num]
        str_goods_name = goods_name_list[row_num]
        if str_spec_id != '':
            ishavespec = True
        else:
            ishavespec = False

        if str_goods_name != '':
            isfirstspec = True
        else:
            isfirstspec = False
        # 如果规格编码为空则不带规格，如果商品名称为空，应该讲最近的一个商品名称作为基础商品名称
        if ishavespec:
            if isfirstspec:
                last_str_goods_name = goods_name_list[row_num]
                isfirstspec = False
            str_goods_id = spec_id_list[row_num]
            str_goods_name = last_str_goods_name + spec_name_list[row_num]
        else:
            str_goods_id = goods_id_list[row_num]
            str_goods_name = goods_name_list[row_num]
            ishavespec = False

        goods_data[str_goods_id] = str_goods_name

    return goods_data



# 使用命令行指定组合文件路径
filepath = sys.argv[1]
goods_data = read_goods_info('~\\' + filepath + '\\goodsinfo.xlsx')

comb_data = read_comb_list('~\\' + filepath + '\\combination_list.dt')
write_data_to_excel('~\\' + filepath + '\\comb_data_input.xlsx', comb_data,
                    goods_data)
