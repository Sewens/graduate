# coding:utf-8
import re
import MySQLdb
import SentimentAnalyzer


# 用来进行两种格式的日期的匹配
def time_match(item):
    pattern_time1 = re.compile('\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}')
    pattern_time2 = re.compile('(\d{2})月(\d{2})日\s(\d{2}:\d{2})')
    time = pattern_time2.findall(item)
    if len(time) != 0:
        rt_time = '2016-%s-%s %s:00' % (time[0][0], time[0][1], time[0][2])
        return rt_time

    else:
        time = pattern_time1.findall(item)
        if len(time) != 0:
            rt_time = time[0]
            return rt_time
        else:
            return ''


#标签为ctt的是用户自己发布的微博
def ctt_match(item):
    pattern_content = re.compile('<span class="ctt">(.+)</span>')
    cnt = pattern_content.findall(item)
    return cnt[0]

#标签名称为cmt的表示是当前转发的微博
'''#用于匹配转发内容，暂时不用了
def cmt_match(item):
    pattern_content = re.compile('<span class="cmt">(.+)</span>')
    cnt = pattern_content.findall(item)
    return cnt[0]
'''
def ident_match(item):
    pattern_id = re.compile(r'id="(.+)"><div>')
    id = pattern_id.findall(item)
    return id[0]


def agree_match(item):
    try:
        pattern_content = re.compile('赞\[(\d+)\]')
        cnt = pattern_content.findall(item)
        return cnt[0]
    except Exception,e:
        return 0


def trans_match(item):
    try:
        pattern_content = re.compile('转发\[(\d+)\]')
        cnt = pattern_content.findall(item)
        return cnt[0]
    except Exception, e:
        return 0

def commit_match(item):
    try:
        pattern_content = re.compile('评论\[(\d+)\]')
        cnt = pattern_content.findall(item)
        return cnt[0]
    except Exception, e:
        return 0




# 用来将爬虫爬取的有效内容提取出来


#还是原有的功能，用于打开本地的文件进行分析 最后返回一个lst 相应的需要带上用户的微博id信息
def txt_formate(name):
    name = name.encode('utf-8')
    filename = "%s.txt" % name
    try:
        filename = unicode(filename, 'utf8')
    except Exception, e:
        print '%s0 Exception!' % txt_formate.__name__
        print 'Exception:%s' % e
    _file = open(filename)
    huge_txt = _file.read()
    _file.close()
    lst = []
    #匹配微博用户发布的微博 区块标志为ctt
    pattern_ctt = re.compile('id=".+"><div><span class="ctt">.+</span>.+<span class="ct">.+</span>')
    for item in pattern_ctt.findall(huge_txt):
        dic = {'name':name}
        cnt = ctt_match(item)
        dic['flag'] = 'ctt'
        dic['ident'] = ident_match(item)
        dic['time'] = time_match(item)
        dic['cnt'] = unicode(cnt, 'utf-8')
        dic['agree'] = agree_match(item)
        dic['trans'] = trans_match(item)
        dic['commit'] = commit_match(item)
        lst.append(dic)
    #匹配微博用户转发的微博 其区块标志为cmt
    '''#该部分是匹配转发信息的部分，需要再仔细分析div块的属性之类的 暂时不用了
    pattern_cmt = re.compile(r'id=".+"><div><span class="cmt">.+</a></span>')
    for item in pattern_cmt.findall(huge_txt):
        dic = {}
        cnt = ctt_match(item)
        dic['cnt'] = unicode(cnt, 'utf-8')
        dic['flag'] = 'cmt'
        dic['id'] = id_match(item)
        dic['time'] = time_match(item)
        dic['agree'] = agree_match(item)
        dic['trans'] = trans_match(item)
        dic['commit'] = commit_match(item)
        lst.append(dic)
    '''
    return lst


'''
if __name__=="__main__":
    analyser = SentimentAnalyzer.SentimentAnalyzer()
    analyser.load()
    connection = MySQLdb.connect(host='localhost',user='root',passwd='root',db='test1',charset='utf8')
    cursor = connection.cursor()
    select_query = 'select * from kaifulee'
    cursor.execute(select_query)
    content = cursor.fetchall()
    count = 0
    for item in content:
        count += 1
        senti = analyser.analyze(item[2])
        query = "update kaifulee set sentiment1 = %f where id = '%s'" %(senti,item[0])
        cursor.execute(query)
        print count
    connection.commit()
    connection.close()
'''



