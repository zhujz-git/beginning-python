from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.platypus import Image
import json


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
    cav.drawString(x_l, page_y, '豆瓣电影 Top 250')
    #图像宽 高
    img_width = 54
    img_height = 80
    #设置虚线格式
    cav.setDash(2, 1)
    i = 0
    for mdict in mlist:
        cav.line(x_l, page_y - 30, x_r, page_y - 30)
        cav.setFont(psfontname='simfang', size=10, leading=1)
        cav.drawString(55, 755, '1')
        imgulr = 'p480747492.webp.jpg'
        image = Image(imgulr)
        cav.drawImage(imgulr, 65, 685, 54, 80, 'auto')
        textobj = cav.beginText(130, 755, direction=(15, 300))
        textobj.setFont(psfontname='simfang', size=15, leading=20)
        textobj.textLines(
            '肖申克的救赎  / The Shawshank Redemption \n / 月黑高飞(港) / 刺激1995(台) ')
        textobj.setFont(psfontname='simfang', size=10, leading=15)
        textobj.textLine(
            '导演: 弗兰克·德拉邦特 Frank Darabont   主演: 蒂姆·罗宾斯 Tim Robbins /...')
        textobj.textLine('2680678人评价')
        textobj.textLine('希望让人自由。')
        cav.drawText(textobj)
        cav.showPage()
    cav.save()


def lead_json():
    with open('movie_data.json', 'r') as file:
        return json.load(file)


if __name__ == '__main__': setpdf(lead_json()[:2])