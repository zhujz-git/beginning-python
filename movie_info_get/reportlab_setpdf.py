from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics, ttfonts
import json
from reportlab.lib import colors
import time
import logging
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import A4

def set_movie_list_pdf(mlist):

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
        cav.line(x_l, pagey_offset - offset * 100, x_r,
                 pagey_offset - offset * 100)
        cav.setFont(psfontname=pdf_font, size=10, leading=1)

        # 序号+电影图片
        cav.setFillColor(colors.darkgray)
        cav.drawString(x_l, movie_offset - offset * 100, mdict['em'])
        imgulr = mdict['image_addr']
        cav.drawImage(imgulr, x_l + 15,
                      movie_offset - img_height + 10 - offset * 100, img_width,
                      img_height, 'auto')

        # 电影介绍
        textobj = cav.beginText(130, movie_offset - offset * 100, (80, 400))
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


def set_movie_info_pdf(minfo):

    pdf_font = 'simsun'
    # 生成pdf文件
    doc = SimpleDocTemplate('./pdf/frame_test.pdf', pagesize=A4)
    
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.fontName = 'simsun'      # 字体名
    styleN.fontSize = 18            # 字体大小
    styleN.leading = 50             # 行间距
    styleN.textColor = colors.green     # 字体颜色
    styleN.alignment = 1    # 居中
    styleN.wordWrap = 'CJK'
    styleH = styles['Heading1']
    story = []

    # add some flowables
    story.append(Paragraph("This is a Heading", styleH))
    titile = Paragraph("This is a paragraph in <i>Normal</i> style. <br /> This is a paragraph in <i>Normal</i> style.",
                           styleN)
    story.append(titile)
    img = Image('https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2879160094.webp')       # 读取指定路径下的图片
    img.drawWidth = 5*cm        # 设置图片的宽度
    img.drawHeight = 8*cm       # 设置图片的高度
    col_width = 120
    data = [(img, titile)]
    ta = Table(data)
    story.append(ta)
    story.append(img)
    str_para = ''
    for i in range(100):
            str_para += '影片讲述拥有一双明眸的朱芷欣（吴千语 饰），却有一对失明父母：甘笑红（惠英红 饰）、朱国强（吴岱融'
    story.append(Paragraph(str_para, styleN))

    #f = Frame(inch, inch, 6*inch, 9*inch, showBoundary=0)
    #f.addFromList(story, canv)
    
    doc.build(story)


def lead_json(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)


def dump_data(file_name, json_data):
    with open(file_name, 'w') as file:
        json.dump(json_data, file, indent=2)
        logging.info('success dump file :{}'.format(file_name))


if __name__ == '__main__':
    # 设置中文字体
    simfang_path = './font/simsun.ttf'
    simfang_font = ttfonts.TTFont(name='simsun', filename=simfang_path)
    pdfmetrics.registerFont(font=simfang_font)
    minfo = []
    set_movie_info_pdf(minfo)
    # set_movie_list_pdf(lead_json('./json/movie_data.json'))
