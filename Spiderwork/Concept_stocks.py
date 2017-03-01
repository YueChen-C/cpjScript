# -*-coding: utf-8 -*-
import re

from Clib import db
from Clib.Threadhtml import threadStart
from Clib.http import _Http
from Clib.httplog import log


class Concept():
    def __init__(self):
        self.datalist=self.Concepttype()

    def Concepttype(self):
        text=[]
        transition=[]
        req_url = 'http://www.ipo3.com/strategy-category.html'
        http=_Http()
        htmlSource = http.getData(req_url=req_url, num=5)
        for i in range(1,9):
            for p in htmlSource.xpath('.//*[@id="section"]/div/div[2]/div/div['+str(i)+']/ul'):
                for j in xrange(1,len(p)+1):
                    c=p.xpath('li['+str(j)+']/a/@href')
                    transition.append(''.join(c))
                    text.append(p.find('li['+str(j)+']/a/div/span[2]').text)
        return dict(zip(text,transition))


    def Conceptlist(self,url):
        type=None
        connet=self.datalist
        for key in connet:
            if connet[key]==url:
                type=key
                break
        req_url='http://www.ipo3.com'+url
        http=_Http()
        try:
            htmlSource = http.getData(req_url=req_url, num=5)
            text=[]
            for p in htmlSource.xpath('.//*[@id="section"]/div/div[2]/table'):
                for j in range(2,len(p)+1):
                    connet=[]
                    connet.append(p.find('tr['+str(j)+']/td[1]/p[1]').text)#名字
                    code=p.find('tr['+str(j)+']/td[1]/p[2]').text#股票代码
                    connet.append(''.join(re.compile(r'\d+').findall(code)))
                    connet.append(p.find('tr['+str(j)+']/td[2]').text)#地区
                    connet.append(p.find('tr['+str(j)+']/td[3]').text)#主板劵商
                    connet.append(p.find('tr['+str(j)+']/td[4]').text)#转换类型
                    connet.append(p.find('tr['+str(j)+']/td[5]/p').text)#行业
                    connet.append(type)
                    text.append(tuple(connet))
                key=('name','stokcode','region','business','transition_type','industry','type')
                db.insertTuple('Concept_stoks', key, text, repeat=1)
        except Exception,e:
            log('http',u'与服务器连接异常,链接:' + req_url)

if __name__ == "__main__":
    Concept=Concept()
    url = (Concept.datalist).values()
    threadStart(method=Concept.Conceptlist, arrs=url, num=10)
