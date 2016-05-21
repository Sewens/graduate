#coding:utf-8
from bokeh.charts.utils import df_from_json
from bokeh.charts import HeatMap, output_file, show
import MySQLdb
import jieba.posseg as pseg


noneed = [u'评论',u'微',u'图片',u'原图',u'博',u'全文', u'时',u'转发',u'事']


def ishan(text):
    # for python 2.x, 3.3+
    # sample: ishan(u'一') == True, ishan(u'我&&你') == False
    return all(u'\u4e00' <= char <= u'\u9fff' for char in text)


def heat():
    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test1', charset='utf8')
    cursor = connection.cursor()
    query = "select * from kaifulee"
    cursor.execute(query)
    cursor.fetchall()

    txt = ' '
    for item in cursor:
        txt += unicode(item[2])
    rst = pseg.cut(txt, 1)
    dic = {}
    connection.close()
    for item, flag in rst:
        if ishan(item):
            if item in noneed:
                continue
            if (flag == 'n' or flag == 'an'):
                if item in dic:
                    dic[item] += 1
                else:
                    dic[item] = 0
        else:
            pass
    ranking = []
    for i in range(0, 100):
        rank = 0
        lable = ''
        for item in dic:
            if rank >= dic[item]:
                pass
            else:
                rank = dic[item]
                lable = item
        ranking.append([lable, dic[lable]])
        dic.pop(lable)
    # (dict, OrderedDict, lists, arrays and DataFrames are valid inputs)
    word = [word[0] for word in ranking]
    _heat = [hea[1] for hea in ranking]
    _file = open('xixi.txt','w')
    _file.write(str(ranking))
    _file.close()

    data = {'word1': word,
            'heat': _heat,
            'word2': [1,2,3,4,5]}
    output_file('heatmap.html')
    hm = HeatMap(data, x='word1', y='word2', values='heat',title='Heat', stat=None)
    show(hm)

heat()