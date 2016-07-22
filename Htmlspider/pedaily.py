# -*-coding: utf-8 -*-
#投资界
import os

from BeautifulSoup import BeautifulSoup
from Clib import db
from Clib.Threadhtml import Threadstart
from Clib.http import _http
from Clib.httplog import log
from Clib.config_db import news



Classify={
    'PE':['http://pe.pedaily.cn/top/handlers/Handler.ashx?action=newslist-all&p=%s&url=http://pe.pedaily.cn/top/newslist.aspx?p=1',u'VC/PE'],
    'TMT':['http://www.pedaily.cn/top/handlers/Handler.ashx?action=newslist-all&p=%s&url=http://www.pedaily.cn/top/newslist.aspx?c=i-tmt/',u'TMT'],
    'XF':['http://www.pedaily.cn/top/handlers/Handler.ashx?action=newslist-all&p=%s&url=http://www.pedaily.cn/top/newslist.aspx?c=i-consume/',u'消费'],
    'YL':['http://www.pedaily.cn/top/handlers/Handler.ashx?action=newslist-all&p=%s&url=http://www.pedaily.cn/top/newslist.aspx?c=i-medical-health/',u'医疗健康']
}


class work():
    def __init__(self):
        self.website=u'投资界'
        self.time='2016-01-01 00:00'


    def pedaily_text(self,list):
        '''
        :param list[req_url,req_url,category]
        '''
        req_url=list[0]
        img_url=list[1]
        if req_url.split('/')[2]=='newseed.pedaily.cn':
            return
        try:
            arr = {}
            # 获取正文信息
            http = _http()
            htmlSource = http.get_data(req_url=req_url, num=2)
            soup = BeautifulSoup(htmlSource)
            try:
                arr['website'] = u"投资界"
                arr['title'] = soup.find('div', {"class": "news-show"}).h1.getText()
                arr['introduction'] = soup.find('div', {"class": "subject"}).getText()
                text = []
                for i in soup.find('div', {"class": "box-l tag"}).contents:
                    text.append(i.getText())
                arr['keyword'] = ','.join(text)

                # 时间，来源，作者
                content = soup.find('div', {"class": "box-l"}).contents
                content = content[3].split(u" ")
                arr['author'] = ''
                arr['source'] = ''
                try:arr['author'] = content[2]
                except:pass
                try:arr['source'] = content[1]
                except:pass

                arr['source_url'] = req_url
                arr['copyright_statement'] = ""
                arr['news_pic'] = img_url
                arr['content'] = u"%s" % soup.find('div', {"class": "news-content"})
                arr['release_time'] = soup.find('span', {"class": "date"}).getText()
                arr['category'] = self.category
                print arr['title']
            except Exception,E:
                log('http').log.warning(req_url)
                log('http').log.warning(E)
            key={'title':arr['title'],'category':arr['category']}
            db.insert_dict(table=news['table'], repeat=4,key=key, **arr)
        except Exception,E:
            log('http').log.warning(E)


    def olddata(self,category):
        sql="SELECT `title`, `release_time` FROM `%s` WHERE `category` = '%s' and `website`='%s'ORDER BY `release_time` DESC limit 1"%(news['table'],category,self.website)
        return db.select(sql)



    def list(self,page,sorts,olddata=''):
        '''
        :param page: 页数
        :param sorts: 分类
        :param olddata: 数据库数据，用于增量
        :return:
        '''
        url=Classify[sorts][0]%page
        print url
        self.category=Classify[sorts][1]
        urlhttp = _http()
        htmlSource = urlhttp.get_data(req_url=url, num=2)
        soup = BeautifulSoup(htmlSource)
        list = []
        title=''
        try:
            for i in soup.findAll('li'):
                data = []
                data.append(i.find('div', {"class": "img"}).find('a').get("href"))
                data.append(i.find('div', {"class": "img"}).find('img').get("src"))
                list.append(data)
                title = i.find('div', {"class": "img"}).find('a').find('img').get("alt")
                time = i.find('span', {"class": "date"}).getText()
                if time<self.time:
                    Threadstart(self.pedaily_text,list,3)
                    return False
                #增量添加，查询匹配时返回
                if olddata:
                    print title,olddata[0]['title']
                    if time < str(olddata[0]['release_time']) or olddata[0]['title'] == title:
                        Threadstart(self.pedaily_text,list,3)
                        return False
            Threadstart(self.pedaily_text,list,5)
        except Exception,E:
            log('http').log.warning(url)
            log('http').log.warning(E)
        return True


if __name__ == "__main__":
    work=work()
    for sorts in Classify:
        olddata=work.olddata(Classify[sorts][1])
        for page in range(1,30):
            if work.list(page,sorts,olddata)==False:
                break
