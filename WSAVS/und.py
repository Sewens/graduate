#coding:utf-8
import Extract


lst = Extract.Extract('林鸿飞')
count = 1
for item in lst:
    if count>10:
        break
    print item['name'],type(item['name']),len(item['name'])
    print item['name'],isinstance(item['name'],str),item['name'].decode('utf-8'),type(item['name'].decode('utf-8'))

    p = '("%s", "%s", "%s", "%s", %d, %d, %d, 0, 0, % s)'% \
        (item['flag'], item['ident'], item['time'], item['cnt'], int(item['agree']), int(item['trans']),
       int(item['commit']),item['name'].decode('utf-8'))
    print p


