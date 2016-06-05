#coding:utf-8
import MySQLdb

def Us_init():
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
        print '%s Exception!' % Us_init.__name__
        print 'Exception:%s' % e
    connection.commit()
    connection.close()
    print "Us_init Success!"

#user_id为查询微博是所用字段 user_name为微博用户真实id
def Us_create(user_name,user_id):
    user_id = user_id.encode('utf-8')
    user_name = user_name.encode('utf-8')

    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
    cursor = connection.cursor()
    query = 'insert into user_state (user_name, user_id) values (%s, %s)'% (user_name, user_id)
    try:
        cursor.execute(query)
    except Exception, e:
        print '%s Exception!' % Us_create.__name__
        print 'Exception:%s' % e
    connection.commit()
    connection.close()
    print "Us_create Success!"


#user_id为查询微博时候用的字段 state为需要进行更新的状态
#1 为search状态
#2 为spyder状态
#3 为analysis状态
#4 为freq状态
def Us_update(user_id,state):
    user_id = user_id.encode('utf-8')
    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
    cursor = connection.cursor()
    lst_state = [0,0,0,0]
    if state == 1:
        lst_state[0] = 1
    elif state == 2:
        lst_state[1] = 1
    elif state == 3:
        lst_state[2] = 1
    elif state == 4:
        lst_state[3] = 1
    else:
        print "State Error, nothing happend!"

    query = 'update user_state set search_state = %d,' \
            ' spyder_state = %d,' \
            ' analysis_state = %d,' \
            ' freq_state = %d where user_id="%s"' % (lst_state[0],lst_state[1],lst_state[2],lst_state[3],user_id)
    try:
        cursor.execute(query)
    except Exception,e:
        print '%s Exception!' % Us_update.__name__
        print 'Exception:%s' % e
    connection.commit()
    connection.close()
    print "Us_update Success!"