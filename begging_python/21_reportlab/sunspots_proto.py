from reportlab.lib import colors
from reportlab.graphics.shapes import *
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics import renderPDF
from urllib.request import urlopen

import json

def yearmon_to_num(stryearmon):
    yearmon = stryearmon.split('-')
    a = int(yearmon[0]) + int(yearmon[1])/12.0
    return a

#读取json数据文件
data_file_solar = urlopen(
    'https://services.swpc.noaa.gov/json/solar-cycle/predicted-solar-cycle.json')
jsondata_solar = json.load(data_file_solar)

drawing = Drawing(400, 200)
pred = [row['predicted_ssn'] for row in jsondata_solar]
high = [row['high_ssn']  for row in jsondata_solar]
low = [row['low_ssn'] for row in jsondata_solar]
times = [yearmon_to_num(row['time-tag']) for row in jsondata_solar]

lp = LinePlot()

lp.x = 50
lp.y = 50
lp.height = 125
lp.width = 300
lp.data = [
    list(zip(times, pred)),
    list(zip(times, high)),
    list(zip(times, low)),
]
lp.lines[0].strokeColor = colors.blue
lp.lines[1].strokeColor = colors.red
lp.lines[2].strokeColor = colors.green

drawing.add(lp)

drawing.add(String(250,150, 'Sunspots', fontSize=14, fillColor=colors.red))

renderPDF.drawToFile(drawing, 'report2.pdf', 'Sunspots')