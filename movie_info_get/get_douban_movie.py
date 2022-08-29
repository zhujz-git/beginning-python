import requests
import json
from bs4 import BeautifulSoup
import re
import reportlab_setpdf
from pyquery import PyQuery as pq


# 设置统一的请求头
def get_html_head():
    hd = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Cookie':
        'douban-fav-remind=1; __utmv=30149280.4252; _ga=GA1.2.938565153.1593217773; _vwo_uuid_v2=DECC280D16CD4F57D701F745CD09857EB|2ff5b3f490ddf1585331fd3d0106680f; viewed="34993976"; gr_user_id=1eadc6be-b669-4f11-bca2-f7e16df6d8a9; __utmz=30149280.1649128375.67.9.utmcsr=m.ashvs1.cn|utmccn=(referral)|utmcmd=referral|utmcct=/2022/03/30/%e6%9c%88%e7%90%83%e9%99%a8%e8%90%bd-moonfall-2022/; ll="118174"; bid=nxozWDMC7Qg; __gads=ID=57d76279b9b07603-222d96b336d500a5:T=1657941077:RT=1657941077:S=ALNI_MbrRyQcNOZy-MxAqDaMixWDFAQsGA; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1659870774; __yadk_uid=ZNrRh8jdz6CcZtyYRj8tH2ldNNozmQgE; __utma=30149280.938565153.1593217773.1661523221.1661696315.78; __utmc=30149280; __utmb=30149280.1.10.1661696315; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1661696316%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.1464621297.1593217783.1661523222.1661696316.54; __utmb=223695111.0.10.1661696316; __utmc=223695111; __utmz=223695111.1661696316.54.45.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ap_v=0,6.0; __gpi=UID=0000047e5f873424:T=1649128399:RT=1661696386:S=ALNI_MayEAtdGdCJ8WvE4kW2l0PJKsWosA; _pk_id.100001.4cf6=902fb43b894f66e1.1593217783.54.1661697537.1661523236.',
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
        r = requests.get(url, headers=hd)
        r.encoding = 'utf-8'
        r.raise_for_status()
        print('start parse :' + url)
        return r
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
        reviews = get_html_soup(reviews_url).select('div[data-cid]')
        for review in reviews:
            cid = review['data-cid']
            rname = review.find('a', 'name').string
            rtime = review.find('span', 'main-meta').string
            review_url = 'https://movie.douban.com/j/review/' + cid + '/full'
            resp = get_html_response(review_url)
            re_text = pq(resp.json().get('html')).text()
            rlist.append((cid, rname, rtime, re_text))
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
    minfo_list = []
    for m in mlist:
        minfo_list.append(bs4_parse_movie_info(m))


if __name__ == '__main__':
    mlist = reportlab_setpdf.lead_json('./json/movie_data.json')
    m = bs4_parse_movie_info(mlist[0])
    reportlab_setpdf.dump_data('./json/{}.json'.format(m['reviewed']), m)
