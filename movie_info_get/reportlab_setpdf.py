from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.lib import colors
import time
import os
import re
import logging
import json
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
import get_douban_movie


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
    pdf_filename = './pdf/' + minfo['id'] + '-' + minfo['reviewed'] + '.pdf'
    # 生成pdf文件
    doc = SimpleDocTemplate(pdf_filename,
                            pagesize=A4,
                            initialFontName=pdf_font)

    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.fontName = pdf_font
    styleN.alignment = TA_LEFT
    styleB = styles['BodyText']
    styleB.fontName = pdf_font
    styleT = styles['Title']
    styleT.alignment = TA_LEFT
    styleT.fontName = pdf_font
    styleT.textColor = colors.darkgoldenrod
    styleH1 = styles['Heading1']
    styleH1.fontName = pdf_font
    styleH1.textColor=colors.darkgreen
    styleH1.alignment = TA_LEFT
    styleH2 = styles['Heading2']
    styleH2.fontName = pdf_font
    styleH2.alignment = TA_LEFT
    styleH2.textColor=colors.darkblue
    styleH3 = styles['Heading3']
    styleH3.fontName = pdf_font

    story = []

    # 标题
    str_text = minfo['top_no'] + '豆瓣电影Top250'
    story.append(Paragraph(str_text, styleN))
    str_text = minfo['reviewed'] + minfo['year']
    story.append(Paragraph(str_text, styleT))

    # 电影主图+电影信息

    img = get_html_img(minfo['mainpic'])  # 读取指定路径下的图片
    img.drawWidth = 108  # 设置图片的宽度
    img.drawHeight = 160   # 设置图片的高度
    col_width = [108, 320]
    str_text = '<br />'.join(minfo['info'])
    table_para = Paragraph(str_text, styleN)
    story.append(Table([(img, table_para)], colWidths=col_width, vAlign='LEFT'))

    # 剧情简介
    str_text = minfo['related-info']
    story.append(Paragraph(str_text, styleB))

    # 演职员
    str_text = minfo['celebrities']['title']
    story.append(Paragraph(str_text, styleH1))
    cele_li = minfo['celebrities']['li']
    
    img_data = []
    cele1_data = []
    cele2_data = []
    col_width = 75
    rowHeight = [100, 10, 10]
    style = [
            ('FONTNAME', (0, 0), (-1, -1), pdf_font),  # 字体
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 所有表格上下居中对齐
            ('ALIGN', (0, 0), (-1, -1), 'CENTER')
        ]
    for cele in cele_li:
        img = get_html_img(cele[2])  # 读取指定路径下的图片
        img.drawWidth = 70#9.5*4  # 设置图片的宽度
        img.drawHeight = 99#13.4*4  # 设置图片的高度
        img_data.append(img)
        cele1_data.append(cele[0][:6])
        cele2_data.append(cele[1][:6])
    table_data = [img_data, cele1_data, cele2_data]
    story.append(Table(table_data, style=style, colWidths=col_width, rowHeights=rowHeight))

    # 显示 剧照 海报 壁纸
    table_data = []
    pic_types = minfo['related-pic']
    pic_num = 4
    for pic_type in pic_types:
        str_text = pic_type['title']
        story.append(Paragraph(str_text, styleH1))
        table_data = []
        for i in range(pic_num):
            img = get_html_img(pic_type['list'][i][1])  # 读取指定路径下的图片             
            rate = img.imageWidth/float(img.imageHeight)
            if img.imageWidth > img.imageHeight:
                img.drawWidth = 100  # 设置图片的宽度
                img.drawHeight = 100/rate  # 设置图片的高度
            else:
                img.drawWidth = 100*rate  # 设置图片的宽度
                img.drawHeight = 100  # 设置图片的高度

            table_data.append(img)
        story.append(Table((table_data,)))

    # 短评
    str_text = minfo['comments']['title']
    story.append(Paragraph(str_text, styleH1))
    comments_list = minfo['comments']['list']
    for i in range(10):
        str_text = comments_list[i][0]
        story.append(Paragraph(str_text, styleH2))
        str_text = comments_list[i][1]
        story.append(Paragraph(str_text, styleB))

    # 影评
    str_text = '影评'
    story.append(Paragraph(str_text, styleH1))
    reviews_list = minfo['reviews']
    for i in range(10):
        str_text = reviews_list[i][1] + ' ' + reviews_list[i][2]
        story.append(Paragraph(str_text, styleH2))
        str_text = reviews_list[i][3]
        story.append(Paragraph(str_text, styleB))

    doc.build(story)

    # 最后删除下载的图片临时文件
    for f in get_all_dir_file('.\\image\\tmp'):
        os.remove(f)
        logging.info('delete file:'+ f)
    logging.info('success generate a pdf:{}'.format(pdf_filename))

def lead_json(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

# 下载文件并加载，返回一个img
def get_html_img(url):
    root = './image/tmp/'
    filepath = get_douban_movie.down_web_image(url, root)
    img = Image(filepath)
    
    return img

# 写入json文件
def dump_data(file_name, json_data):
    with open(file_name, 'w') as file:
        json.dump(json_data, file, indent=2)
        logging.info('success dump file :{}'.format(file_name))

# 获取一个目录里的所有文件
def get_all_dir_file(dir):
    for root, dirs, files in os.walk(dir):
        for name in files:
            yield os.path.join(root, name)


if __name__ == '__main__':
    # 设置日志
    get_douban_movie.set_logging_config()
    # 设置中文字体
    simfang_path = './font/simsun.ttf'
    simfang_font = ttfonts.TTFont(name='simsun', filename=simfang_path)
    pdfmetrics.registerFont(font=simfang_font)
    minfo = lead_json('./json/1291546.json')
    set_movie_info_pdf(minfo)
    # set_movie_list_pdf(lead_json('./json/movie_data.json'))
