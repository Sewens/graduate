#coding:utf-8
import numpy
import MySQLdb
import bokeh.plotting
from  bokeh.models import HoverTool,BoxSelectTool,WheelZoomTool
from bokeh.charts import Bar, output_file, show
from collections import OrderedDict




#接受一个name参量作为用户的id值 使用这个id作为查询条件 查阅到相应的表进行数据分析
def draw_rect(name):
    try:
        name = unicode(name, 'utf8')
    except Exception, e:
        print '%s0 Exception!' % draw_bar.__name__
        print 'Exception:%s' % e


    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test1', charset='utf8')
    cursor = connection.cursor()
    query = "select * from %s"% name
    cursor.execute(query)
    cursor.fetchall()
    lst = []

    print "start init"
    count = 0
    for item in cursor:
        if count>100:
            break
        count += 1
        inser = {
            'data':item[3],
            'time':item[1]
        }
        lst.append(inser)

    TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,save"
    output_file('hasp.html')
    p = bokeh.plotting.figure(width=800, height=400, tools=TOOLS)
    p.title = u'%s微博分析结果' % name
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Scale'
    p.ygrid.band_fill_color="olive"
    p.ygrid.band_fill_alpha = 0.1

    print 'start ploting'
    count = 0
    for item in lst:
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


    hover = p.select_one(HoverTool)
    hover.point_policy = "follow_mouse"
    hover.tooltips = [
        ("Time", "$px"),
        ("Data", "$py"),
    ]

    show(p)


def draw_bar(name):
    try:
        name = unicode(name, 'utf8')
    except Exception, e:
        print '%s0 Exception!' % draw_bar.__name__
        print 'Exception:%s' % e
    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
    cursor = connection.cursor()
    query = "select * from %s"% name
    cursor.execute(query)
    cursor.fetchall()

    print "start init"
    count = 0
    lst_data = OrderedDict()
    lst_time = []
    lst_sentiment1 = []

    for item in cursor:
        if count>100:
            break
        count += 1
        #此处需要注意，在修改表结构之后数据可能紊乱 需要改动程序
        lst_sentiment1.append(item[3])
        lst_time.append(str(item[1]))

    lst_data['data'] = lst_sentiment1
    lst_data['days'] = lst_time

    print "complete"
    #上面都是数据准备的部分

    hover = HoverTool()
    hover.point_policy = "follow_mouse"
    hover.tooltips = [
        ("Time", "@days"),
        ("Data", "@data"),
    ]
    Tools = [hover,WheelZoomTool(),'resize','reset','box_select']

    title = u'%s微博分析结果' % name

    p = Bar(lst_data, values = 'data', label = 'days', tools = Tools,
            width = 800, height = 400, title = title)

    output_file('hasp.html')
    show(p)


draw_bar('kaifulee1')
