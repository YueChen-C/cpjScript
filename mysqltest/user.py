#coding=utf8
#user表填充

from Clib.Threadhtml import Threadstartone
from Clib import db
import random,datetime,time,logging
from xpinyin import Pinyin
start = time.clock()
text= db.select('SELECT * FROM `user`WHERE id=1')[0]#数据样例
print text.keys()
print text
pinyin=Pinyin()
def GB2312():
    #随机中文
    try:
        Chinese=''
        for i in range(random.randint(2,6)):
            head = random.randint(0xB0, 0xCF)
            body = random.randint(0xA, 0xF)
            tail = random.randint(0, 0xF)
            val = ( head << 8 ) | (body << 4) | tail
            Chinese += "%x" % val

        return Chinese.decode('hex').decode('gb2312')
    except Exception,E:
        return text['name']+str(random.randint(1,10000))



def testmysql():
    for k in range(20):
        content=[]
        for i in range(5000):
            text['id']=None
            text['email']=str(random.randint(1,999999999))+(random.choice(['@qq.com','@163.com','@126.com','@sina.com ','@yahoo.com','@163.net']))
            text['phone']=str(random.randint(10000000000,19999999999))
            text['gender']=random.randint(1,2)
            name=GB2312()
            text['name']=name
            text['name_spelling']=pinyin.get_pinyin(name)
            text['first_char']=pinyin.get_initials(name)[0]
            text['created_at']=datetime.datetime.now()
            content.append(tuple(text.values()))
        db.insert_tuple(table='user',keys=text.keys(),values=content)
Threadstartone(testmysql,num=5)
end = time.clock()
print "执行时间: %f s" % (end - start)