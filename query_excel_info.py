import xlrd
import xlwings
import pandas as pd
import excel_pd
import traceback



# 查询excel文件里的数据，返回一个字典
# 文件名，索引信息列，query_list为要查询的信息列表，以列名列出
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
    for i, key_value in enumerate(key_values[1:]):
        user_info_map[key_value] = [
            col_values[j][i+1] for j in range(0, len(col_values))
        ]

    print('success query source data.')
    return user_info_map



# filename 文件名 
# user_info_map 前面查询到的信息数据库
# vol_list 要查询到的EXCEL信息列，A,B,C
# 关键字在第几列
# 信息列名称，直接填充
def set_dest_data(filename, user_info_map, vol_list, query_list,key_vol=1):
    try:
        app = xlwings.App(add_book=False)
        workbook = app.books.open(filename)
        load_sheet = workbook.sheets[0]

        
        # 从第几行开始（排除标题行）
        start_row = 2

        # 填充好标题行
        #for i, vol_id in enumerate(vol_list):
        #    load_sheet['{}{}'.format(vol_id, start_row-1)].value = query_list[i]

        # 获取 行与列
        info = load_sheet.used_range
        nrow = info.last_cell.row

        print('start process 总共行数：')
        print(nrow)
        for i in range(start_row, nrow + 1):
            try:
                user_name = load_sheet.range(i, key_vol).value.strip()
            except AttributeError as e:
                # 跳过空行
                print(e)
                continue
            # 关键字查询
            user_info = user_info_map.get(user_name)

            if user_info:
                # 根据查询条件 将要查询的数据填充
                for j, vol in enumerate(vol_list):
                    scell = '{}{}'.format(vol, i)
                    load_sheet[scell].value = user_info[j]
                     
                    #load_sheet['{}{}'.format(vol, i)].value = '异常''

                #整行标颜色
                load_sheet.range(i, 1).expand('right').color = (84, 255, 159) 
            #else:
                #load_sheet['{}{}'.format(vol_list[0], i)].value = ' '

        # 保存文件
        workbook.save()
        # 关闭工作表
        workbook.close()
        print('success set dest data file.')
    except Exception as e:
        print(traceback.format_exc())
        # 退出程序
        app.quit()
        return
    app.quit()

# pandas版本 topleft_range:要写入的左上角单元格  index_col:关键字列次
def set_dest_datafile_pd(filename, uinfo_df, topleft_range, index_col=0):
    try:
        # 默认查询关键字列在第一列
        df_dest = pd.read_excel(filename, index_col=index_col, usecols=[index_col])
        df_jion = df_dest.join(uinfo_df, how='left')
        # 替换下nan字符
        df_jion = df_jion.fillna({'联系人手机号': '号码空的'})

        app = xlwings.App(add_book=False)
        workbook = app.books.open(filename)
        load_sheet = workbook.sheets[0]
        # 自动调整列宽
        load_sheet.autofit('c')

        load_sheet[topleft_range].options(index=False).value = df_jion

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
    query_list = ['单位名称', '注册地址']
    topleft_range = 'I1'

    # 原文件
    flist = ['./pandas_excel/xl/已自我声明公开导出标准2024-07-25.xlsx']
    # 目标文件
    set_filename = './pandas_excel/xl/瞿溪规上企业.xlsx'

    # 获取表格数据
    df_source = excel_pd.read_excel_pd(flist, query_list)
    # 根据源数据，写入目标文件
    set_dest_datafile_pd(set_filename, df_source, topleft_range, '单位名称')

def query_excel():
    filename = './pandas_excel/xl/企业.xls'
    user_info_map = load_source_data(filename, '企业名称', ['住所','法定代表人(负责人、执行事务合伙人)','电话'])
   
    filename = './pandas_excel/xl/个体.xls'
    user_info_map_2 = load_source_data(filename, '企业名称', ['住所','法定代表人(负责人、执行事务合伙人)','电话'])
    user_info_map.update(user_info_map_2)
   
    dest_name = 'D:\\瞿溪市监所\\产品质量科\\2025年瓯海区鞋类产品质量整治提升\鞋类生产企业底数\\鞋类和个体.xlsx'
    set_dest_data(dest_name, user_info_map, ['G','H','I'],['登记住所','联系人','联系方式'])

