import requests
import json
from bs4 import BeautifulSoup
import re


def get_html_content(url):
    try:
        hd = {
            'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        }
        r = requests.get(url, headers=hd)
        r.encoding = 'utf-8'
        r.raise_for_status()
        print('start parse :' + url)
        return r.text
    except Exception as e:
        print('爬取失败', e)


def bs4_parse_html(mlist, htxt):
    try:
        soup = BeautifulSoup(htxt, 'html.parser')
        # 找出网页中的所有电影<ol class="grid_view">中的所有<div class="item">
        movies = soup.find('ol', 'grid_view').find_all('div', 'item')
        for movie in movies:
            movie_dict = {}
            movie_dict['em'] = movie.em.string
            # 电影名称
            movie_dict['name'] = movie.a.img['alt']
            # 海报地址，后续下载
            movie_dict['image_addr'] = movie.a.img['src']
            # 电影详情地址链接
            movie_dict['href'] = movie.a['href']
            # 获取电影名称和别名
            movie_dict['title'] = ''.join(
                [i.string for i in movie.find_all('span', 'title')])
            movie_dict['other'] = movie.find('span', 'other').string

            bd = movie.find('div', 'bd')
            # 电影简介
            movie_dict['review'] = '\n'.join(bd.p.stripped_strings)
            # 评价-豆瓣评分
            movie_dict['rating_num'] = bd.find('span', 'rating_num').string
            # 评语
            try:
                movie_dict['quote'] = bd.find('span', 'inq').string
            except AttributeError:
                movie_dict['quote'] = ''
            mlist.append(movie_dict)
    except Exception as e:
        print('爬取失败', e)


def bs4_parse_movie_info_html(htxt):
    soup = BeautifulSoup(htxt, 'html.parser')
    cont = soup.find('div', id='content')
    minfo = {}
    minfo['top_no'] = cont.find('div', 'top250').span.string
    minfo['reviewed'] = cont.h1.span.string
    minfo['year'] = cont.h1.find('span', 'year').string
    minfo['allpic_herf'] = cont.find('div', id='mainpic').a['href']
    minfo['mainpic'] = cont.find('div', id='mainpic').img['src']
    tinfo = cont.find('div', id='info')
    minfo['info'] = get_movie_info(tinfo)
    related_info = cont.find('div', 'related-info')
    minfo['related-info'] = ''.join(related_info.h2.stripped_strings) + '\n' + '\n'.join(
        related_info.find('span', property="v:summary").string)
    minfo['celebrities'] = get_movie_celebrities(
        cont.find('div', id='celebrities'))
    minfo['related-pic'] = get_related_pic(cont.find('div', 'related-pic'))


def get_movie_info(tinfo):
    # 找出影片内容
    info = []
    span = tinfo.span
    iOneItem = True
    item_str = ''
    while span:
        if span.name == 'br':
            iOneItem = False
            info.append(item_str)
            item_str = ''

        if iOneItem:
            item_str += ''.join(span.stripped_strings)

        span = span.next_sibling
        iOneItem = True
    return info

# 获取演职员列表


def get_movie_celebrities(celebrities):
    cd = {}
    cd['title'] = celebrities.i.string
    li = []
    pat = re.compile(r'(?<=\()(.*)(?=\))')
    for cele in celebrities.find_all('li', 'celebrity'):
        title = cele.a['title']
        role = cele.find('span', 'role').string
        # 匹配（……）里的url
        url = pat.search(cele.find('div', 'avatar')['style']).group(0)
        li.append((title, role, url))
    cd['li'] = li
    return cd

# 获取电影所有图片链接


def get_related_pic(related_pic):
    title = related_pic.i.string
    pic_num = related_pic.span.find(string=re.compile('图片'))
    href = related_pic.span.find(href=re.compile('photo'))
    pic_num = href.string
    ahref = href['href']
    ahref = ahref.rstrip('all_photos')
    type_s = ('S', 'R', 'W')
    pic_url_list = []
    for s in type_s:
        url = ahref+'photos?type='+s
        pic_url_list.append(get_all_pic(url))

# 获取一个页面的所有图片链接
def get_all_pic(url):    
    htxt = get_html_content(url)
    soup = BeautifulSoup(htxt, 'html.parser')
    cont = soup.find('div', id='content')
    mdict = {}
    mdict['title'] = cont.h1.string
    # 获取图片数量
    pat = re.compile(r'(\d+)')
    pic_num = cont.find('span', 'count').string
    npic = int(pat.search(pic_num).group(0))

    #遍历所有页面里的图片，获取地址 30张 一页
    pic_id_list = []
    for i in range(npic/30+1):
        nurl = url+'&start=' + '{}'.format(i*30)
        soup = BeautifulSoup(get_html_content(nurl), 'html.parser')
        cont = soup.find('div', id='content')
        for li in cont.select('li[data-id]'):
            pic_id = li['data-id']
            pic_href = li.a['href']
            soup = BeautifulSoup(get_html_content(pic_href), 'html.parser')
            cont = soup.find('div', id='content')
            img_src = cont.img['src']
            pic_id_list.append((pic_id, img_src))
    mdict['list'] = pic_id_list


def get_movie_list():
    url = 'https://movie.douban.com/top250?start='
    n = 25
    mlist = []
    for i in range(10):
        html = get_html_content(url + str(n * i))
        bs4_parse_html(mlist, html)
    with open('movie_data.json', 'w') as file:
        json.dump(mlist, file, indent=2)
        print('success dump file :movie_data.json')
    return mlist


def get_movie_list_info(mlist):
    minfo_list = []
    for m in mlist:
        html = get_html_content(m['href'])
        minfo_list.append(bs4_parse_movie_info_html(html))
