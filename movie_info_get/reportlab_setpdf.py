from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics, ttfonts
import json
from reportlab.lib import colors


def setpdf(mlist):
    simfang_path = './font/simfang.ttf'
    simfang_font = ttfonts.TTFont(name='simfang', filename=simfang_path)
    pdfmetrics.registerFont(font=simfang_font)
    cav = canvas.Canvas('./pdf/doubanmovie250.pdf')
    cav.setFont(psfontname='simfang', size=20, leading=1)
    #页面高度
    page_y = 841.89 - 40
    #文字起始位置
    x_l = 50
    x_r = 545
    page_width = 595.27
    cav.setFillColor(colors.blue)
    cav.drawString(x_l, page_y, '豆瓣电影 Top 250')
    #图像宽 高
    img_width = 54
    img_height = 80
    #设置虚线格式
    cav.setDash(2, 1)
    i = 0
    for mdict in mlist:
        #7项一页
        offset = i % 7
        #虚线
        cav.setFillColor(colors.black)
        cav.line(x_l, page_y - 30 - offset*100, x_r, page_y - 30 - offset*100)
        cav.setFont(psfontname='simfang', size=10, leading=1)
        #序号+电影图片
        cav.setFillColor(colors.darkgray)
        cav.drawString(x_l, page_y - 45 - offset*100, mdict['em'])
        imgulr = mdict['image_addr']
        cav.drawImage(imgulr, x_l + 15, page_y - 45 - img_height + 10 - offset*100, img_width, img_height, 'auto')
        #电影介绍
        textobj = cav.beginText(130, page_y - 45 - offset*100, (80, 400))
        textobj.setFont(psfontname='simfang', size=12, leading=15)
        textobj.setFillColor(colors.ReportLabBlue)
        textobj.textLines(mdict['title'])
        textobj.textLines(mdict['other'])
        textobj.setFillColor(colors.black)
        textobj.setFont(psfontname='simfang', size=10, leading=12)        
        textobj.textLines(mdict['review'])
        textobj.textLine(mdict['rating_num'])
        textobj.textLine(mdict['quote'])
        cav.drawText(textobj)
        i += 1
        if i % 7 == 0 and i > 0: cav.showPage()
    cav.save()


def lead_json():
    with open('movie_data.json', 'r') as file:
        return json.load(file)


if __name__ == '__main__': setpdf(lead_json()[:20])