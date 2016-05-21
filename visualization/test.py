#coding:utf-8
import numpy
import MySQLdb
import bokeh.plotting
from bokeh.charts import Bar, output_file, show


connection = MySQLdb.connect(host = 'localhost',user = 'root',passwd = 'root',db = 'test1',charset = 'utf8')
cursor = connection.cursor()
query = "select * from kaifulee"
cursor.execute(query)
cursor.fetchall()


dic = []

for item in cursor:
    inser = {
        'data':item[3],
        'time':item[1]
    }
    dic.append(inser)

output_file('p.html')
p = bokeh.plotting.figure(width=400, height=400)
p.title = 'test'
p.xaxis.axis_label = 'Date'
p.yaxis.axis_label = 'Scale'
p.ygrid.band_fill_color="olive"
p.ygrid.band_fill_alpha = 0.1

count = 0
for item in dic:
    count += 1
    px = count
    py = 0
    color_p = '#ff0000'
    color_n = '#0000ff'
    color_c = ''
    high = item['data']
    if high>0:
        py = high/2
        color_c = color_p
    else:
        high = abs(high)
        py = - high/2
        color_c = color_n

    p.rect(x = px,y = py,width = 0.1 , height = high, color=color_c)

show(p)


