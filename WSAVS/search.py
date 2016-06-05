#coding:utf-8
import urllib
import urllib2
import re
import MySQLdb
import webbrowser
import time
import random
from UserAgents import agents
from Cookies import *



#查询函数 通过get方法访问weibo.cn/search 将所要查询的内容提交给后台 返回一个查询结果
#但是目前存在问题，搜索只能获取到第一页的结果，后续页的访问会遇到403错误，留待解决
#函数参数为搜索的字符串 返回一个包含搜索结果的list对象
def Search(name):
    url = url_base + "/search/?pos=search"
    req = urllib2.Request(url, headers=headers)
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    req.add_header('Connection', 'keep-alive')
    data = 'keyword='+ urllib.quote(name) +'&suser=%E6%89%BE%E4%BA%BA'
    req.add_data(data)
    #上面是构造初次访问的访问包
    text_final = ''  # 将搜索页面的全部结果汇总到一个对象中 便于处理
    text_final += urllib2.urlopen(req).read()
    #获取到总的搜索页数 之后通过页码进行后续搜索页的访问
    '''
    _cmp_page = re.compile(r'<input name="mp" type="hidden" value="(\d)"')
    num_page = int(_cmp_page.findall(text_final)[0])
    for count in range(2,num_page+1):
        url_next = 'http://weibo.cn/search/mblog?keyword=%s&page=%d' % (urllib.quote(name),count)
        text_final += urllib2.urlopen(req).read()
    '''
    #这部分代码由于经常出现403Forbidden错误而难以使用，在排出问题之前只能将其注释掉了
    #这意味着只能获取到搜索页的第一页内容
    _cmp_block = re.compile(r'<table>(.+?)</table>')
    rst_block = _cmp_block.findall(text_final)
    #定义一个list用于返回整个搜索的结果（目前只能返回10条）
    lst_rst = []
    for item in rst_block:
        lst_rst.append(_find_rst(item))
    return lst_rst



#用于匹配出html文档中搜索信息的函数 输入文本输出一个包含所需要特定内容的dict对象
def _find_rst(txt):
    dic = {}
    #构造匹配搜索结果url的模式
    try:
        _cmp_url = re.compile(r'<a href="(.+?)"')
        rst_match = _cmp_url.findall(txt)[0]
        dic['url'] = rst_match[0:len(rst_match) - 11]
        _cmp_fans = re.compile(r'粉丝(\d+)')
        dic['fans'] = int(_cmp_fans.findall(txt)[0])
        _cmp_loc = re.compile(r'&nbsp;(.+?)<br/>')
        dic['loc'] = _cmp_loc.findall(txt)[0]
        # 构造匹配姓名的模式
        _cmp_name = re.compile(r'<a href="%s.+?\D">(.+?)</a>' % dic['url'])
        name_tmp = _cmp_name.findall(txt)[0]
        dic['name'] = re.findall(r'<a href="%s.+">(.+?)$' % dic['url'],name_tmp)[0]
        return dic
    except Exception , e:
        print '%s Exception!' % _find_rst.__name__
        print 'Exception:%s'% e
        return -1

#用于建立搜索结果保存所用的数据表
def Search_init():
    time_now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    connection = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
    cursor = connection.cursor()
    try:
        cursor.execute('create table rst_search'
                       ' (id int primary key auto_increment,'
                       'name text,'
                       'url varchar(64) unique,'
                       'location text,'
                       'fans int,'
                       'cnt_date datetime,'
                       'key_word text)')
        connection.commit()
    except Exception, e:
        print '%s Exception!' % Search_rst_insert.__name__
        print 'Exception:%s' % e

#将搜索结果导入数据库 dic为搜索得到的信息结果 key_word为当前搜索所使用的关键词
def Search_rst_insert(dic,key_word):
    time_now = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    connection = MySQLdb.connect(host = 'localhost',user = 'root',passwd = 'root',db = 'test',charset='utf8')
    cursor = connection.cursor()
    #设置自增序号作为id
    try:
        for item in dic:
            query_insert = 'insert into rst_search' \
                '(name,url,location,fans,cnt_date,key_word) values("%s","%s","%s",%d,"%s","%s") ' \
                           %(item['name'],item['url'],item['loc'],item['fans'],time_now,key_word)
            cursor.execute(query_insert)
            connection.commit()
    except Exception,e:
        print '%s Exception!' % Search_rst_insert.__name__
        print 'Exception:%s'% e
        connection.close()
        return -1
    print 'Insert complete!'
    connection.close()
    return 0

#从数据库中取出插入完毕后的模块
#name为用户当初搜索时所用的字符串，这一对象被用来区分搜索结果
def Search_rst_fetch(name):
    connect = MySQLdb.Connect(host='localhost', user='root', passwd='root', db='test',charset='utf8')
    cursor = connect.cursor()
    query = 'select * from rst_search where key_word="%s"'% name
    order = -1
    try:
        cursor.execute(query)
        content = cursor.fetchall()
        retn = []
        count = 0
        for item in content:
            count +=1
            dic = {}
            dic['name'] = item[1]
            dic['url'] = item[2]
            dic['loc'] = item[3]
            print "No.%d: Name:%s \tLocation:%s \tUrl:%s"%(count ,dic['name'],dic['loc'],dic['url'])
            retn.append(dic)
        while 1:
            order = input('Choose a user to start:')
            if order < count+1 and order >0:
                break
            else:
                print "Wrong number!"

    except Exception,e:
        print '%s Exception!' % Search_rst_fetch.__name__
        print 'Exception:%s' % e
        connect.close()
        return -1
    print "Fetch successful!"
    connect.close()
    return retn[order - 1]
