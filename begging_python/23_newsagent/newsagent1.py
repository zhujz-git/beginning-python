from nntplib import NNTP, decode_header

servername = 'news.mixmin.net'
group = 'rocksolid.nodes.announce'
server = NNTP(servername)
howmany = 10
#print(server.list())
resp, count, first, last, name = server.group(group)

strat = last - howmany + 1
#print('Group', name, 'has', count, 'articles, range', first, 'to', last)
resp, overviews = server.over((strat, last))
for id, over in overviews:
    subject = over['subject']
    resp, info = server.body(id)
    print(subject)
    print('-' * len(subject))
    for line in info.lines:
        print(line.decode('latin1'))
    print()
server.quit()