#coding=utf8
import json
import re

from Clib import db
from Clib.Threadhtml import Threadstart
from Clib.http import _http


class down():
    def htmljson(self,content):
        pattern = re.compile(r'\[.*\]', re.DOTALL).findall(content)
        htmljson = json.loads("".join(pattern))
        return htmljson

    def accounting(self):
        url='http://www.neeq.com.cn/info/list.do?callback=jQuery18302463568950221321_1467704895415'
        data='keywords=&page=0&pageSize=60&nodeId=131'
        http=_http(data=data)
        text=http.get_data(req_url=url,num=3)
        htmljson=self.htmljson(text)
        content=htmljson[0]['data']['content']
        for i in range(0,len(content)):
            arr={}
            arr['name']=content[i]['title']
            arr['website']=content[i]['linkUrl']
            print arr
            key={'name':arr['name']}
            db.insert_dict(table='lawyers', repeat=4,key=key,**arr)

    def pagenum(self):
        url='http://www.neeq.com.cn/info/list.do?callback=jQuery18302463568950221321_1467704895415'
        data='keywords=&page=2&pageSize=60&nodeId=133'
        http=_http(data=data)
        text=http.get_data(req_url=url,num=3)
        htmljson=self.htmljson(text)
        pagenum=int(htmljson[0]['data']['totalPages'])
        return pagenum


    def law_firm(self,page):
        url='http://www.neeq.com.cn/info/list.do?callback=jQuery18302463568950221321_1467704895415'
        data='keywords=&page=%s&pageSize=60&nodeId=133'%page
        http=_http(data=data)
        text=http.get_data(req_url=url,num=3)
        htmljson=self.htmljson(text)
        content=htmljson[0]['data']['content']
        for i in range(0,len(content)):
            arr={}
            arr['name']=content[i]['title']
            arr['website']=content[i]['linkUrl']
            print arr
            key={'name':arr['name']}
            db.insert_dict(table='lawyers', repeat=4,key=key,**arr)


if __name__ == "__main__":
    down=down()
    pagenum=[i for i in range(1,down.pagenum()+1)]

    down.accounting()
    Threadstart(down.law_firm,pagenum,3)