def query_20250425():
    # 2025年4月 查询准入中已列异名单，将异已列异的进行标记
            
    filename = 'C:\\Users\\Administrator\\Downloads\\经营异常列入信息导出-2025年04月25日.xls'
    user_info_map = load_source_data(filename, '主体名称', ['申请日期'])

    dest_name = 'D:\\瞿溪市监所\\信用监管\\年报\\年报分类名单管理导出-未年报 虚拟地址.xls'
    set_dest_data(dest_name, user_info_map, 'K',['是否已列异'])


def query_20250310():
    # 2025年3月 放心消费单元清理 查询准入中已注销名单和已列异名单，将异常经营单元进行清理。
    filename = './pandas_excel/20250310/注销简单查询_20250310.xls'
    user_info_map = load_source_data(filename, '企业名称', ['注销日期'])

    filename = './pandas_excel/20250310/企业经营异常名录导出-2025年03月10日.xls'
    user_info_map1 = load_source_data(filename, '企业名称', ['状态'])
    user_info_map.update(user_info_map1)

    filename = './pandas_excel/20250310/个体瞿溪经营异常名录导出-2025年03月10日.xls'
    user_info_map1 = load_source_data(filename, '企业名称', ['状态'])
    user_info_map.update(user_info_map1)
        
    filename = './pandas_excel/20250310/农专社经营异常名录导出-2025年03月10日.xls'
    user_info_map1 = load_source_data(filename, '企业名称', ['状态'])
    user_info_map.update(user_info_map1)

    dest_name = './pandas_excel/20250310/放心消费名单有效主体表.xlsx'
    set_dest_data(dest_name, user_info_map, 'B',['经营状况'])

def query_20250310B():
    #更新年报状态
    filename = 'D:\\瞿溪市监所\\信用监管\\年报\\2025\\年报分类名单管理导出-2025年04月23日.xls'
    user_info_map = load_source_data(filename, '企业名称', ['年报状态', '年报日期'])

    dest_name = 'D:\\瞿溪市监所\\信用监管\\年报\\2025\\年报分类名单管理导出企业 无违规信用记录.xls'
    set_dest_data(dest_name, user_info_map, ['F','G'],['年报状态', '年报日期'])

def query_20250331():
    #更新虚拟地址年报状态
    filename = 'C:\\Users\\Administrator\\Downloads\\年报分类名单管理导出-2025年06月26日.xls'
    user_info_map = load_source_data(filename, '企业名称', ['年报状态', '年报日期'])

    filename = 'C:\\Users\\Administrator\\Downloads\\年报分类名单管理导出-2025年06月26日 个体 2024前.xls'
    user_info_map.update(load_source_data(filename, '企业名称', ['年报状态', '年报日期']))

    filename = 'C:\\Users\\Administrator\\Downloads\\年报分类名单管理导出-2025年06月26日个体 2024后.xls'
    user_info_map.update(load_source_data(filename, '企业名称', ['年报状态', '年报日期']))

    dest_name = 'D:\\瞿溪市监所\\信用监管\\年报\\年报分类名单管理导出-未年报 虚拟地址.xls'
    set_dest_data(dest_name, user_info_map, ['C','D'],['年报状态', '年报日期'])

def query_20250620():
    #更新未年报企业状态
    filename = 'C:\\Users\\Administrator\\Downloads\\年报分类名单管理导出-2025年06月25日.xls'
    user_info_map = load_source_data(filename, '企业名称', ['年报状态', '年报日期'])


    dest_name = 'D:\\瞿溪市监所\\信用监管\\年报\\年报分类名单管理导出-2025年06月09日 未年报企业.xls'
    set_dest_data(dest_name, user_info_map, ['F','G'],['年报状态', '年报日期'])

