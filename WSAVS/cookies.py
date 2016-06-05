#coding:utf-8
import os
from UserAgents import *
import random

url_base = 'http://weibo.cn'

cookie = '_T_WM=63dff67cb599430958f0855675a0b97d; ' \
         'SUB=_2A256QsVkDeRxGeVM7FQT9ynJyT6IHXVZzOssrDV6PUJbstBeLRbDkW1LHeuig34OeeH2V3xJt8V3S7tWxs_6CA..;' \
         ' SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhmuP4Ef-Gwl4bzviKJL7hk5JpX5o2p5NHD95Q0eoMceoMNSKzEWs4DqcjT-cSaMrWDdfvlHXYt;' \
         ' SUHB=0ftpyZaR6RS8dC; SSOLoginState=1464251701; gsid_CTandWM=4u7JCpOz5GcBFv1je6TxcdKjb8q'

headers = {
    'User-Agent': random.choice(agents),
    'cookie':cookie
}
#设置最新的cookies值保证能够正常访问微博帐号
def set_cookies():
    print "请将当前登录微博帐号的Cookies填入打开的文本文件中，保存并退出以更新Cookies"
    op = os.popen('notepad cookies.txt')
    print '执行结果:'
    for line in op:
        print op
    print "消息输出完毕"


#该函数将全局变量cookies设置（更新）为用户填入文本文件中的最新的cookies值
def get_cookies():
    _file = open('cookies.txt','r')
    cookies = _file.read()
    if cookies=='':
        _file.close()
        return 0
    _file.close()
