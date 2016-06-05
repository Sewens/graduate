#coding:utf-8
import urllib2
import re
import time
import random
from UserAgents import agents
import subprocess
from Cookies import *
import Extract



def find_startnumber(filename):
    start = 0
    filename = filename.encode('utf-8')
    try:
        __file = open(filename, 'r')
        lis = __file.read()
        re_one = re.compile('<number>\d+</number>')
        num = re_one.findall(lis)
        re_num = re.compile('\d+')
        for every in num:
            temp = int(re_num.findall(every)[0])
            # print 'temp:' + str(temp)
            if (start < temp):
                start = temp
            else:
                pass
        # print int(start)
        __file.close()
        return start
    except Exception, e:
        print '%sA Exception!' % find_startnumber.__name__
        print 'Exception:%s' % e
        return 0


#负责将微博内容抓到本地形成一个文本文件
#此处对之前的代码做一修改，根据搜索得到的结果来进行下一步的抓取活动
#传入的dic对象中有指定微博的博主姓名 微博主页的url 通过这两个参数进行url的访问以及本地文本文件的创建
def Spyder (name,url):
    name = name.encode('utf8')
    filename = "%s.txt" % name
    try:
        filename = unicode(filename,'utf8')
    except Exception,e:
        print '%s0 Exception!' % Spyder.__name__
        print 'Exception:%s' % e
    #打开本地的存储玩野源代码的文件 读取并定位当前抓取到的位置 此处由子模块进行实现 start 即为本次爬虫爬取的起始页面号
    start = find_startnumber(filename)
    maxnumber = find_maxnumber(url)
    #微博页面总页数通过find_maxnumber函数来获取
    print "即将开始爬虫主体工作！"
    _file = open((filename), 'w+')
    try:
        #start web spider
        for count in range(start + 1, maxnumber):
            time.sleep(int(random.random() * 5))
            url_req = url_base + "%s?page=%d" % (url, count)
            req = urllib2.Request(url_req, headers=headers)
            req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
            req.add_header('Connection','keep-alive')
            text = urllib2.urlopen(req).read()
            #regular match
            pattern = re.compile(r'<div class="c"(.+?)<div class="s"></div>')
            string = pattern.findall(text)
            #write in file
            for item in string:
                _file.write(item + '\n')
                #print item
            _file.write('<number>' + str(count) + '</number>' + '\n')
            print '状态输出，第<number>' + str(count) + '</number>次循环.' + '\n'
            #定时刷新浏览器 用于反 反爬虫
            refresh_random()
        print "爬虫工作完毕，共抓取用户:%s微博页面:%d页."%(name,maxnumber)
    except Exception, e:
        print '%sB Exception!' % Spyder.__name__
        print 'Exception:%s'% e
        _file.close()
    finally:
        pass
    _file.close()


#如果查询最大页数的函数正常，返回最后的页数 若不正常 返回一个最大值 直接进行访问的形式获取
def find_maxnumber(url):
    try:
        url_req = url_base + "%s" % url
        req = urllib2.Request(url_req, headers=headers)
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        req.add_header('Connection', 'keep-alive')
        text = urllib2.urlopen(req).read()
        pattern_maxnumber = re.compile(r'value="(\d+?)" /><input type="text" name="page" size="2"')
        number = pattern_maxnumber.findall(text)[0]
        return int(number)
    except Exception,e:
        return 9999


#用于使用浏览器定时刷新weibo登录，防止weibo识别出爬虫行为
#目前只能通过打开浏览器再kill的方式进行
def refresh_random():
    try:
        process = subprocess.Popen('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'% url_base)
        time.sleep(int(random.random())*100)
        process.kill()
    except Exception,e:
        print '%s Exception!' % refresh_random.__name__
        print 'Exception:%s'% e



