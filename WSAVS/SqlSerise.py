#coding:utf-8
import MySQLdb
from SentimentAnalyzer import *


#用于进行用户的情感情况分析 调用SentimentAnalyzer使用
#name字段主要用于在表content中查询指定的用户的微博进行修改
#同属于sql系列的函数
def sql_sntianaly(name):
    analyzer = SentimentAnalyzer()
    analyzer.load()
    connection = MySQLdb.Connect(host='localhost',user='root',passwd='root',db='test',charset='utf8')
    cursor = connection.cursor()
    query = 'select * from cnt_spyder where name="%s"' % name
    cursor.execute(query)
    rst_query = cursor.fetchall()
    count = 0
    for item in rst_query:
        count += 1
        txt_tweet = item[4]
        rst_float = analyzer.analyze(txt_tweet)
        print "正在分析第:%d条，情感结果:%f." % (count,rst_float)
        query = 'update cnt_spyder set sentiment1=%f where id=%d' % (rst_float,item[0])
        cursor.execute(query)
    print '分析完毕！'
    connection.commit()
    connection.close()


#sql 系列的函数用于处理微博内容表中相关的信息
#用于创建存储微博内容的表 表名content
def sql_create():
    #其中的name字段为 微博用户的id
    create_query = 'create table cnt_spyder (' \
                   'id int primary key auto_increment,' \
                   'flag varchar(16),' \
                   'ident varchar(16) unique,' \
                   'date_time datetime,' \
                   'cnt text,' \
                   'agree int,' \
                   'trans int,' \
                   'comment int,' \
                   'sentiment1 float default -127,' \
                   'sentiment2 float default -127,' \
                   'name varchar(32))'
    print create_query
    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
    cursor = connection.cursor()
    try:
        cursor.execute(create_query)
    except Exception, e:
        print "%s table create Exception!" % sql_insert.__name__
        print "Exception:%s" % e
    connection.close()


#插入指定内容 内容由lst传入 lst传入一次处理得到的所有单条微博信息
def sql_insert(lst):
    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
    cursor = connection.cursor()
    for item in lst:
        item = dict(item)
        item['cnt'] = item['cnt'].replace('\"','\'')
        insert_query = 'insert into cnt_spyder (' \
                       'flag,' \
                       'ident,' \
                       'date_time,' \
                       'cnt,' \
                       'agree,' \
                       'trans,' \
                       'comment,' \
                       'name) values' \
                '("%s","%s","%s","%s",%d,%d,%d,"%s")'\
        % (item['flag'], item['ident'], item['time'],item['cnt'],int(item['agree']),int(item['trans']),int(item['commit']),item['name'].decode('utf-8'))
        print insert_query
        try:
            cursor.execute(insert_query)
        except Exception,e:
            print "%s table insert Exception!" % sql_insert.__name__
            print "Exception:%s" % e
    connection.commit()
    connection.close()
