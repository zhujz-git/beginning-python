from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics, ttfonts
import json
from reportlab.lib import colors
import time


def setpdf(mlist):
    # 设置中文字体
    simfang_path = './font/simsun.ttf'
    simfang_font = ttfonts.TTFont(name='simsun', filename=simfang_path)
    pdfmetrics.registerFont(font=simfang_font)
    cav = canvas.Canvas('./pdf/doubanmovie250.pdf')
    pdf_font = 'simsun'

    # 页面高度
    page_y = 841.89 - 30
    # 划线开始
    pagey_offset = page_y - 20
    # 图片开始
    movie_offset = pagey_offset - 20
    # 文字起始位置
    x_l = 50
    x_r = 545
    page_width = 595.27

    # 图像宽 高
    img_width = 54
    img_height = 80
    bNewpage = True
    i = 0
    for mdict in mlist:
        # 7项一页
        offset = i % 7

        # 设置页眉页脚
        if bNewpage:
            cav.setFont(psfontname=pdf_font, size=15)
            cav.setFillColor(colors.blue)
            cav.drawCentredString(page_width / 2, page_y, '豆瓣电影 Top 250 ')

            cav.setFont(psfontname=pdf_font, size=8)
            cav.setFillColor(colors.black)
            cav.setDash(1, 0)
            cav.line(x_l, 40, x_r, 40)
            cav.drawRightString(
                x_r, 20, 'created by zhujz ' + time.strftime('%Y-%m-%d'))
            cav.drawCentredString(page_width / 2, 20,
                                  '第 {} 页'.format(cav.getPageNumber()))

            bNewpage = False
        # 换页
        if offset == 0 and i > 0:
            cav.showPage()
            bNewpage = True

        # 虚线
        cav.setDash(2, 1)
        cav.setFillColor(colors.black)
        cav.line(x_l, pagey_offset - offset*100,
                 x_r, pagey_offset - offset*100)
        cav.setFont(psfontname=pdf_font, size=10, leading=1)

        # 序号+电影图片
        cav.setFillColor(colors.darkgray)
        cav.drawString(x_l, movie_offset - offset*100, mdict['em'])
        imgulr = mdict['image_addr']
        cav.drawImage(imgulr, x_l + 15, movie_offset - img_height +
                      10 - offset*100, img_width, img_height, 'auto')

        # 电影介绍
        textobj = cav.beginText(130, movie_offset - offset*100, (80, 400))
        textobj.setFont(psfontname=pdf_font, size=12, leading=15)
        textobj.setFillColor(colors.ReportLabBlue)
        textobj.textLines(mdict['title'])
        textobj.textLines(mdict['other'])
        textobj.setFillColor(colors.black)
        textobj.setFont(psfontname=pdf_font, size=10, leading=12)
        textobj.textLines(mdict['review'])
        textobj.textLine(mdict['rating_num'])
        textobj.textLine(mdict['quote'])
        cav.drawText(textobj)

        i += 1
    cav.save()


def lead_json(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)
def dump_data(file_name, json_data):
    with open(file_name, 'w') as file:
        json.dump(json_data, file, indent=2)
        print('success dump file :{}'.format(file_name))


if __name__ == '__main__':
    setpdf(lead_json('./json/movie_data.json'))
