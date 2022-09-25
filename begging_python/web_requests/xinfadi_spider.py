# 新发地蔬菜价格信息爬取
import requests
import pandas as pd
from bs4 import BeautifulSoup 
import json

# 获取一个response
def get_html_response(url):
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
        'user-agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        }                
        r = requests.post(url, data=pdata, headers=hd)
        r.encoding = 'utf-8'
        r.raise_for_status()
        return r
    except Exception as e:
        print('爬取失败', e)


xfdurl = 'http://www.xinfadi.com.cn/priceDetail.html'
resp1= get_html_response(xfdurl)

soup = BeautifulSoup(resp1.text)
thead = soup.select('table thead tr th')
tcolums = [i.string  for i in thead]
gp_url = 'http://www.xinfadi.com.cn/getPriceData.html'
pdata = {
            'limit': 20,
            'current': 1,
            'pubDateStartTime':'' ,
            'pubDateEndTime': '',
            'prodPcatid': '',
            'prodCatid': '',
            'prodName': '',
        }
resp2 = post_price_data(gp_url, pdata)
jj = json.loads(resp2.text)