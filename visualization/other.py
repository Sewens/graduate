#coding:utf-8
import jieba
import MySQLdb
import jieba.posseg as pseg
import bokeh.plotting
from bokeh.charts import Bar, output_file, show



noneed = [u'评论',u'微',u'图片',u'原图',u'博',u'全文', u'时',u'转发',u'事']

def ishan(text):
    # for python 2.x, 3.3+
    # sample: ishan(u'一') == True, ishan(u'我&&你') == False
    return all(u'\u4e00' <= char <= u'\u9fff' for char in text)




def func():
    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test1', charset='utf8')
    cursor = connection.cursor()
    query = "select * from kaifulee"
    cursor.execute(query)
    cursor.fetchall()

    txt = ' '
    for item in cursor:
        txt +=unicode(item[2])
    rst = pseg.cut(txt, 1)
    dic = {}
    connection.close()

    for item, flag in rst:
        if ishan(item):
            if item in noneed:
                continue
            if(flag == 'n' or flag == 'an'):
                if item in dic:
                    dic[item] += 1
                else:
                   dic[item] = 0
        else:
            pass

    ranking = []
    for i in range(0,100):
        rank = 0
        lable = ''
        for item in dic:
            if rank>=dic[item]:
                pass
            else:
                rank = dic[item]
                lable = item
        ranking.append([lable,dic[lable]])
        dic.pop(lable)

    for item in ranking:
        print unicode(item[0]),item[1]
    output_file('p.html')
    p = bokeh.plotting.figure(width=400, height=400)
    p.title = '热词统计'
    p.xaxis.axis_label = '词频数'
    p.yaxis.axis_label = '词语'
    p.ygrid.band_fill_color="olive"
    p.ygrid.band_fill_alpha = 0.1
    count = 0
    for item in ranking:
        count += 1
        px = count
        high = item[1]
        py = high/2
        p.rect(x = px,y = py,width = 0.2 , height = high, color='#ff0000')
    show(p)

func()


