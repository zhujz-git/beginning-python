from nntplib import NNTP, decode_header
from urllib.request import urlopen
import textwrap
import re


class NewsAgent:
    """
    可将新闻源中的新闻分发到新闻目的地的对象
    """
    def __init__(self) -> None:
        self.sources = []
        self.destinations = []

    def add_source(self, source):
        self.sources.append(source)

    def addDestination(self, dest):
        self.destinations.append(dest)

    def distribute(self):
        """
        从所有新闻源获取所有的新闻，再将其分发到所有的新闻目的地
        """
        items = []
        for source in self.sources:
            items.extend(source.get_items())
        for dest in self.destinations:
            dest.receive_items(items)


class NewsItem:
    """
    由标题和正文组成的简单新闻
    """
    def __init__(self, title, body) -> None:
        self.title = title
        self.body = body


class NNTPSource:
    """
    从NNTP新闻组获取新闻的新闻源
    """
    def __init__(self, servername, group, howmany) -> None:
        self.servername = servername
        self.group = group
        self.howmany = howmany

    def get_items(self):
        server = NNTP(self.servername)
        resp, count, first, last, name = server.group(self.group)
        start = last - self.howmany + 1
        resp, overviews = server.over((start, last))
        for id, over in overviews:
            title = decode_header(over['subject'])
            resp, info = server.body(id)
            body = '\n'.join(line.decode('latin')
                             for line in info.lines) + '\n\n'
            yield NewsItem(title, body)
        server.quit()


class SimpleWebSource:
    """
    使用正则表达式从网页提取新闻的新闻源
    """
    def __init__(self,
                 url,
                 title_pattern,
                 body_pattern,
                 encoding='utf8') -> None:
        self.url = url
        self.title_pattern = re.compile(title_pattern)
        self.body_pattern = re.compile(body_pattern)
        self.encoding = encoding

    def get_items(self):
        text = urlopen(self.url).read().decode(self.encoding)
        titles = self.title_pattern.findall(text)
        bodies = self.body_pattern.findall(text)
        print(titles, bodies)
        for title, body in zip(titles, bodies):
            yield NewsItem(title, textwrap.fill(body) + '\n')


class PlaiDestination:
    """
    以纯文本方式显示所有新闻的新闻目的地
    """
    def receive_items(self, items):
        for item in items:
            print(item.title)
            print('-' * len(item.title))
            print(item.body)


class HTMLDestination:
    """
    以HTML格式显示所有新闻的新闻目的地
    """
    def __init__(self, filename) -> None:
        self.filename = filename

    def receive_items(self, items):
        out = open(self.filename, 'w')
        print("""
        <html>
          <head>
            <title>Today's News</title>
          </head>
          <body>
          <h1>Today's News<h1>
          """,
              file=out)

        print('<ul>', file=out)
        id = 0
        for item in items:
            id += 1
            print('<li><a href="#{}">{}</a></li>'.format(id, item.title),
                  file=out)
        print('</ul>', file=out)

        id = 0
        for item in items:
            id += 1
            print('<h2><a name="{}" href="{}">{}</a></h2>'.format(id, item.title, item.body),
                  file=out)
            print('<pre>{}</pre>'.format(item.body), file=out)

        print("""
        </body>
          </html>
          """, file=out)


def runDefaultSetup():
    """
    默认的新闻源和目的地设置，请根据偏好修改
    """

    agent = NewsAgent()

    #从cnbata获取新闻的对象
    reuters_url = 'https://www.cnbeta.com/'
    reuter_title = r'<a class="link" href="(.*?)"\s*\S*"></a>'
    reuter_body = r'<h3 class="figure-title">(.*?)</h3>'

    reuters = SimpleWebSource(reuters_url, reuter_title, reuter_body)
    agent.add_source(reuters)
    #从 获取新闻的NNTPSource对象
    clpa_server = 'news.mixmin.net'
    clpa_group = 'rocksolid.nodes.announce'
    clpa_howmany = 10
    clpa = NNTPSource(clpa_server, clpa_group, clpa_howmany)

    agent.add_source(clpa)

    agent.addDestination(PlaiDestination())
    agent.addDestination(HTMLDestination('news.html'))

    agent.distribute()


runDefaultSetup()