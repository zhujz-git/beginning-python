# 新发地蔬菜价格信息爬取
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import datetime


def get_html_response(url):
    # 获取一个response
    try:
        hd = {
            'user-agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ,
        }
        r = requests.get(url, headers=hd)
        r.encoding = 'utf-8'
        r.raise_for_status()
        return r
    except Exception as e:
        print('爬取失败', e)


# 发送查询请求
def post_price_data(url, pdata):
    try:
        hd = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '85',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.xinfadi.com.cn',
            'Origin': 'http://www.xinfadi.com.cn',
            'Referer': 'http://www.xinfadi.com.cn/priceDetail.html',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/86.0.4240.198 Safari/537.36'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ,
            'X-Requested-With': 'XMLHttpRequest',
        }
        r = requests.post(url, data=pdata, headers=hd)
        r.encoding = 'utf-8'
        r.raise_for_status()
        return r
    except Exception as e:
        print('爬取失败', e)


# 从本地读入原来已导入的数据
try:
    xinfadi_pd = pd.read_pickle('xinfadi.pkl')
except Exception as e:
    print(e)
    # 从主页查询列名
    xfdurl = 'http://www.xinfadi.com.cn/priceDetail.html'
    resp1 = get_html_response(xfdurl)

    soup = BeautifulSoup(resp1.text, 'html.parser')
    thead = soup.select('table thead tr th')
    tcolums = [i.string for i in thead]
    xinfadi_pd = pd.DataFrame(columns=tcolums)
    xinfadi_pd.set_index(tcolums[-1], inplace=True)
    # index设置为日期类型
    xinfadi_pd.index = pd.to_datetime(xinfadi_pd.index)

# 查询缺失数据的时间间隔
start_time = datetime.date(2020, 1, 1) if pd.isna(
    xinfadi_pd.index.max()) else xinfadi_pd.index.max()
end_time = datetime.date.today()

# 然后查询总数
gp_url = 'http://www.xinfadi.com.cn/getPriceData.html'
pdata = {
    'limit': 20,
    'current': 1,
    'pubDateStartTime': start_time.strftime('%Y/%m/%d'),
    'pubDateEndTime': end_time.strftime('%Y/%m/%d'),
    'prodPcatid': '',
    'prodCatid': '',
    'prodName': '',
}
get_price_r = post_price_data(gp_url, pdata)
json_prod = json.loads(get_price_r.text)
count = json_prod['count']

server_colums = [
    'prodCat', 'prodPcat', 'prodName', 'lowPrice', 'highPrice', 'avgPrice',
    'specInfo', 'place', 'unitInfo', 'pubDate'
]
limit = min(1000, count)

# 将所有数据查询出来
current = 1
pd_list = []
pdata['limit'] = limit
while (count > 0):
    pdata['current'] = current
    get_price_r = post_price_data(gp_url, pdata)
    json_prod = json.loads(get_price_r.text)
    print('get price data:', json_prod['current'], json_prod['limit'],
          json_prod['count'])
    pd_list.append(pd.DataFrame(json_prod['list']))

    count -= limit
    current += 1

# 将所有数据合并
prod_pd = pd.concat(pd_list)[server_colums]

# 设置发布日期为index
index_name = xinfadi_pd.index.name
new_columns = xinfadi_pd.columns.to_list()
new_columns.append(index_name)
prod_pd.columns = new_columns
prod_pd.set_index(index_name, inplace=True)

# index设置为日期类型
prod_pd.index = pd.to_datetime(prod_pd.index)

# 将新查询的跟保存的数据合并后保存到文件
xinfadi_pd = pd.concat([xinfadi_pd, prod_pd])
xinfadi_pd = xinfadi_pd.reset_index().drop_duplicates().set_index(index_name)
xinfadi_pd.to_pickle('xinfadi.pkl')


