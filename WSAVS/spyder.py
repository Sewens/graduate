#coding:utf-8
import urllib2
import re
import time
import random
from user_agents import agents
import subprocess
from cookies import *
import extract

#负责将微博内容抓到本地形成一个文本文件
#此处对之前的代码做一修改，根据搜索得到的结果来进行下一步的抓取活动
#传入的dic对象中有指定微博的博主姓名 微博主页的url 通过这两个参数进行url的访问以及本地文本文件的创建
def _spyder (name,url):
    #name = unicode(name,'utf8')
    filename = "f:/%s.txt" % name
    try:
        filename = unicode(filename,'utf8')
    except Exception,e:
        print '%s0 Exception!' % _spyder.__name__
        print 'Exception:%s' % e
    #打开本地的存储玩野源代码的文件 读取并定位当前抓取到的位置
    start = 0
    try:
        __file = open(filename, 'r')
        lis = __file.read()
        re_one = re.compile('<number>\d+</number>')
        num = re_one.findall(lis)
        re_num = re.compile('\d+')
        for every in num:
            temp = int(re_num.findall(every)[0])
            #print 'temp:' + str(temp)
            if (start < temp):
                start = temp
            else:
                pass
        #print int(start)
        __file.close()
    except Exception, e:
        start = 0
        print '%sA Exception!' % _spyder.__name__
        print 'Exception:%s'% e
    finally:
        pass
    #

    _file = open((filename), 'w+')
    try:
        maxnumber = 9999
        #open file
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

            print find_maxnumber(text)

            #write in file
            
            for item in string:
                _file.write(item + '\n')
                #print item
            _file.write('<number>' + str(count) + '</number>' + '\n')
            #print '<number>' + str(count) + '</number>' + '\n'

            #定时刷新浏览器 用于反 反爬虫
            refresh_random()
    except Exception, e:
        print '%sB Exception!' % _spyder.__name__
        print 'Exception:%s'% e
        _file.close()
    finally:
        pass
    _file.close()



def find_maxnumber(txt):
    pattern_maxnumber = re.compile(r'value="(\d+?)" /><input type="text" name="page" size="2"')
    number = pattern_maxnumber.findall(txt)[0]
    return number

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



