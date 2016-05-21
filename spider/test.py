#coding:utf-8

import urllib2
import urllib
import re
import MySQLdb
import webbrowser
import time
import random
from user_agents import agents

url_base = 'http://weibo.cn/'
#每次登录之前都得换一次cookies否则会有问题，大概都是登陆不上去的问题
cookie = '_T_WM=2981848bf2441c1ae56056ee5ec5656e;' \
         ' SUB=_2A256RD6kDeRxGeVM7FQT9ynJyT6IHXVZx0LsrDV6PUJbstBeLXKhkW1LHetYKr12hDcVrjVQi-_wrsz807Rdbg..; ' \
         'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhmuP4Ef-Gwl4bzviKJL7hk5JpX5o2p5NHD95Q0eoMceoMNSKzE;' \
         ' SUHB=0gHiXTv5uAeqyQ; SSOLoginState=1463832308; gsid_CTandWM=4ugaCpOz5xXtOrO6EGTcYdKjb8q'

headers = {
    'User-Agent': random.choice(agents),
    'cookie': cookie
}

def _search(name):
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
        print "Error occur:%s"% e
        return -1



def _search_rst_insert(dic):
    print dic
    time_now = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    connection = MySQLdb.connect(host = 'localhost',user = 'root',passwd = 'root',db = 'test',charset='utf8')
    cursor = connection.cursor()
    try:
        cursor.execute('create table rst_search (id int primary key auto_increment,name text,url text,location text,fans int,cnt_date datetime)')
        connection.commit()
    except Exception,e:
        pass
    #设置自增序号作为id
    try:
        for item in dic:
            query_insert = 'insert into rst_search(name,url,location,fans,cnt_date) values("%s","%s","%s",%d,"%s")'\
                           %(item['name'],item['url'],item['loc'],item['fans'],time_now)
            cursor.execute(query_insert)
            connection.commit()
    except Exception,e:
        print 'Error occur:%s' % e
        connection.close()
        return -1
    print 'Insert successful!'
    connection.close()
    return 0


if __name__=='__main__':
    dic = _search('林鸿飞')
    _search_rst_insert(dic)
