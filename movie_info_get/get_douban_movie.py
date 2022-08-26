import requests
import json
from bs4 import BeautifulSoup
import re
import reportlab_setpdf

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
        #找出网页中的所有电影<ol class="grid_view">中的所有<div class="item">
        movies = soup.find('ol', 'grid_view').find_all('div', 'item')
        for movie in movies:
            movie_dict = {}
            movie_dict['em'] = movie.em.string
            #电影名称
            movie_dict['name'] = movie.a.img['alt']
            #海报地址，后续下载
            movie_dict['image_addr'] = movie.a.img['src']
            #电影详情地址链接
            movie_dict['href'] = movie.a['href']
            #获取电影名称和别名
            movie_dict['title'] = ''.join(
                [i.string for i in movie.find_all('span', 'title')])
            movie_dict['other'] = movie.find('span', 'other').string

            bd = movie.find('div', 'bd')
            #电影简介
            movie_dict['review'] = '\n'.join(bd.p.stripped_strings)
            #评价-豆瓣评分
            movie_dict['rating_num'] = bd.find('span', 'rating_num').string
            #评语
            try:
                movie_dict['quote'] = bd.find('span', 'inq').string
            except AttributeError:
                movie_dict['quote'] = ''
            mlist.append(movie_dict)
    except Exception as e:
        print('爬取失败', e)


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


get_movie_list()