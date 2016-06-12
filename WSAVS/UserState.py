#coding:utf-8
import MySQLdb

def us_init():
    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
    cursor = connection.cursor()
    query = 'create table user_state (id int primary key auto_increment,' \
            ' user_name varchar(64),' \
            ' user_id varchar(64),' \
            ' search_state int default 0,' \
            ' spyder_state int default 0,' \
            ' analysis_state int default 0,' \
            ' freq_state int default 0)'
    try:
        cursor.execute(query)
    except Exception,e:
        print '%s Exception!' % us_init.__name__
        print 'Exception:%s' % e
    connection.commit()
    connection.close()
    print "Us_init Success!"

#user_id为查询微博是所用字段 user_name为微博用户真实id
def us_create(user_name,user_id):
    user_id = user_id.encode('utf-8')
    user_name = user_name.encode('utf-8')

    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
    cursor = connection.cursor()
    query = 'insert into user_state (user_name, user_id) values (%s, %s)'% (user_name, user_id)
    try:
        cursor.execute(query)
    except Exception, e:
        print '%s Exception!' % us_create.__name__
        print 'Exception:%s' % e
    connection.commit()
    connection.close()
    print "Us_create Success!"


#user_id为查询微博时候用的字段 state为需要进行更新的状态 名称 必须传入freq search spyder analysis 四者
def us_update(user_id,state):
    user_id = user_id.encode('utf-8')
    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
    cursor = connection.cursor()
    query = 'update user_state set %s_state = 1'% state
    try:
        cursor.execute(query)
    except Exception,e:
        print '%s Exception!' % us_update.__name__
        print 'Exception:%s' % e
    connection.commit()
    connection.close()
    print "Us_update Success!"


#检测用户状态 提交一个用户的姓名信息和一个需要查询的状态信息 返回1表示成功 返回0表示失败
def us_check(user_id,state):
    user_id = user_id.encode('utf-8')
    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
    cursor = connection.cursor()
    query = 'select * from user_state where user_id="%s"' % user_id
    try:
        cursor.execute(query)
    except Exception, e:
        print '%s Exception!' % us_check.__name__
        print 'Exception:%s' % e
        return 0
    rst_search = cursor.fetchall()
    for item in rst_search:
        if state == 'search':
            if item[3] == 1:
                return 1
            else:
                return 0
        elif state == 'spyder':
            if item[4] == 1:
                return 1
            else:
                return 0
        elif state == 'analysis':
            if item[5] == 1:
                return 1
            else:
                return 0
        elif state == 'freq':
            if item[6] == 1:
                return 1
            else:
                return 0
        else:
            return 0