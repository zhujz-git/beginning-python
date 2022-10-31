from selenium import webdriver
from bs4 import BeautifulSoup
import os
from time import sleep
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import re
import json


def get_item_browser():
    cookies = [
        {'domain': '.tmall.com',
         'expiry': 1682497469,
         'httpOnly': False,
         'name': 'tfstk',
         'path': '/',
         'secure': False,
         'value': 'ct4PBgv1FaQycIPdBq0U7go0elpRZkz3zEkrq92NmaUwi2oliApKiUzogxR2K0f..'},
        {'domain': 'papa.tmall.com',
         'expiry': 1698481471,
         'httpOnly': False,
         'name': 'cq',
         'path': '/',
         'secure': False,
         'value': 'ccp%3D0'},
        {'domain': '.tmall.com',
            'httpOnly': False,
            'name': 'uc1',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': 'cookie15=VT5L2FSpMGV7TQ%3D%3D&cookie21=U%2BGCWk%2F7ow08GIhZA1V8cQ%3D%3D&cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&pas=0&cookie14=UoeyCG%2B%2Fw9MSNQ%3D%3D&existShop=true'},
        {'domain': '.tmall.com',
            'httpOnly': False,
            'name': 'cancelledSubSites',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': 'empty'},
        {'domain': 'papa.tmall.com',
            'expiry': 1669537468,
            'httpOnly': False,
            'name': 'pnm_cku822',
            'path': '/',
            'secure': False,
            'value': ''},
        {'domain': '.tmall.com',
            'httpOnly': True,
            'name': 'uc4',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': 'nk4=0%40GIsuUD0zoBas8xPVPxljQ9PPdg%3D%3D&id4=0%40UO2hZtlDwmC1EgFm6P2FjTPXFq8%3D'},
        {'domain': '.tmall.com',
            'httpOnly': True,
            'name': 'sgcookie',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': 'E100d3Mg8nPU1KRh3uKItMnNYcB2njRaPgsNA4vz2%2FsNhqfYOlC%2Buqc3UIdMMg1E0KjThJaNoIBDdJADfdCUuDzhhYm6nSgghhxLYpl14Hxm%2Fmcb7FVLIR%2F7ACK9sZH%2FPcrr'},
        {'domain': '.tmall.com',
            'httpOnly': False,
            'name': 'tracknick',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': 'ylucky64'},
        {'domain': '.tmall.com',
            'httpOnly': False,
            'name': '_nk_',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': 'ylucky64'},
        {'domain': '.tmall.com',
            'httpOnly': False,
            'name': 'sg',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': '48a'},
        {'domain': '.tmall.com',
            'httpOnly': False,
            'name': '_tb_token_',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': '3473a5f3eb33'},
        {'domain': '.tmall.com',
            'httpOnly': False,
            'name': 'csg',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': 'c9d51ddc'},
        {'domain': '.tmall.com',
            'httpOnly': True,
            'name': 'cookie2',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': '95b95488d315f4a174cd5ee082de34e5'},
        {'domain': '.tmall.com',
            'expiry': 1667031655,
            'httpOnly': False,
            'name': 'xlly_s',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': '1'},
        {'domain': '.tmall.com',
            'expiry': 1682497469,
            'httpOnly': False,
            'name': 'isg',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': 'BOvrtFGDDGn4gFC93X6m-Zp5eg_VAP-Cye7IVF1o4SqB_Ate5dXv0W5WUj2SXFd6'},
        {'domain': '.tmall.com',
            'httpOnly': False,
            'name': 'unb',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': '141973468'},
        {'domain': '.tmall.com',
            'httpOnly': True,
            'name': 'uc3',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': 'id2=UoW2%2BqtUqtky&lg2=W5iHLLyFOGW7aA%3D%3D&vt3=F8dCv4oYssgWuxlaGxg%3D&nk2=Ggc99bDLhrQ%3D'},
        {'domain': '.tmall.com',
            'httpOnly': True,
            'name': 'cookie17',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': 'UoW2%2BqtUqtky'},
        {'domain': '.tmall.com',
            'httpOnly': False,
            'name': '_l_g_',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': 'Ug%3D%3D'},
        {'domain': '.tmall.com',
            'httpOnly': False,
            'name': 't',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': '2242100bcfa08de93eaa5384eb6dc682'},
        {'domain': '.tmall.com',
            'expiry': 1698510268,
            'httpOnly': False,
            'name': 'lid',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': 'ylucky64'},
        {'domain': '.tmall.com',
            'httpOnly': False,
            'name': 'login',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': 'true'},
        {'domain': '.tmall.com',
            'httpOnly': False,
            'name': 'dnk',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': 'ylucky64'},
        {'domain': '.tmall.com',
            'expiry': 1682497469,
            'httpOnly': False,
            'name': 'l',
            'path': '/',
            'secure': False,
            'value': 'eBPqYQqRTuZ-EDvSBOfwhurza77tdIRAguPzaNbMiOCP9TCw5WD5W6yM_5TeCnGchsZeR3AIrDUWBeYBqCDXrVms9qWT9WHmn'},
        {'domain': '.tmall.com',
            'httpOnly': False,
            'name': 'lgc',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': 'ylucky64'},
        {'domain': '.tmall.com',
            'httpOnly': True,
            'name': 'cookie1',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': 'W8HY4jZX0v8S6Y1LD1t%2FyYGF%2BgdPhVUTvA0PHjXmT4o%3D'},
        {'domain': '.tmall.com',
            'expiry': 1701505254,
            'httpOnly': False,
            'name': 'cna',
            'path': '/',
            'sameSite': 'None',
            'secure': True,
            'value': '7X7iG6hBfkUCAX1u4JD8ZSdn'}]
    # https://python3webspider.cuiqingcai.com/7.4-shi-yong-selenium-pa-qu-tao-bao-shang-pin
    # https://selenium-python.readthedocs.io/api.html#module-selenium.common.exceptions
    browser = webdriver.Edge(executable_path='msedgedriver.exe')
    browser.maximize_window()
    browser.get('https://papa.tmall.com')

    for item in cookies:
        browser.add_cookie(item)

    return browser


# 设置统一的请求头
def get_html_head():
    hd = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Cookie':
        'gr_user_id=06b268dc-f2af-472f-8d75-95dc7c0863c3; __utmv=30149280.4252; douban-fav-remind=1; bid=-rbqx6M9uZ8; __gads=ID=e60f97d8cddcc79d-2242122ac2d500e1:T=1661320700:RT=1661320700:S=ALNI_MbzwyBCrDyDaOaPn9lMF4au9Nn_2Q; ll="118174"; __utmc=30149280; dbcl2="42521702:5nS0bXkYJr0"; ck=pllS; frodotk="54a1ce10192d170cfde56a304b874524"; __utma=30149280.470231712.1617176844.1661836107.1661911542.30; __utmb=30149280.0.10.1661911542; __utmz=30149280.1661911542.30.5.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; __gpi=UID=000008fa6e8a48e4:T=1661320700:RT=1661911542:S=ALNI_MZrbfTwN0pFnmvL3ivykafmoE3P4w; push_noty_num=0; push_doumail_num=0',
    }
    return hd


# 获取一个response
def get_html_response(url):
    try:
        hd = get_html_head()
        # 增加爬虫安全性 一秒钟访问一次
        sleep(1)
        r = requests.get(url, headers=hd)
        r.raise_for_status()
        return r
    except Exception as e:
        print('爬取失败', e)


def down_web_image(url, root, filename):
    try:
        if url[:6] != 'https:' :
            url = 'https:' + url
        path = root + filename
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            r = get_html_response(url)
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
                #print('success download image:{}, filename:{}'.format(url, path))
                return path
        else:
            print('image is alread exist:{}'.format(path))
            return path
    except Exception as e:
        print('爬取失败', e)

#下载页面中的所有宝贝图片
def down_page_item_img(browser, page_no):
    search_url = 'https://papa.tmall.com/category.htm?search=y&orderType=newOn_desc&pageNo='
    browser.get(search_url + str(page_no))

    # 打开网页后上下刷新几次
    for i in range(10):
        browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        sleep(1)

    for i in range(10):
        browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP)
        sleep(1)

    html = browser.page_source
    bs = BeautifulSoup(html, 'html.parser')
    url_list = []
    img_root = './image/'

    restored_item_list = get_restored_item(img_root)
    # 找出所有页面链接
    for item in bs.find_all('dd', 'detail'):
        if is_restored(restored_item_list, item.a.string.rstrip()):
            print(item.a.string + '已经下载过，跳过，要重新下载请删除文件夹')
            continue
        url_list.append(item.a['href'])
        

    for n, url in enumerate(url_list, start=1):
        print('开始下载第{}个宝贝，总数：{}'.format(n, len(url_list)))
        down_item_img(browser, url, img_root, restored_item_list) 

# 遍历已经下载的文件夹
def get_restored_item(dir):
    return list(os.walk(dir))[0][1]

def is_restored(ilist, item):
    for i in ilist:
        if item in i:
            return True
    return False

# 单独下载一个页面
def down_item_img(browser, url, img_root, restored_item_list):
        if url[:6] != 'https:' :
            url = 'https:' + url
        # 打开网页后拉倒最底下
        browser.get(url)
        html = browser.page_source
        bs = BeautifulSoup(html, 'html.parser')
        # 拼出文件夹名字
        main_title = bs.find(class_=re.compile('ItemHeader--mainTitle')).string
        # 判断是否已经下载了
        if is_restored(restored_item_list, main_title):
            print(main_title + '已经下载过，跳过，要重新下载请删除文件夹')
            return 

        sleep(5)
        for i in range(30):
            browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            sleep(1)

        # 开始分析网页
        html = browser.page_source
        bs = BeautifulSoup(html, 'html.parser')
        try:
            origin_price = bs.find(class_=re.compile(
                'Price--originPrice')).find(class_=re.compile('Price--priceText')).string
        except AttributeError:
            origin_price = ''
            
        try:
            extra_price = bs.find(class_=re.compile(
                'Price--extraPrice')).find(class_=re.compile('Price--priceText')).string
        except AttributeError:
            extra_price = origin_price
        dir_name = main_title + '-'  + origin_price + '-' + extra_price + '/'
        item_dir = img_root + dir_name

        #主图
        main_pics = bs.find(class_=re.compile(
            'PicGallery--thumbnails')).find_all('li')
        for n, main_pic in enumerate(main_pics, 1):
            img_src = main_pic.img['src']
            img_url = img_src.partition('jpg')[0]+'jpg'
            down_web_image(img_url, item_dir, '主图{}.jpg'.format(n))

        #向上翻10次 尽量显示全
        for i in range(30):
            browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP)
            sleep(1)

        html = browser.page_source
        bs = BeautifulSoup(html, 'html.parser')
        #详情页第一种
        n = 1
        for image in bs.find_all('div', 'descV8-singleImage'):            
            img_url = image.img['src']
            if img_url.find('getAvatar=avatar') > 0:
                continue
            down_web_image(img_url, item_dir, '详情{}.jpg'.format(n))
            n += 1

        #详情页第二种
        richtext = bs.find('div', 'descV8-richtext')
        n = 1
        if richtext:
            for image in richtext.select('div > img.lazyload'):
                img_url = image['src']
                if img_url.find('getAvatar=avatar') > 0:
                    continue
                if img_url[-4:]== '.gif':
                    continue
                down_web_image(img_url, item_dir, '详情{}.jpg'.format(n))
                n += 1

        #详情页第3种
        n = 1
        for img in bs.find_all('img', 'descV6-mobile-image lazyload'):            
            img_url = img['src']
            if img_url.find('getAvatar=avatar') > 0:
                continue
            down_web_image(img_url, item_dir, '详情{}.jpg'.format(n))
            n += 1

if __name__ == '__main__':
    browser = get_item_browser()
    for i in range(4,26):
        down_page_item_img(browser, i)