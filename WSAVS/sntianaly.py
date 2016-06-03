#coding:utf-8
from SentimentAnalyzer import *
import MySQLdb


def sntianaly(name):
    try:
        name = unicode(name, 'utf8')
    except Exception, e:
        print '%s0 Exception!' % sntianaly.__name__
        print 'Exception:%s' % e

    analyzer = SentimentAnalyzer()
    analyzer.load()

    connection = MySQLdb.Connect(host='localhost',user='root',passwd='root',db='test',charset='utf8')
    cursor = connection.cursor()
    query = 'select * from %s where sentiment1=-1' % name
    rst_query = cursor.execute(query)

    for item in rst_query:
        txt_tweet = item[4]
        rst_float = analyzer.analyze(txt_tweet)
        query = 'update table %s set sentiment1=%f' % (name,rst_float)
        cursor.execute(query)

    connection.commit()
    connection.close()
