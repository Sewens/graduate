#coding:utf-8
import UserState
import MySQLdb
import pandas


#展示目前系统中各部分功能的推进情况 这一方法会将user_state表中所有用户输出
#输出所有用户状态之后进行用户选择 最终返回一个包含用户信息的dict对象
#一旦出错或者其他异常 会导致返回一个None
def hist_show():
    connection = MySQLdb.connect(host='localhost',user='root',passwd='root',db='test',charset='utf8')
    cursor = connection.cursor()
    query = 'select * from user_state'
    user = []
    print "数据准备中."
    try:
        cursor.execute(query)
        rst_search = cursor.fetchall()
        for item in rst_search:
            user_state = {}
            user_state['user_keyword'] = item[1]
            user_state['user_id'] = item[2]
            user_state['spyder'] = item[4]
            user_state['analysis'] = item[5]
            user_state['freq'] = item[6]
            user_state['visual'] = item[7]
            user.append(user_state)
    except Exception,e:
        print '%s Exception!' % hist_show.__name__
        print 'Exception:%s' % e
        return None

    print "输出当前微博用户抓取信息."
    count = 0
    for item in user:
        count += 1
        output = str(count)+u"."
        output += "user_name:" + item['user_keyword'] + "\t"
        output += "user_id:" + item['user_id'] + "\t"
        if item['spyder'] == 1:
            output += u"爬虫结果已输入|"
        else:
            output += u"爬虫结果未输入|"
        if item['analysis'] == 1:
            output += u"情感分析已完成|"
        else:
            output += u"情感分析未完成|"
        if item['freq'] == 1:
            output += u"词频统计完成|"
        else:
            output += u"词频统计未完成|"
        if item['visual'] == 1:
            output += u"可视化结果已输出|"
        else:
            output += u"可视化结果未输出|"
        print output
    print "历史结果显示完毕."
    order = 0
    while 1:
        order = input('选择您想要分析的微博用户:')
        if order < count + 1 and order > 0:
            break
        else:
            print "输入错误,请再次尝试."
    if order != 0:
        return user[order-1]
    else:
        return None