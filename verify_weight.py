import xlrd
import xlwings
import get_user_filepath


def read_product(filepath):
    """
        读取组合商品编码和重量，返回一个字典
    """
    # 打开excel文件
    try:
        workbook = xlrd.open_workbook(filepath)
    except PermissionError:
        print('请先关闭文件')
        exit

    # 获取工作表
    sheet1 = workbook.sheet_by_index(0)

    # 组合商品编码和重量
    product_code = [str(j).strip() for j in sheet1.col_values(0)]

    product_weight = sheet1.col_values(2)

    # 组合成一个字典，以便后续查询
    product_codes = dict(zip(product_code, product_weight))

    return product_codes


def read_orders(filepath):
    """
        读取订单数据，获取快递单号和对应的商品编码
    """
    # 打开excel文件
    workbook = xlrd.open_workbook(filepath)

    # 获取工作表
    sheet1 = workbook.sheet_by_index(0)
    first_row = sheet1.row_values(0)
    try:
        tracking_number_id = first_row.index('快递单号')
        order_comment_id = first_row.index('备注')
        product_count_id = first_row.index('数量')
        product_code_id = first_row.index('商品编码')
    except ValueError:
        print(ValueError, first_row)
        return

    order_list = {}
    for i in range(1, sheet1.nrows):
        row = sheet1.row_values(i)
        # 读取订单快递单号
        tracking_number = row[tracking_number_id].strip()

        # 读取订单备注
        order_comment = row[order_comment_id].strip()

        # 读取商品数量
        try:
            product_count = int(row[product_count_id])
        except ValueError:
            print(ValueError, row[product_count_id])
            continue

        # 创建一个商品元组，包含商品数量 商品编码 订单备注
        product_element = (product_count, row[product_code_id].strip(),
                           order_comment)

        # 如果快递单号已存在，则是多个商品，将该商品放入上一行的商品列表中
        try:
            order_list[tracking_number]['product_list'].append(product_element)
        except KeyError:
            order_list[tracking_number] = {'product_list': [product_element]}

    return order_list


def verify_weight(filepath, product_codes, order_list):

    # 打开excel文件
    app = xlwings.App(add_book=False)
    workbook = app.books.open(filepath)

    load_sheet = workbook.sheets[0]

    # 获取 行与列
    info = load_sheet.used_range
    nrow = info.last_cell.row
    ncol = info.last_cell.column

    range_val = load_sheet.range(
        (1, 1),  # 获取 第一行 第一列
        (nrow, ncol)  # 获取 第 nrow 行 第 ncol 列
    ).value
    # 获取工作表
    for i in range(1, nrow):
        # 读取一行数据
        row = range_val[i]

        # 设置外包装瓦楞纸价格为0
        packaging_price = 0
        # 快递单号
        tracking_number = str(row[0]).strip()
        order_comment = ''

        # 空行则跳过
        if tracking_number == 'None':
            continue

        try:
            # 获取快递单号对应的商品列表
            product_list = order_list[tracking_number]['product_list']
        except KeyError:
            print('不能找到快递单号：' + tracking_number)
            continue

        product_weight = ''
        order_comment = ''

        # 遍歷元組列表
        for product_element in product_list:
            # 获取组合商品数量 编码 备注
            product_number = product_element[0]
            product_code = product_element[1]
            order_comment += product_element[2]
            if product_code == '0001':
                product_weight = '线下商品'
                continue

            try:
                # 获取商品对应的重量
                product_weight += str(product_codes[
                    product_code.strip()]) + '*' + str(product_number) + '; '

                # 设置瓦楞纸箱价格
                if int(product_codes[product_code.strip()]) >= 2:
                    packaging_price = 3
            except KeyError:
                if (product_code.find('YL') >=
                        0) or (product_code.find('PZ') >=
                               0) or (product_code.find('KC') >= 0):
                    product_code = '单件'
                    # 获取商品对应的重量
                    product_weight += str(product_codes[product_code.strip()]
                                          ) + '*' + str(product_number) + '; '
                else:
                    print('不能找到商品编码单号：' + product_code)
                    continue
        # 写入查询后的重量
        load_sheet.range((i + 1, 4)).value = product_weight
        load_sheet.range((i + 1, 5)).value = packaging_price
        load_sheet.range((i + 1, 6)).value = order_comment

    # 保存文件
    workbook.save()
    # 关闭工作表
    workbook.close()
    # 退出程序
    app.quit()


# month = sys.argv[2]
# 获取月份文件夹
filepath = get_user_filepath.get_file_path_addmonth()
# 读取组合商品重量
product_codes = read_product(filepath + '\\combination_weight.xlsx')
# 读取订单数据
order_list = read_orders(filepath + '\\order_list.xlsx')
# 核对
verify_weight(filepath + '\\居家族  7月 - 副本.xls', product_codes, order_list)
