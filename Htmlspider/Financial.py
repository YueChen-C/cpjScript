# -*-coding: utf-8 -*-
#财经网
from BeautifulSoup import BeautifulSoup

from Clib import db
from Clib.Threadhtml import threadStart
from Clib.config_db import news
from Clib.http import _Http
from Clib.httplog import log

Classify={
    'ZQYW':['http://stock.caijing.com.cn/stocknews/',u'要闻'],
    'XGPL':['http://stock.caijing.com.cn/xgpl/',u'新股评论'],
    'HGZC':['http://stock.caijing.com.cn/stockeconomy/',u'宏观政策']

}

index={
    'ZQTT':['http://stock.caijing.com.cn/index.html',u'证券头条'],
    'XGTT':['http://stock.caijing.com.cn/newstock/',u'新股头条']
}


class Work():
    def __init__(self):
        self.time=u'2016年01月01日'
        self.website=u'财经网'
        self.table=news['table']

    def olddata(self,category):
        '''
        :param website: 网站名称
        :param category: 分类名称
        :return: title，release_time
        '''

        sql="SELECT `title`, `release_time` FROM `%s` WHERE `category` = '%s' and `website`='%s'ORDER BY `release_time` DESC limit 1"%(self.table,category,self.website)
        return db.select(sql)

    def data(self,url):
        header= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36',
                 'Accept-Language': 'zh-CN,zh;q=0.8',
                 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                 'Host':'stock.caijing.com.cn',
                 'Cookie':'afpCT=1; Hm_lvt_b0bfb2d8ed2ed295c7354d304ad369f1=1468311363; Hm_lpvt_b0bfb2d8ed2ed295c7354d304ad369f1=1468312121; Hm_lvt_3694d7ec09e48181debb3e5b975f1721=1468311364; Hm_lpvt_3694d7ec09e48181debb3e5b975f1721=1468312121; _ga=GA1.3.1640827747.1468311364; _gat=1'}
        http = _Http(header=header)
        htmlSource = http.getData(req_url=url, num=2)
        soup = BeautifulSoup(htmlSource)
        return soup



    def CJtext(self,req_url):
        try:
            soup = self.data(req_url)
            try:
                arr={}
                article=soup.find('div',{"class": "article"})
                arr['website']=u'财经网'
                arr['title']=article.find('h2',{"id": "cont_title"}).getText()
                arr['introduction']=''
                keyword=article.find('div',{"class": "ar_keywords"}).findAll('a')
                text=[]
                for i in keyword:
                    text.append(i.getText())
                arr['keyword']=','.join(text)
                try:
                    arr['author']=article.find('span',{"id": "uthor_baidu"}).getText()
                except:pass
                arr['source']=article.find('span',{"id": "source_baidu"}).getText()
                arr['source_url']=req_url
                arr['copyright_statement']=''
                arr['content']=u"%s" % article.find('div',{"class": "article-content"})
                arr['release_time']=article.find('span',{"id": "pubtime_baidu"}).getText()
                arr['category']=self.category
                print arr['title']
                #去重字段
                key={'title':arr['title'],'category':arr['category']}
                db.insertDict(table=self.table, repeat=4, key=key)
            except Exception:
                log('http',req_url + u'财经网')
        except Exception:
                log('http',req_url + u'财经网')


    def index(self,url,category):
        self.category=category
        soup=self.data(url)
        head=soup.find('div',{"class": "yaow_cont"}).findAll('a')
        for i in head:
            url=i.get('href')
            self.CJtext(url)


    def list(self,sorts,page,olddata=''):
        url=Classify[sorts][0]+str(page)+'.shtml'
        print url
        self.category=Classify[sorts][1]
        soup=self.data(url)
        head=soup.find('ul',{"class": "list"}).findAll('li')
        urlarr=[]
        for i in head:
            urlarr.append(i.find('a').get('href'))
            time=i.find('div',{"class": "time"}).getText()
            title=i.find('a').getText()
            if time<self.time:
                threadStart(self.CJtext, urlarr, 3)
                return False
            #数据库增量判断
            if olddata:
                print title,olddata[0]['title'],olddata[0]['release_time'],time
                if time < str(olddata[0]['release_time']) or olddata[0]['title'] == title:
                    threadStart(self.CJtext, urlarr, 3)
                    return False
        threadStart(self.CJtext, urlarr, 5)



if __name__ == "__main__":
    work=Work()
    # #新股头条
    work.index(index['XGTT'][0],index['XGTT'][1])
    # #证券头条
    work.index(index['ZQTT'][0],index['ZQTT'][1])

    for sorts in Classify:
        olddata=work.olddata(Classify[sorts][1])
        for i in range(1,30):
            if work.list(sorts,i,olddata)==False:
                break

