from base64 import encode
from time import sleep
import requests
import json
from bs4 import BeautifulSoup
import re
import reportlab_setpdf
from pyquery import PyQuery as pq
import os
import logging


# 设置统一的请求头
def get_html_head():
    hd = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Cookie':
        'gr_user_id=06b268dc-f2af-472f-8d75-95dc7c0863c3; __utmv=30149280.4252; douban-fav-remind=1; bid=-rbqx6M9uZ8; __gads=ID=e60f97d8cddcc79d-2242122ac2d500e1:T=1661320700:RT=1661320700:S=ALNI_MbzwyBCrDyDaOaPn9lMF4au9Nn_2Q; ll="118174"; __utmc=30149280; dbcl2="42521702:5nS0bXkYJr0"; ck=pllS; frodotk="54a1ce10192d170cfde56a304b874524"; __utma=30149280.470231712.1617176844.1661836107.1661911542.30; __utmb=30149280.0.10.1661911542; __utmz=30149280.1661911542.30.5.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; __gpi=UID=000008fa6e8a48e4:T=1661320700:RT=1661911542:S=ALNI_MZrbfTwN0pFnmvL3ivykafmoE3P4w; push_noty_num=0; push_doumail_num=0',
    }
    return hd


# bs4分析下
def get_html_soup(url):
    try:
        return BeautifulSoup(get_html_text(url), 'html.parser')
    except Exception as e:
        print(e)


# 获取网页文本
def get_html_text(url):
    return get_html_response(url).text


# 获取一个response
def get_html_response(url):
    try:
        hd = get_html_head()
        # 增加爬虫安全性 一秒钟访问一次
        sleep(1)
        r = requests.get(url, headers=hd)
        r.encoding = 'utf-8'
        r.raise_for_status()
        logging.info('start parse :' + url)
        return r
    except Exception as e:
        print('爬取失败', e)

# 下载图片文件
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
                return path
        else:
            print('文件已存在', path)
            return path
    except Exception as e:
        print('爬取失败', e)

# 分析top250列表
def bs4_parse_topmlist(mlist, soup):
    try:
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
            movie_dict['id'] = movie_dict['href'].split('/')[-2]
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


# 获取一个电影页面的所有信息 保存到一个字典
def bs4_parse_movie_info(movie_info):
    soup = get_html_soup(movie_info['href'])
    cont = soup.find('div', id='content')
    minfo = {}
    minfo['id'] = movie_info['href'].split('/')[-2]
    # 250名次
    minfo['top_no'] = cont.find('div', 'top250').span.string
    # 电影名称
    minfo['reviewed'] = cont.h1.span.string
    # 年份
    minfo['year'] = cont.h1.find('span', 'year').string
    # 电影主图
    minfo['allpic_herf'] = cont.find('div', id='mainpic').a['href']
    minfo['mainpic'] = cont.find('div', id='mainpic').img['src']
    # 电影的主要信息
    tinfo = cont.find('div', id='info')
    minfo['info'] = get_movie_info(tinfo)
    # 剧情简介
    related_info = cont.find('div', 'related-info')
    minfo['related-info'] = ''.join(
        related_info.h2.stripped_strings) + '\n' + '\n'.join(
            related_info.find('span', property="v:summary").stripped_strings)
    # 演职员表
    minfo['celebrities'] = get_movie_celebrities(
        cont.find('div', id='celebrities'))
    # 电影图片
    minfo['related-pic'] = get_related_pic(cont.find('div', 'related-pic'))
    # 短评
    minfo['comments'] = get_comments(cont.find('div', id='comments-section'))
    # 影评
    minfo['reviews'] = get_reviews(movie_info['href'])
    return minfo


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
            try:
                item_str += ''.join(span.stripped_strings)
            except AttributeError:
                item_str += span.string

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
    href = related_pic.span.find(href=re.compile('photo'))
    ahref = href['href']
    ahref = ahref.rstrip('all_photos')
    type_s = ('S', 'R', 'W')
    pic_url_list = []
    for s in type_s:
        url = ahref + 'photos?type=' + s
        pic_url_list.append(get_all_pic(url))
    return pic_url_list


