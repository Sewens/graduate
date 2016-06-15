#coding:utf-8
import MySQLdb
import bokeh
from bokeh.plotting import figure,ColumnDataSource
from bokeh.models import HoverTool
from bokeh.charts import output_file, show,HeatMap
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas
import bokeh.palettes #这个是热度图的着色信息


#绘图前的数据准备 返回一个dic对象
def draw_rect_data_pre(name):
    dir = path.dirname(__file__)
    try:
        name = unicode(name, 'utf8')
    except Exception, e:
        print '%s0 Exception!' % draw_rect.__name__
        print 'Exception:%s' % e
    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
    cursor = connection.cursor()
    query = 'select * from cnt_spyder where name ="%s"' % name
    cursor.execute(query)
    rst_search = cursor.fetchall()
    path_happy = dir+'\\rescources\happy.gif'
    path_sad = dir+'\\rescources\sad.gif'
    path_mid = dir+'\\rescources\mid.gif'
    if len(rst_search)== 0:
        print '无数据结果！'
        exit(0)
    print "情感分析柱状图,开始数据准备."
    count = 0
    lst_data = {}
    lst_data['id'] = []
    lst_data['cnt'] = []
    lst_data['date_time'] = []
    lst_data['agree'] = []
    lst_data['trans'] = []
    lst_data['comment'] = []
    lst_data['sentiment1'] = []
    lst_data['img'] = []
    lst_data['state'] = []
    for item in rst_search:
        count += 1
        lst_data['id'].append(count)
        lst_data['date_time'].append(str(item[3]))
        lst_data['cnt'].append(item[4])
        lst_data['agree'].append(int(item[5]))
        lst_data['trans'].append(int(item[6]))
        lst_data['comment'].append(int(item[7]))
        lst_data['sentiment1'].append(float(item[8]))
        if float(item[8]) > 0:
            lst_data['img'].append(path_happy)
            lst_data['state'].append('开心')
        elif float(item[8]) < 0:
            lst_data['img'].append(path_sad)
            lst_data['state'].append('难过')
        else:
            lst_data['img'].append(path_mid)
            lst_data['state'].append('中立')
            # 此处需要注意，在修改表结构之后数据可能紊乱 需要改动程序
    print "数据准备完成."
    return lst_data

#通过数据处理子函数得到数据之后绘制柱状图



#词云绘制的函数
def draw_word_cloud(name):
    try:
        name = name.decode('utf8')
    except:
        pass

    print '词云,数据准备.'
    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
    cursor = connection.cursor()
    query = 'select * from freq_rst where user_name ="%s"' % name
    cursor.execute(query)
    rst_search = cursor.fetchall()
    rst_freq = []
    for item in rst_search:
        temp = (unicode(item[1]),int(item[10]))
        rst_freq.append(temp)
    print '词云,数据准备完毕,开始绘图.'
    d = path.dirname(__file__)
    wordcloud = WordCloud(max_font_size=800,background_color='white', relative_scaling=.5, width=1920,
                          height=1080
                          ,font_path=r'C:\Windows\Fonts\simsun.ttc').fit_words(rst_freq)
    plt.figure()
    plt.title('Topic word Top30')
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    print '词云,绘图结束,结果输出.'
    wordcloud.to_file(path.join(d+u"\\output\\",name + u".jpg"))



def draw_rect(name):
    lst = draw_rect_data_pre(name)
    lst['sentiment2'] = []
    for item in lst['sentiment1']:
        lst['sentiment2'].append(item/2)

    Tools = ["pan,wheel_zoom,hover,save", 'resize', 'reset', 'crosshair']
    source = ColumnDataSource(lst)
    title = u'%s微博分析结果' % name
    output_file("output\%s.html"%title)
    p = figure(plot_width=1080, plot_height=640, tools=Tools)
    p.title = title
    p.xaxis.axis_label = '序号'
    p.yaxis.axis_label = '情感值'
    p.ygrid.band_fill_color = "black"
    p.ygrid.band_fill_alpha = 0.1
    p.rect("id", "sentiment2",0.5, "sentiment1", source=source,
           color="#00ccff", line_color='#00ccff')
    hover = p.select_one(HoverTool)
    hover.point_policy = "follow_mouse"
    hover.tooltips = """
                <div>
                    <div>
                        <img
                            src="@img" height="42" alt="@img" width="42"
                            style="float: left; margin: 0px 15px 15px 0px;"
                        ></img>
                        <span>情感状况:</span><span style="font-size: 17px; font-weight: bold;">@state</span>
                    </div>
                    <div>
                        <span style="font-size: 2px;">赞同数:@agree 转发数:@trans 评论数:@comment</span>
                    </div>
                    <div>
                        <span style="font-size: 1px;">时间:@date_time</span>
                    </div>
                </div>
                """
    show(p)
    print '情感分布柱状图，绘制结束.'
    return p

def draw_heat_judge(val):
    if val<20:
        return 0
    elif val<50:
        return 1
    elif val<100:
        return 2
    elif val<200:
        return 3
    elif val<350:
        return 4
    elif val<500:
        return 5
    elif val<750:
        return 6
    elif val<1000:
        return 7
    else:
        return 8

