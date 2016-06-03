#coding:utf-8
import MySQLdb

#这个字符串为分析词频时所用，先将一年中所有微博汇总到一个对象中，之后对该对象进行分析

connect = MySQLdb.Connect(host='localhost',user='root',passwd='root',db='test1',charset='utf8')
cursor = connect.cursor()
query = 'create table %s_freq (id int primary key auto increment,' \
        'word varchar(64) unique,' \
        'freq09 int,freq10 int,freq11 int,freq12 int,freq13 int,freq14 int,freq15 int,freq16 int)' % 'kaifulee'
cnt_analysis = ''
for i in range(9, 16):
    str_tail = ''
    if i < 10:
        str_tail = '0' + str(i)
    elif i >= 10:
        str_tail = str(i)
    query = 'SELECT * FROM test1.李开复 where time between "20%s-01-01 00:00:00" and "20%s-12-31 23:59:59"' \
            % (str_tail, str_tail)
    print query
    cursor.execute(query)
    result = cursor.fetchall()
    # 这步骤后，将所有的语料统一起来 进入下一步分析
    for item in result:
        cnt_analysis += item[4]
    print  cnt_analysis