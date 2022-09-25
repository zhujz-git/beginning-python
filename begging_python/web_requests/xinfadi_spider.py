# 新发地蔬菜价格信息爬取
from operator import truediv
from time import sleep
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json


def get_html_response(url):
    # 获取一个response
    try:
        hd = {
            'user-agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        r = requests.post(url, data=pdata, headers=hd)
        r.encoding = 'utf-8'
        r.raise_for_status()
        return r
    except Exception as e:
        print('爬取失败', e)


xfdurl = 'http://www.xinfadi.com.cn/priceDetail.html'
resp1 = get_html_response(xfdurl)

soup = BeautifulSoup(resp1.text, 'html.parser')
thead = soup.select('table thead tr th')
tcolums = [i.string for i in thead]
gp_url = 'http://www.xinfadi.com.cn/getPriceData.html'
pdata = {
    'limit': 20,
    'current': 1,
    'pubDateStartTime': '',
    'pubDateEndTime': '',
    'prodPcatid': '',
    'prodCatid': '',
    'prodName': '阳光玫瑰',
}
get_price_r = post_price_data(gp_url, pdata)
json_prod = json.loads(get_price_r.text)
count = json_prod['count']

server_colums = ['prodCat', 'prodPcat', 'prodName', 'lowPrice', 'highPrice', 'avgPrice', 'specInfo',  'place', 'unitInfo', 'pubDate']
#prod_pd = pd.DataFrame(json_prod['list'])[server_colums]


#count = 20000
limit = min(1000, count)

current = 1 
pd_list = []
pdata['limit'] = limit
while(True):
    pdata['current'] = current
    get_price_r = post_price_data(gp_url, pdata)
    json_prod = json.loads(get_price_r.text)
    pd_list.append(pd.DataFrame(json_prod['list']))
    if (current * limit)  > count:
        break
    current += 1 
    

prod_pd = pd.concat(pd_list)[server_colums]
prod_pd.columns = tcolums
