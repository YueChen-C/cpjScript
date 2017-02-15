# -*-coding: utf-8 -*-
#财经网金融
from BeautifulSoup import BeautifulSoup
from Clib import db
from Clib.http import _Http
from Clib.Threadhtml import threadStart
from Clib.config_db import news
from Clib.httplog import log

class Work():
    def __init__(self):
        self.table=news['table']

    def data(self,url):
        header= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20101101 Firefox/47.0',
                 'Accept-Language': 'zh-CN,zh;q=0.8'}
        http = _Http(header=header)
        htmlSource = http.getData(req_url=url, num=3)
        soup = BeautifulSoup(htmlSource)
        return soup




    def CJtext(self,req_url):
        try:
            urlsplit=req_url.split('/')
            if urlsplit[2] and urlsplit[2]=='finance.caijing.com.cn':
                    soup=self.data(req_url)
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
                        try:arr['author']=article.find('span',{"id": "uthor_baidu"}).getText()
                        except:pass
                        arr['source']=article.find('span',{"id": "source_baidu"}).getText()
                        arr['source_url']=req_url
                        arr['copyright_statement']=''
                        arr['content']=u"%s" % article.find('div',{"class": "article-content"})
                        arr['release_time']=article.find('span',{"id": "pubtime_baidu"}).getText()
                        arr['category']=u'金融'
                        print arr['title']
                        #去重字段
                        key={'title':arr['title'],'category':arr['category']}
                        db.insertDict(table=self.table, repeat=4, key=key)
                    except Exception:
                        log('db').log.exception(req_url+u'财经网金融')
            else:
                return False
        except Exception:
                log('http').log.exception(req_url+u'财经网金融')



    def index(self):
        url='http://finance.caijing.com.cn/index.html'
        soup=self.data(url)

        url=soup.findAll('a',{"target": "_blank"})
        urlarr=[]
        for i in url:
            urlarr.append(i.get('href'))
        return urlarr


if __name__ == "__main__":
    work=Work()
    urlarr=work.index()
    threadStart(work.CJtext, urlarr, 5)


