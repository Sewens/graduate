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



def txt_formate(text,fname):
    filename = "f:/%s.txt" % fname
    try:
        filename = unicode(filename, 'utf8')
    except Exception, e:
        print '%s0 Exception!' % txt_formate.__name__
        print 'Exception:%s' % e

    huge_txt = text

    lst = []
    #匹配微博用户发布的微博 区块标志为ctt
    pattern_ctt = re.compile('id=".+"><div><span class="ctt">.+</span>.+<span class="ct">.+</span>')
    for item in pattern_ctt.findall(huge_txt):
        dic = {}
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
    sql_insert(lst,fname)


#新建表以及插入所有被爬到的微博内容
#lst参数为处理完毕的微博内容信息，fname为表名，实际上是搜索过程中获得的用户id信息
def sql_insert(lst,fname):
    fname=unicode(fname,'utf8')
    create_query='create table %s (' \
                 'id int primary key auto_increment,' \
                 'flag varchar(16),' \
                 'ident varchar(16) unique,' \
                 'time datetime,' \
                 'cnt text,' \
                 'agree int,' \
                 'trans int,' \
                 'commit int,' \
                 'sentiment1 float,' \
                 'sentiment2 float)' % fname
    connection = MySQLdb.connect(host='localhost',user='root',passwd='root',db='test',charset='utf8')
    cursor = connection.cursor()
    try :
        cursor.execute(create_query)
    except Exception,e:
        print "%s table create Exception!"  % sql_insert.__name__
        print "Exception:%s" % e

    for item in lst:
        item = dict(item)
        item['cnt'] = item['cnt'].replace('\"','\'')
        insert_query = 'insert into %s (' \
                       'flag,' \
                       'ident,' \
                       'time,' \
                       'cnt,' \
                       'agree,' \
                       'trans,' \
                       'commit,' \
                       'sentiment1,' \
                       'sentiment2' \
                       ') values' \
                '("%s","%s","%s","%s",%d,%d,%d,0,0)'\
                %(fname,item['flag'], item['ident'], item['time'], item['cnt'],int(item['agree']),int(item['trans']),int(item['commit']))
        print insert_query
        try:
            cursor.execute(insert_query)
        except Exception,e:
            print "%s table insert Exception!" % sql_insert.__name__
            print "Exception:%s" % e
    query = 'alter table %s set sentiment1=-1'% fname
    cursor.execute(query)
    connection.commit()
    connection.close()

# sql_query()
#txt_formate()
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

if __name__=='__main__':
    txt_formate('李开复')

