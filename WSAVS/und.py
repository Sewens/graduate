#coding:utf-8
def hanshu(name):
    print name.encode('utf-8')
    print 'name:' + name


str = '中文'
ustr = u'中文'
inpu = raw_input('input chinese')
hanshu(inpu.decode('utf-8'))

