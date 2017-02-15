#coding=utf8
import json
import re

from Clib import db
from Clib.Threadhtml import threadStart
from Clib.http import _Http


class Down():
    def htmlJson(self, content):
        pattern = re.compile(r'\[.*\]', re.DOTALL).findall(content)
        htmljson = json.loads("".join(pattern))
        return htmljson

    def accounting(self):
        url='http://www.neeq.com.cn/info/list.do?callback=jQuery18302463568950221321_1467704895415'
        data='keywords=&page=0&pageSize=60&nodeId=131'
        http=_Http(data=data)
        text=http.getData(req_url=url, num=3)
        htmljson= self.htmlJson(text)
        content=htmljson[0]['data']['content']
        for i in range(0,len(content)):
            arr={}
            arr['name']=content[i]['title']
            arr['website']=content[i]['linkUrl']
            print arr
            key={'name':arr['name']}
            db.insertDict(table='lawyers', repeat=4, key=key)

    def pageNum(self):
        url='http://www.neeq.com.cn/info/list.do?callback=jQuery18302463568950221321_1467704895415'
        data='keywords=&page=2&pageSize=60&nodeId=133'
        http=_Http(data=data)
        text=http.getData(req_url=url, num=3)
        htmljson= self.htmlJson(text)
        pagenum=int(htmljson[0]['data']['totalPages'])
        return pagenum


    def lawFirm(self, page):
        url='http://www.neeq.com.cn/info/list.do?callback=jQuery18302463568950221321_1467704895415'
        data='keywords=&page=%s&pageSize=60&nodeId=133'%page
        http=_Http(data=data)
        text=http.getData(req_url=url, num=3)
        htmljson= self.htmlJson(text)
        content=htmljson[0]['data']['content']
        for i in range(0,len(content)):
            arr={}
            arr['name']=content[i]['title']
            arr['website']=content[i]['linkUrl']
            print arr
            key={'name':arr['name']}
            db.insertDict(table='lawyers', repeat=4, key=key)


if __name__ == "__main__":
    down=Down()
    pagenum=[i for i in range(1, down.pageNum() + 1)]

    down.accounting()
    threadStart(down.lawFirm, pagenum, 3)


