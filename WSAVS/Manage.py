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



#词频统计模块 首先将微博内容分析一遍，得出出现频率最高的30词，之后用这30词在各年份中统计词频率并新建数据表写入
#参数依然是目标微博用户的id
def freq_analysis(name):
    #这部分是对文件名进行处理的函数，对不同情形下文件名处理 保证不会发生编码问题
    try:
        filename = unicode(name, 'utf8')
    except Exception, e:
        print '%s0 Exception!' % freq_analysis.__name__
        print 'Exception:%s' % e
    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test1', charset='utf8')
    cursor = connection.cursor()
    query = "select * from %s"%name
    cursor.execute(query)
    cursor.fetchall()
    txt = []
    for item in cursor:
        txt.append(unicode(item[2]))
    text = ''.join(txt)
    #pseg是jieba分析的词性标注分词器
    rst = pseg.cut(text, 1)
    dic = {}
    for item, flag in rst:
        #ishan函数用于判定是否为汉语字符
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
    for i in range(0, 30):
        rank = 0
        lable = ''
        for item in dic:
            if rank >= dic[item]:
                pass
            else:
                rank = dic[item]
                lable = item
        #print lable,rank
        ranking.append([lable, dic[lable]])
        dic.pop(lable)
    query = "create table %s_freq (id int primary key auto_increment,word varchar(32),freq int)"% name
    cursor.execute(query)
    for item in ranking:
        query = 'insert into %s_freq (word,freq) values (%s,%d)'%(name,item[0],item[1])
        cursor.execute(query)
    connection.commit()
    connection.close()

    return ranking
#用于将表更新 计算各年中各词频率之和


#用于建表 内含各年度词频数据
def freq_init():
    connection = MySQLdb.Connect(host='localhost', user='root', passwd='root', db='test1', charset='utf8')
    cursor = connection.cursor()
    # 此处开始是各年度的词汇频率统计处理部分
    query = 'create table freq_rst (id int primary key auto_increment,' \
            'word varchar(64) unique,' \
            'freq09 int default 0,' \
            'freq10 int default 0,' \
            'freq11 int default 0,' \
            'freq12 int default 0,' \
            'freq13 int default 0,' \
            'freq14 int default 0,' \
            'freq15 int default 0,' \
            'freq16 int default 0,' \
            'freq_sum int default 0' \
            'user_name varchar(64))'
    try:
        cursor.execute(query)
    except Exception, e:
        print "%s tb_create Exception!" % freq_init.__name__
        print "Exception:%s" % e


#最终还是使用子函数进行统计
def annual_freq_analysis(ranking,id_name):
    connection = MySQLdb.Connect(host='localhost', user='root', passwd='root', db='test1', charset='utf8')
    cursor = connection.cursor()
    #此处开始是各年度的词汇频率统计处理部分
    for item in ranking:
        query = 'insert into %s_freq (word) values("%s")' % (id_name, item[0])
        print query
        cursor.execute(query)
    connection.commit()
    try:
        pass
    except Exception,e:
        print "%s tb_insert Exception!" % annual_freq_analysis.__name__
        print "Exception:%s" % e
        return -2
    cnt_analysis = ''
    for i in range(9, 16):
        str_tail = ''
        if i < 10:
            str_tail = '0' + str(i)
        elif i >= 10:
            str_tail = str(i)
        query = 'SELECT * FROM test1.李开复 where time between "20%s-01-01 00:00:00" and "20%s-12-31 23:59:59"' \
                % (str_tail, str_tail)
        #print query
        cursor.execute(query)
        result = cursor.fetchall()
        # 这步骤后，将所有的语料统一起来 进入下一步分析每次循环之前将其清空
        cnt_analysis = ''
        for item in result:
            cnt_analysis += item[4]
        #调用分词器处理文本
        rst = pseg.cut(cnt_analysis,1)
        #复制一份ranking词典 用作年度热词统计的计数词典 之后将原来的频度信息清空
        annual_ranking = ranking
        for item in annual_ranking:
            item[1]=0

        #分词之后item即为分好的词
        for item,flag in rst:
            # ishan函数用于判定是否为汉语字符
            if ishan(item):
                for freq_word in annual_ranking:
                    if item == freq_word[0]:
                        freq_word[1]+=1

        for item in annual_ranking:
            #print item[0],item[1]
            query = 'update %s_freq set freq%s=%d where word="%s"' % (id_name, str_tail, int(item[1]),item[0])
            cursor.execute(query)
            connection.commit()

    connection.close()

    word = [word[0] for word in ranking]
    _heat = [hea[1] for hea in ranking]
    _file = open('xixi.txt','w')
    _file.write(str(ranking))
    _file.close()

'''
    data = {'word1': word,
            'heat': _heat,
            'word2': [1,2,3,4,5]}
    output_file('heatmap.html')
    hm = HeatMap(data, x='word1', y='word2', values='heat',title='Heat', stat=None)
    show(hm)
'''

if __name__=="__main__":
    ranking = freq_analysis('kaifulee')
    #annual_freq_analysis(ranking,'kaifulee')