def filter_virtual_addr(filename, filters_str, add_column, virtual_column, agent_cloumn):
    #filename 文件名， add_column 地址列， virtual_column 虚拟地址标记列
    #filters_str 筛选列表
    
    try:
        app = xlwings.App(add_book=False)
        workbook = app.books.open(filename)
        load_sheet = workbook.sheets[0]

        # 从第几行开始（排除标题行）
        start_row = 2

        # 获取 行与列
        info = load_sheet.used_range
        nrow = info.last_cell.row

        for i in range(start_row, nrow + 1):
            try:
                user_name = load_sheet['{}{}'.format(add_column, i)].value.strip()
            except AttributeError as e:
                # 跳过空行
                print(e)
                continue
            # 关键字查询
            for filter in filters_str:
                if filter[0] in user_name:
                    load_sheet['{}{}'.format(virtual_column, i)].value = '虚拟地址' 
                    load_sheet['{}{}'.format(agent_cloumn, i)].value = filter[1]

        # 保存文件
        workbook.save()
        # 关闭工作表
        workbook.close()
        print('success set dest data file.')
    except Exception as e:
        print(traceback.format_exc())
        # 退出程序
        app.quit()
        return
    app.quit()
def query_20250314():
    #对名单进行地址筛选，基本目的为查询名单中虚拟地址的主体
    filename = 'D:\\瞿溪市监所\\信用监管\\年报\\年报分类名单管理导出-2025年06月26日未年报企业+个体.xls'
    filters_str = [['延川路58号13幢5楼511室','温州力西特创业服务有限公司-吕克凯'],
                   ['蛟雄路6号','温州稳盘胜算众创空间有限公司-吴康'],
                   ['延川路58号10幢415室','温州浙创众创空间管理有限公司-庄春秋'],
                   ['农机大楼',' '],
                   ['原钢材市场',' ']
                   ]
    filter_virtual_addr(filename, filters_str, 'N', 'O','P')

def query_20250402():
    #标准化统计监测管辖所查询
    filename = 'D:\\瞿溪市监所\\标准计量\\标准化统计监测\\2023年度列表填报数据.xlsx'
    user_info_map = load_source_data(filename, '企业名称', ['联系人', '联系方式', '管辖所'])

    dest_name = 'D:\\瞿溪市监所\\标准计量\\标准化统计监测\\2025年温州市统计监测企业名单\\工业 1.温州市9474.xlsx'
    set_dest_data(dest_name, user_info_map, ['K','L','M'],['联系人', '联系方式', '管辖所'])

def query_20250604():
    #全零申报企业查询联系方式
    filename = 'D:\\瞿溪市监所\\信用监管\\年报\\全零申报\\年报分类名单管理导出-2025年06月04日.xls'
    user_info_map = load_source_data(filename, '企业名称', ['法定代表人联系电话', '年报联络员联系电话'])

    dest_name = 'D:\\瞿溪市监所\\信用监管\\年报\\全零申报\\年报信息综合查询导出 全零申报.xlsx'
    set_dest_data(dest_name, user_info_map, ['N','P'],['法定代表人联系电话', '年报联络员联系电话'])

def query_20250609():
    #根据信用代码查询企业地址
    filename = './pandas_excel/xl/企业.xls'
    user_info_map = load_source_data(filename, '统一社会信用代码', ['住所','企业名称','电话'])
   
    filename = './pandas_excel/xl/个体.xls'
    user_info_map_2 = load_source_data(filename, '统一社会信用代码', ['住所','企业名称','电话'])
    user_info_map.update(user_info_map_2)

    dest_name = 'D:\\瞿溪市监所\\价监分局\\\家电以旧换新\\0501-0605家电12、3C价格超50-温州.xlsx'
    set_dest_data(dest_name, user_info_map, ['X','Y','Z'],['登记住所','联系人','联系方式'])


if __name__ == '__main__':
    # query_market_excel()
    
    #从导出的准入名单中查询信息
    #query_excel()


    #年报状态查询-分给朱伟 胜泽 小龙
    #query_20250310B()

    #虚拟地址筛选
    query_20250314()

    #虚拟地址年报查询
    #query_20250331()
    #query_20250425()

    #标准化统计监测
    #query_20250402()

    #全零申报企业查询联系方式
    #query_20250604()
 
    #根据信用代码查询企业地址
    #query_20250609()

    #query_20250620()