# 获取一个页面的所有图片链接
def get_all_pic(url):
    soup = get_html_soup(url)
    cont = soup.find('div', id='content')
    mdict = {}
    mdict['title'] = cont.h1.string
    # 获取图片数量
    pat = re.compile(r'(\d+)')
    npic = 0
    if cont.find('span', 'count'):
        pic_num = cont.find('span', 'count').string
        npic = int(pat.search(pic_num).group(0))

    # 遍历所有页面里的图片，获取地址 30张 一页
    pic_id_list = []
    for i in range(int(npic / 30) + 1):
        nurl = url + '&start=' + '{}'.format(i * 30)
        soup = get_html_soup(nurl)
        cont = soup.find('div', id='content')
        for li in cont.select('li[data-id]'):
            pic_id = li['data-id']
            img_src = li.img['src']
            '''打开每个网页太慢了。改进下。先放缩略图，要大图的后续改进
            soup = get_html_soup(pic_href)
            cont = soup.find('div', id='content')
            img_src = cont.img['src']
            '''
            pic_id_list.append((pic_id, img_src))
    mdict['list'] = pic_id_list
    return mdict


# 获取所有短评
def get_comments(comments):
    mod = comments.find('div', 'mod-hd')
    com_dict = {}
    com_dict['title'] = mod.h2.i.string
    mod = mod.find('span', 'pl')
    href = mod.a['href']
    pat = re.compile(r'(\d+)')
    comments_num = int(pat.search(mod.a.string).group(0))
    limit = 50
    #最大只爬10页短评 不然太慢
    com_list = []
    n = min(int(comments_num / 200), 10)
    for i in range(n):
        url = href + '&start={}'.format(
            i * limit) + '&limit={}'.format(limit) + '&sort=new_score'
        coms = get_html_soup(url).find_all('div', 'comment-item')
        for com in coms:
            com_list.append((com.a['title'], com.find('span', 'short').string))
    com_dict['list'] = com_list
    return com_dict


# 获取所有影评
def get_reviews(url):
    reviews_url = url + 'reviews'
    rlist = []
    #爬取10页
    for i in range(1):
        reviews_url = url + 'reviews?start={}'.format(i * 20)
        soup = get_html_soup(reviews_url)
        if (soup):
            try:
                reviews = soup.select('div[data-cid]')
                for review in reviews:
                    cid = review['data-cid']
                    rname = review.find('a', 'name').string
                    rtime = review.find('span', 'main-meta').string
                    review_url = 'https://movie.douban.com/j/review/' + cid + '/full'
                    resp = get_html_response(review_url)
                    re_text = pq(resp.json().get('html')).text()
                    rlist.append((cid, rname, rtime, re_text))
            except Exception as e:
                print(e)
                continue

    return rlist


# 活动top250的电影列表
def get_movie_list():
    url = 'https://movie.douban.com/top250?start='
    n = 25
    mlist = []
    for i in range(10):
        soup = get_html_soup(url + str(n * i))
        bs4_parse_topmlist(mlist, soup)
    reportlab_setpdf.dump_data('./json/movie_data.json', mlist)
    return mlist


# 遍历电影列表中的所有电影，获取详细信息
def get_movie_list_info(mlist):
    id_list = get_restored_movie('./json')
    for i in mlist:
        # 已经获取的跳过
        if i['id'] not in id_list:
            try:
                m = bs4_parse_movie_info(i)
                logging.info('success get the movie:' + m['reviewed'])
                reportlab_setpdf.dump_data('./json/{}.json'.format(m['id']), m)
            except Exception as e:
                print(e)
                continue


# 遍历json文件夹 导入已遍历的电影id
def get_restored_movie(dir):
    pat = re.compile('(\d+)\.json')
    id_list = [
        n.split('.')[0] for n in list(os.walk(dir))[0][2] if pat.match(n)
    ]
    return id_list


if __name__ == '__main__':
    mlist = get_movie_list()
    #直接获取或者从json文件里读取
    #mlist = reportlab_setpdf.lead_json('./json/movie_data.json')
    handler = [
        logging.FileHandler(filename='./log/movie.log', encoding='utf-8')
    ]
    logging.basicConfig(handlers=handler, level=logging.INFO)

    get_movie_list_info(mlist)
