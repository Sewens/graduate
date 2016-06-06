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



def freq_analysis(name):
    #这部分是对文件名进行处理的函数，对不同情形下文件名处理 保证不会发生编码问题
    print '建立数据库连接.'
    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
    cursor = connection.cursor()
    query = ''
    print '数据库连接完成.'
    #本部分有三层循环 第一层作用在于将不同年份的微博信息取出
    #第二层循环为将这一年单条微博的内容进行带有词性标注的分析工作
    #第三层则是对词频的统计部分
    print '开始各年度词频统计.'
    count = 0
    dic = {}
    for i in range(9, 16):
        str_tail = ''

        if i < 10:
            str_tail = '0' + str(i)
        elif i >= 10:
            str_tail = str(i)
        query = 'SELECT * FROM cnt_spyder where name="%s"and date_time between "20%s-01-01 00:00:00" and "20%s-12-31 23:59:59"' \
                % (name,str_tail, str_tail)
        cursor.execute(query)
        rst_search = cursor.fetchall()

        for item in rst_search:
            count +=1
            txt = unicode(item[4])
            print '开始对第%d条微博进行分析.'%count
        #pseg是jieba分析的词性标注分词器
            rst = pseg.cut(txt, 1)
            for item, flag in rst:
                #ishan函数用于判定是否为汉语字符
                #dic对象是存储所有频率信息的对象
                '''各个其中数据组织方式为
                    dic ={'词语名':{'09':值,'10':值....}}
                    这样的字典中包含字典的形式
                '''
                #算法首先判断这个词是否为汉语 之后判断是否在拒绝词列表中
                #之后在dic对象中搜索 词存在，则将当前年度对应的词频进行加一更新
                #若词不存在 则执行初始化部分 新建一个内部dic对象 将属性名写入 数据初始化为0 表示各年度的数据值情况
                if ishan(item):
                    if item in noneed:
                        continue
                    if (flag == 'n' or flag == 'an'):
                        if item in dic:
                            dic[item][str_tail] += 1
                            dic[item]['sum'] += 1
                        else:
                            dic[item] = {}
                            dic[item]['09'] = 0
                            dic[item]['10'] = 0
                            dic[item]['11'] = 0
                            dic[item]['12'] = 0
                            dic[item]['13'] = 0
                            dic[item]['14'] = 0
                            dic[item]['15'] = 0
                            dic[item]['16'] = 0
                            dic[item]['sum'] = 0
                else:
                    pass
    #选出前30热词
    ranking = []
    for i in range(0, 100):
        rank = 0
        lable = ''
        for item in dic.keys():
            if rank >= dic[item]['sum']:
                pass
            else:
                rank = dic[item]['sum']
                lable = item
        #print lable,rank
        ranking.append([lable, dic[lable]])
        dic.pop(lable)
    for item in ranking:
        print item[0],item[1]
    connection.commit()
    connection.close()
    return ranking

#配合freq_analysis函数使用的函数 主要功能在于将rank值插入rank为一个list对象，list中包含list
#子list中第一个元素为单词 第二个元素为一个包含着各个年度的词频率信息
def freq_insert(rank,name):
    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
    cursor = connection.cursor()
    count = 0
    for item in rank:
        count += 1
        dic = item[1]
        query = 'insert into freq_rst (' \
            'word,' \
            'freq09,' \
            'freq10,' \
            'freq11,' \
            'freq12,' \
            'freq13,' \
            'freq14,' \
            'freq15,' \
            'freq16,' \
            'freq_sum,' \
            'user_name) values' \
            '("%s",%d,%d,%d,%d,%d,%d,%d,%d,%d,"%s")' % (item[0],dic['09'],dic['10'],dic['11'],dic['12'],dic['13'],dic['14'],dic['15'],dic['16'],dic['sum'],name.decode('utf8'))
        cursor.execute(query)
        print '插入第%d条词段.' % count
    print '插入完成！'
    connection.commit()
    connection.close()

#用于将表更新 计算各年中各词频率之和
#用于将总词频数进行计算
def freq_update():
    connection = MySQLdb.Connect(host='localhost', user='root', passwd='root', db='test1', charset='utf8')
    cursor = connection.cursor()
    query = 'select * from freq_rst'
    cursor.execute(query)
    rst_select = cursor.fetchall()
    count = 0
    for item in rst_select:
        count +=1
        freq_sum = item[2]+item[3]+item[4]+item[5]+item[6]+item[7]+item[8]+item[9]
        query = 'update freq_rst set freq_sum=%d where id=%d'%(freq_sum,item[0])
        cursor.execute(query)
        print '更新第%d条完毕！'% count

#用于建表 内含各年度词频数据
def freq_init():
    connection = MySQLdb.Connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
    cursor = connection.cursor()
    # 此处开始是各年度的词汇频率统计处理部分
    query = 'create table freq_rst (' \
            'id int primary key auto_increment,' \
            'word varchar(64) unique,' \
            'freq09 int default 0,' \
            'freq10 int default 0,' \
            'freq11 int default 0,' \
            'freq12 int default 0,' \
            'freq13 int default 0,' \
            'freq14 int default 0,' \
            'freq15 int default 0,' \
            'freq16 int default 0,' \
            'freq_sum int default 0,' \
            'user_name varchar(64))'
    try:
        cursor.execute(query)
    except Exception, e:
        print "%s tb_create Exception!" % freq_init.__name__
        print "Exception:%s" % e



'''
#词频统计模块 首先将微博内容分析一遍，得出出现频率最高的30词，之后用这30词在各年份中统计词频率并新建数据表写入
#参数依然是目标微博用户的id
#旧的分析词频模块 目前已经可以不用了
def freq_analysis(name):
    #这部分是对文件名进行处理的函数，对不同情形下文件名处理 保证不会发生编码问题

    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
    cursor = connection.cursor()
    query = 'select * from cnt_spyder where name="%s"'% name
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
    connection.commit()
    connection.close()
    return ranking


def annual_freq_analysis(ranking,name):
    connection = MySQLdb.Connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
    cursor = connection.cursor()
    #此处开始是各年度的词汇频率统计处理部分
    for item in ranking:
        query = 'insert into freq_rst (word) values("%s")' % item[0]
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

    #这部分是用于尝试绘制热度图的部分 应该注释的
    data = {'word1': word,
            'heat': _heat,
            'word2': [1,2,3,4,5]}
    output_file('heatmap.html')
    hm = HeatMap(data, x='word1', y='word2', values='heat',title='Heat', stat=None)
    show(hm)

'''