#coding:utf-8
import urllib2
import test



url = 'http://weibo.cn/search/mblog?keyword=%E6%9D%8E%E5%BC%80%E5%A4%8D&page=3'
req = urllib2.Request(url, headers=test.headers)
req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
req.add_header('Connection', 'keep-alive')
print urllib2.urlopen(req).read()
