import xlrd
import xlwings

'''
使用此文件，将特定的一个数据文件输入，查询其是否有在另一个文件中，
专门用于浙江企业在线公众号激活清单更新使用
若要其他使用 可以稍微改写，此为第一版本
'''
def load_user_info(filepath):
    workbook = xlrd.open_workbook(filepath)
    sheet1 = workbook.sheet_by_index(0)
    first_row = sheet1.row_values(1)
    # 使用单位名称
    user_name_id = first_row.index('主体名称')
    user_name_id_list = sheet1.col_values(user_name_id)    

    user_info_set = set(user_name_id_list)
    return user_info_set


def load_user_phone(filepath, user_info_set, column_num):
    try:
        app = xlwings.App(add_book=False)
        workbook = app.books.open(filepath)

        load_sheet = workbook.sheets[0]

        # 获取 行与列
        info = load_sheet.used_range
        nrow = info.last_cell.row
        
        for i in range(2, nrow + 1):
            #如果已激活，则跳过            
            if load_sheet.range(column_num+str(i)).value == '已激活':
                continue
            user_name = load_sheet.range(i, 3).value

            #如果没在名单内，则认为已激活           
            if user_name not in user_info_set:
                str_row = '{}{}'.format(column_num, i)
                load_sheet[str_row].value = '已激活'         
                #整行标颜色
                load_sheet[i-1, 0].expand('right').color = (84, 255, 159)       
                print(user_name + ' 已激活')
                

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

def query_20250310A():
    #查询未激活清单
    user_info_set = load_user_info(\
        'D:\\瞿溪市监所\\信用监管\\触达率\\2025年\\系统导出最新未激活\\公众号未激活清单.xlsx')
    
    '企业'
    load_user_phone(\
        'D:\\瞿溪市监所\\信用监管\\触达率\\2025年\\（企业2024年成立）公众号未激活清单 - 剔除虚拟地址.xlsx', \
            user_info_set, 'F')
    
    '个体'
    load_user_phone(\
        'D:\\瞿溪市监所\\信用监管\\触达率\\2025年\\（个体户2024年成立）公众号未激活清单 - 剔除虚拟地址.xlsx', \
            user_info_set, 'F')
    
    load_user_phone(\
        'D:\\瞿溪市监所\\信用监管\\触达率\\2025年\\公众号未激活清单 - 虚拟地址-胜泽.xlsx', \
            user_info_set, 'F')



if __name__ == '__main__':
    