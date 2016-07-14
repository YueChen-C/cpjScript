# -*-coding: utf-8 -*-
#新芽网
from BeautifulSoup import BeautifulSoup
from Clib import db
from Clib.http import _http
from Clib.httplog import log
from Clib.config_db import news

Classify={
    'VC':['http://newseed.pedaily.cn/news/c4210-p',u'引力波'],
    'FT':['http://newseed.pedaily.cn/news/c4093-p',u'访谈'],
    'QS':['http://newseed.pedaily.cn/news/c4092-p',u'趋势'],
    'CY':['http://newseed.pedaily.cn/news/t9-p',u'创业'],
    'RZ':['http://newseed.pedaily.cn/news/t627-p',u'融资'],
    'DJS':['http://newseed.pedaily.cn/news/t4717-p',u'独角兽'],
}






def sorts_list(url,sorts,olddata=''):
    '''
    :param page: 页数
    :param sorts: 分类
    :param olddata: 数据库数据，用于增量
    :return:
    '''
    urlhttp = _http()
    htmlSource = urlhttp.get_data(req_url=url, num=2)
    soup = BeautifulSoup(htmlSource)
    list = []
    title=''
    dateinfo=''
    try:
        ul=soup.find('ul',{"id": "newslist"})
        for i in ul.findAll('li'):

            data = []
            data.append(i.find('div', {"class": "img"}).find('a').get("href"))
            data.append(i.find('div', {"class": "img"}).find('img').get("src"))
            data.append(sorts)
            list.append(data)
            title = i.find('div', {"class": "img"}).find('a').find('img').get("alt")
            dateinfo = i.find('span', {"class": "date"}).getText()
            data.append(dateinfo)

            #增量添加，查询匹配时返回
            if olddata:
                print title,olddata[0]['title'],olddata[0]['release_time'],dateinfo
                if dateinfo < str(olddata[0]['release_time']) or olddata[0]['title'] == title:
                    list.pop(-1)
                    return list, False
        return list, True
    except Exception,E:
        log('http').log.warning(url)
        log('http').log.warning(E)




class mian():
    def __init__(self):
        self.type='0'#全量更新
        self.sorts=['VC','FT','QS','CY','RZ','DJS']#分类
        self.url_tell='newseed.pedaily.cn'#验证域名
        self.olddate='2016-01-01 00:00'
        self.table=news['table']
        self.website=u'新芽'

    def newseed_text(self,list,olddata=''):
        '''
        :param list[req_url,req_url,category]
        '''

        req_url = list[0]
        img_url = list[1]
        category = list[2]
        try:
            arr = {}
            # 获取正文信息
            http = _http()
            htmlSource = http.get_data(req_url=req_url, num=2)
            soup = BeautifulSoup(htmlSource)
            try:
                arr['website'] = u"新芽"
                arr['title'] = soup.find('div', {"class": "col-md-660"}).h1.getText()
                arr['introduction'] = soup.find('div', {"class": "subject"}).getText()
                text = []
                p=soup.find('div', {"class": "pull-left"})
                for i in p.findAll('a'):
                    text.append(i.getText())
                arr['keyword'] = ','.join(text)

                # 时间，来源，作者
                content = soup.find('div', {"class": "info"}).findAll('div')[2].contents
                content = content[2].split(u" ")
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
                arr['category'] = category
                print arr['title']
            except Exception,E:
                log('http').log.warning(req_url)
                log('http').log.warning(E)
                #去重字段
            key={'title':arr['title'],'category':arr['category']}
            db.insert_dict(table=self.table, repeat=4,key=key,**arr)
        except Exception,E:
            log('http').log.warning(E)

    def olddata(self,category):
        '''
        :param website: 网站名称
        :param category: 分类名称
        :return: title，release_time
        '''

        sql="SELECT `title`, `release_time` FROM `%s` WHERE `category` = '%s' and `website`='%s'ORDER BY `release_time` DESC limit 1"%(self.table,category,self.website)
        return db.select(sql)

    def work(self,page,url,sorts,olddata=''):
        try:
            req_url=url+str(page)
            urls, type = sorts_list(req_url,sorts,olddata)
            if olddata:
                for list in urls:
                    urlArr = list[0].split(u"/")
                    if urlArr[2] == self.url_tell:
                        self.newseed_text(list)
            else:
                for list in urls:
                    if list[3] > self.olddate:
                        urlArr = list[0].split(u"/")
                        if urlArr[2] == self.url_tell:
                            self.newseed_text(list)
                    else:
                        return False
            if type == False:
                return False
        except Exception,E:
            log('http').log.warning(E)





if __name__ == "__main__":
    xinya=mian()
    for sort in xinya.sorts:
        url=Classify[sort][0]
        category=Classify[sort][1]
        sqldata=xinya.olddata(category)
        for page in range(1,10):
            if xinya.work(page,url,category,sqldata)==False:
                break