def draw_heatmap(name):
    word = []
    year = []
    freq = []
    color = []
    x_ra = []
    y_ra = ["2009","2010","2011","2012","2013","2014","2015","2016"]
    width = 1080
    height = 640
    colors = ["#ffffcc", "#ffeda0", "#fed976", "#feb24c", "#fd8d3c","#fc4e2a","#e31a1c","#bd0026","#800026"]
    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
    cursor = connection.cursor()
    query = 'select * from freq_rst where user_name ="%s"' % name
    cursor.execute(query)
    rst_search = cursor.fetchall()
    for item in rst_search:
        x_ra.append(item[1])
        for i in range(9,17):
            word.append(item[1])
            year.append(str(2000+i))
            freq_val = int(item[i-7])
            freq.append(freq_val)
            color.append(colors[min(draw_heat_judge(freq_val), 6)])
    source = ColumnDataSource(
        data=dict(year=year, word=word, freq=freq,color=color)
    )

    title = u'%s微博09-16年主题词热度图' % name
    output_file("output\%s.html" % title)
    Tools = ["pan,wheel_zoom,hover,save", 'resize', 'reset', 'crosshair','box_zoom']
    p = figure(x_range = x_ra,y_range = y_ra,tools = Tools,width=width,height=height)

    p.rect('word','year',1,1,source = source,color='color',line_color = None)

    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    hover = p.select_one(HoverTool)
    hover.point_policy = "follow_mouse"
    hover.tooltips = [
        ('Word', "$x"),
        ("Year", "$y"),
        ("Freq", "@freq"),
    ]
    p.title = title
    show(p)



'''
def draw_heatmap_data_pre(name):
    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
    cursor = connection.cursor()
    query = 'select * from freq_rst where user_name ="%s"' % name
    cursor.execute(query)
    rst_search = cursor.fetchall()
    dic={'word':[],'year':[],'frequent':[]}
    for item in rst_search:
        for i in range(9,17):
            dic['word'].append(item[1])
            dic['year'].append(2000+i)
            dic['frequent'].append(int(item[i-7]))
    frame = pandas.DataFrame(dic)
    print frame
    return frame

def draw_heatmap(name):
    frame = draw_heatmap_data_pre(name)
    title = u'%s微博09-16年主题词热度图' % name.decode('utf8')
    output_file("output\%s.html"%title)
    Tools = ['wheel_zoom','save','hover', 'resize', 'reset', 'crosshair']
    hm = HeatMap(data = frame,x='word',y='year',values = 'frequent',
                 height = 640, width = 1080,stat = None,tools=Tools)
    hover = hm.select_one(HoverTool)
    hover.point_policy = "follow_mouse"
    hover.tooltips =[
            ('Word', "$x"),
            ("Year", "@y"),
            ("Freq", "@values"),
    ]
    hm.title = title
    show(hm)
    return hm
'''
'''
#两种不同的数据准备格式
def draw_heatmap_data_2(name):
    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
    cursor = connection.cursor()
    query = 'select * from freq_rst where user_name ="%s"' % name
    cursor.execute(query)
    rst_search = cursor.fetchall()
    dic = {}
    for i in range(9, 17):
        dic[str(2000 + i)] = []
    columns = []
    index = [2009,2010,2011,2012,2013,2014,2015,2016]
    for item in rst_search:
        columns.append(item[1])
        for i in range(9,17):
            dic[str(2000+i)].append(item[i-7])
    frame = pandas.DataFrame(dic, index = columns)
    frame.columns.name = 'year'
    return frame
'''

#手动绘制rect 废弃不用的往昔代码
'''
def draw_rect_man(name):
    lst_data = draw_bar_data_pre(name)
    print '绘制模块初始化.'
    source = ColumnDataSource(lst_data)
    TOOLS = "pan,wheel_zoom,,reset,hover,save"
    Tools = [TOOLS, 'resize', 'reset', 'crosshair']
    title = u'%s微博分析结果' % name
    output_file('%s.html' % title)
    p = bokeh.plotting.figure(width=800, height=400, tools=Tools)
    p.title = title
    p.xaxis.axis_label = '序号'
    p.yaxis.axis_label = '情感值'
    p.ygrid.band_fill_color = "olive"
    p.ygrid.band_fill_alpha = 0.1
    print '开始绘图.'
    count = 0
    # 这部分是绘制柱状图时候所用的
    for item in source.data['sentiment1']:
        count += 1
        px = count
        py = 0
        color_p = '#ff0000'
        color_n = '#0000ff'
        color_c = ''
        high = item
        if high > 0:
            py = high / 2
            color_c = color_p
        else:
            high = abs(high)
            py = - high / 2
            color_c = color_n
        p.rect(x=px, y=py, width=0.1, height=high, color=color_c)
    p.circle('id', 'sentiment1', source=source, size=3)
    hover = p.select_one(HoverTool)
    # hover.point_policy = "follow_mouse"
    hover.tooltips = """
            <div>
                <div>
                    <img
                        src="@img" height="42" alt="@img" width="42"
                        style="float: left; margin: 0px 15px 15px 0px;"
                    ></img>
                    <span>情感状况:</span><span style="font-size: 17px; font-weight: bold;">@state</span>
                </div>
                <div>
                    <span style="font-size: 2px;">赞同数:@agree 转发数:@trans 评论数:@comment</span>
                </div>
                <div>
                    <span style="font-size: 1px;">时间:@date_time</span>
                </div>
            </div>
            """
    show(p)
    print '绘制结束.'
'''