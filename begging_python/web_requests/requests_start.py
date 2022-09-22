import requests
import os
from bs4 import BeautifulSoup
import re


def get_search_kw(url, keyvalue):
    try:
        r = requests.get(url, keyvalue)
        print(r.request.url)
        r.raise_for_status()
        print(len(r.text))
    except Exception as e:
        print('爬取失败', e)


def get_html_response(url):
    try:
        hd = {
            'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'cookie':
            't=6f3b1218569a3d352134d565298a1a2e; enc=o6Gnp9%2Fu%2BlX110a8%2F5G8apB%2FC2B1mjLWCRCW2J5Y%2FZx1py8iaFFo2x5DSLip8dAK2ROTPKryEK3bSXJBSXxxiA%3D%3D; cna=Cb/qGKFYJXgCATy+YA6OCoT/; miid=703435975575142564; sgcookie=E100ome5ntgtW%2F7RbhUApz%2BifaE9pBo27chPdXzoOIyVBe9c1NQlO2eo0jbi81csoNh%2FM57zHA3pxamueMHsThri5DpIMr4iGR%2FxuTJXnEOIF629DJShD0FX13lOFJMPhWUt; tracknick=ylucky64; _cc_=WqG3DMC9EA%3D%3D; thw=cn; mt=ci=-1_0; uc1=cookie14=UoexOzqjKoPz%2Bw%3D%3D; cookie2=102378a039befe611a4f7ff43ec93781; _tb_token_=ebb3e8e83beee; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; _m_h5_tk=a50aaecab377fd7818523f7dd376927f_1660115613937; _m_h5_tk_enc=0d7eaca75480543ad4c6d03b66f8a08c; xlly_s=1; JSESSIONID=6ED846FB08ACE9683D8E71836411CA1E; tfstk=cV1CBFqVaDmCyer6bpaaUzy62EdPZvcB7vtdRlfVXFRZnF_CihG2cfd6Ecx1FF1..; l=eBxcgu1lLeemdA_BBOfZourza779jIRAguPzaNbMiOCP_71Hv-vPW6YDOOTMCnGAh6EyR37vCcawBeYBqIccSQLy2j-la_Mmn; isg=BC8v8emikVUzTJbTAZYJtk-avkM51IP20EGBs0G8yB79kE-SSac_R1ZCFoKu6Ftu'
        }
        r = requests.get(url, headers=hd)
        r.encoding = r.apparent_encoding
        r.raise_for_status()
        return r
    except Exception as e:
        print('爬取失败', e)


def get_html_content(url):
    try:
        hd = {
            'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'cookie':'t=6f3b1218569a3d352134d565298a1a2e; enc=o6Gnp9%2Fu%2BlX110a8%2F5G8apB%2FC2B1mjLWCRCW2J5Y%2FZx1py8iaFFo2x5DSLip8dAK2ROTPKryEK3bSXJBSXxxiA%3D%3D; cna=Cb/qGKFYJXgCATy+YA6OCoT/; miid=703435975575142564; sgcookie=E100ome5ntgtW%2F7RbhUApz%2BifaE9pBo27chPdXzoOIyVBe9c1NQlO2eo0jbi81csoNh%2FM57zHA3pxamueMHsThri5DpIMr4iGR%2FxuTJXnEOIF629DJShD0FX13lOFJMPhWUt; tracknick=ylucky64; _cc_=WqG3DMC9EA%3D%3D; thw=cn; mt=ci=-1_0; uc1=cookie14=UoexOzqjKoPz%2Bw%3D%3D; cookie2=102378a039befe611a4f7ff43ec93781; _tb_token_=ebb3e8e83beee; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; _m_h5_tk=a50aaecab377fd7818523f7dd376927f_1660115613937; _m_h5_tk_enc=0d7eaca75480543ad4c6d03b66f8a08c; xlly_s=1; JSESSIONID=6ED846FB08ACE9683D8E71836411CA1E; tfstk=cV1CBFqVaDmCyer6bpaaUzy62EdPZvcB7vtdRlfVXFRZnF_CihG2cfd6Ecx1FF1..; l=eBxcgu1lLeemdA_BBOfZourza779jIRAguPzaNbMiOCP_71Hv-vPW6YDOOTMCnGAh6EyR37vCcawBeYBqIccSQLy2j-la_Mmn; isg=BC8v8emikVUzTJbTAZYJtk-avkM51IP20EGBs0G8yB79kE-SSac_R1ZCFoKu6Ftu'
        }
        r = requests.get(url, headers=hd)
        r.encoding = r.apparent_encoding
        r.raise_for_status()
        return r.text
    except Exception as e:
        print('爬取失败', e)


def test_keyword():
    keyword = '一树梨花压海棠'
    url = 'https://cn.bing.com/search'
    keyvalue = {'q': keyword}
    get_search_kw(url, keyvalue)

    url = 'https://www.baidu.com/s'
    keyvalue = {'wd': keyword}
    get_search_kw(url, keyvalue)

    url = 'https://www.so.com/s'
    keyvalue = {'q': keyword}
    get_search_kw(url, keyvalue)


def down_web_image(url, root):
    try:
        path = root + url.split('/')[-1]
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            r = get_html_response(url)
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
                print('文件保存成功', path)
        else:
            print('文件已存在', path)
    except Exception as e:
        print('爬取失败', e)


def test_down_web_image():
    url = 'https://i.natgeofe.com/n/848510a5-e914-4a20-9327-65c742c80a8d/frank-drake-universe.jpg'
    root = 'image//'
    down_web_image(url, root)   


def bs4_parse_html(ulist, htxt):
    soup = BeautifulSoup(htxt, 'html.parser')
    trs = soup.find('tbody').find_all('tr')
    for tr in trs:
        tds = tr('td')
        ranking = tr.find('div', 'ranking').string.strip()
        uniname = tr.find('a', 'name-cn').string.strip()
        ulist.append((ranking, uniname, tds[4].string.strip()))


def print_uni_list():
    url = 'https://www.shanghairanking.cn/rankings/bcur/2022'
    ulist = []
    bs4_parse_html(ulist, get_html_content(url))

    tplt = '{0:^10}\t{1:{3}^10}\t{2:^10}'
    print(tplt.format('排名', '学校名称', '总分',chr(12288)))
    for u in ulist:
        print(tplt.format(u[0], u[1], u[2], chr(12288)))


def parse_taobao_page(ulist, html_text):
    try:
        plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html_text)
        tlt = re.findall(r'\"raw_title\"\:\".*?\"', html_text)
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            ulist.append((price, title))
    except Exception as e:
        print('parse_taobao_page error:', e)

def print_taobao_list():
    goods = '零食'
    depth = 2
    start_url = 'https://s.taobao.com/search?q=' + goods
    info_list = []
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(44*i)
            html = get_html_content(url)
            parse_taobao_page(info_list, html)
        except Exception as e:
            print('print_taobao_list func error:', e)
            continue

    tplt = '{:4}\t{:^8}\t{:^16}'
    print(tplt.format('序号', '价格', '商品名称'))
    count = 0
    for u in info_list:
        count += 1
        print(tplt.format(count, u[0], u[1]))


print_taobao_list()
