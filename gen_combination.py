import re
import sys


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


# 实用命令行指定组合文件路径
filepath = sys.argv[1]
comb_data = read_comb_list(filepath)
print(comb_data)
