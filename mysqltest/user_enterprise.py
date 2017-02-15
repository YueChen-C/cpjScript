#coding=utf8

from Clib.Threadhtml import ThreadStartone
from Clib import db
import random,datetime,time,logging
from xpinyin import Pinyin


area='110000,120000,130000,220000,210000,310000,350000,360000,370000,140000,340000,330000,230000,410000,320000,150000,420000,430000,440000,450000,520000,510000,500000,460000,530000,540000,610000,710000,650000,640000,630000,810000,820000,910000,620000'

industry='10,11,12,13,14,15,16,17,18,19,20'
label='1,2,3,4,5,6,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36'
start = time.clock()
text= db.select('SELECT * FROM `project`WHERE id=1')[0]#数据样例
print text



def testmysql():
    content=[]
    for k in range(10):
        for i in range(1000,10000):
            text['id']=None
            text['user_id']=i
            # print text
            content.append(tuple(text.values()))
        # print content
        db.insertTuple(table='project', keys=text.keys(), values=content)

testmysql()
end = time.clock()
print "执行时间: %f s" % (end - start)