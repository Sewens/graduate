# coding:utf-8
import os
import re
import MySQLdb
import SentimentAnalyzer


# 用来进行两种格式的日期的匹配
def time_match(item):
    pattern_time1 = re.compile('\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}')
    pattern_time2 = re.compile('(\d{2})月(\d{2})日\s(\d{2}:\d{2})')
    time = pattern_time2.findall(item)
    if len(time) != 0:
        rt_time = '2016-%s-%s %s:00' % (time[0][0], time[0][1], time[0][2])
        return rt_time

    else:
        time = pattern_time1.findall(item)
        if len(time) != 0:
            rt_time = time[0]
            return rt_time
        else:
            return ''


def cnt_match(item):
    pattern_content = re.compile('<span class="ctt">(.+)</span>')
    cnt = pattern_content.findall(item)
    return cnt[0]


def id_match(item):
    pattern_id = re.compile(r'id="(.+)"><div>')
    id = pattern_id.findall(item)
    return id[0]


# 用来将爬虫爬取的有效内容提取出来


def txt_formate(fname='kaifulee'):
    filename = 'f:/%s.txt' % (fname)
    _file = open(filename, 'r')
    huge_txt = _file.read()
    pattern_zero = re.compile('id=".+"><div><span class="ctt">.+</span>.+<span class="ct">.+</span>')
    lst = []

    for item in pattern_zero.findall(huge_txt):
        dic = {}
        cnt = cnt_match(item)
        time = time_match(item)
        id = id_match(item)
        dic['cnt'] = unicode(cnt, 'utf-8')
        dic['id'] = id
        dic['time'] = time
        lst.append(dic)
    sql_insert(lst)

#新建表以及插入所有被爬到的微博内容
def sql_insert(lst,fname='kaifulee'):
    create_query = "create table %s (id varchar(64) primary key,time datetime,cnt text,sentiment1 float,sentiment2 float)" %fname
    connection = MySQLdb.connect(host='localhost',user='root',passwd='root',db='test1',charset='utf8')
    cursor = connection.cursor()
    try :
        cursor.execute(create_query)
    except Exception,e:
        pass
    finally:
        pass

    for item in lst:
        insert_query = "insert into %s values('%s','%s','%s',0,0)"%(fname, item['id'], item['time'], item['cnt'])
        try:
            cursor.execute(insert_query)
        except Exception,e:
            pass
    connection.commit()
    connection.close()

# sql_query()
#txt_formate()

if __name__=="__main__":
    analyser = SentimentAnalyzer.SentimentAnalyzer()
    analyser.load()
    connection = MySQLdb.connect(host='localhost',user='root',passwd='root',db='test1',charset='utf8')
    cursor = connection.cursor()
    select_query = 'select * from kaifulee'
    cursor.execute(select_query)
    content = cursor.fetchall()
    count = 0
    for item in content:
        count += 1
        senti = analyser.analyze(item[2])
        query = "update kaifulee set sentiment1 = %f where id = '%s'" %(senti,item[0])
        cursor.execute(query)
        print count
    connection.commit()
    connection.close()


