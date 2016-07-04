#coding=utf8
from lib.http import _http
from lib.Threadhtml import Threadstart
import os
import json
from lib.cfg import cfg
from lib.httplog import httplog


class Mangaerurl(object):
    '''
    获取所有列表url
    '''
    def __init__(self):
        self.header = {
        'Host': "gs.amac.org.cn",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Accept-Language': "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        'Accept-Encoding': "gzip, deflate",
        'Content-Type': "application/json",
        'X-Requested-With': "XMLHttpRequest",
        'Referer': "http://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html"
        }
        self.data=json.dumps({})
        self.http=_http(header=self.header,data=self.data)

    def fand_num(self):
        url = "http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.3600165833785517&page=5&size=100"
        getnum = self.http.get_data(req_url=url, num=3,type=2)
        return getnum['totalPages']

    def fand_url(self,page):
        '''
        :param num:页数
        :return:url数组
        '''
        url="http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.3600165833785517&page="+str(page)+"&size=100"
        geturl=self.http.get_data(req_url=url,num=3,type=2)
        url=[]
        for i in range(0,len(geturl['content'])):
            url.append("http://gs.amac.org.cn/amac-infodisc/res/pof/manager/"+geturl['content'][i]['url'])
        return url

def Mangerdata(req_url):
    HttpManger=_http()
    try:
        data=HttpManger.get_data(req_url=req_url,num=3,type=1)
        #基本信息
        NameCN=data.find(".//*[@id='foot1']").text#中文
        for p in data.xpath('/html/body/div[1]/div[2]/div/table/tbody'):
            NameEN=p.find("tr[4]/td[2]").text#英文
            code=p.find("tr[5]/td[2]").text#登记编号
            number=p.find("tr[6]/td[2]").text#英文


        #q其他信息
        for p in data.xpath('/html/body/div[1]/div[2]/div/table/tbody'):
                Name=p.find("tr[17]/td[2]").text
                ability=p.find("tr[18]/td[2]").text
                mode=p.find("tr[18]/td[4]").text

        Resume=[]#履历
        for i in data.xpath('/html/body/div[1]/div[2]/div/table/tbody/tr[19]/td[2]/table[1]/tbody'):
            for k in range(1,len(i)+1):
                text=i.find("tr["+str(k)+"]/td[1]").text
                Resume.append("".join(text.split()))
                Resume.append(i.find("tr["+str(k)+"]/td[2]").text)
                Resume.append(i.find("tr["+str(k)+"]/td[3]").text)

        Position=[]#情况
        for i in data.xpath('/html/body/div[1]/div[2]/div/table/tbody/tr[20]/td[2]/table[1]/tbody'):
            for k in range(1,len(i)+1):
                Position.append(i.find("tr["+str(k)+"]/td[1]").text)
                Position.append(i.find("tr["+str(k)+"]/td[2]").text)
                text1=i.find("tr["+str(k)+"]/td[3]").text
                Position.append("".join(text1.split()))
        print Position
    except Exception,e:
        httplog.log.warning(u'与服务器连接异常,链接:'+req_url)
        httplog.log.warning(e)


if __name__ == "__main__":
    Mangaer=Mangaerurl()
    num=Mangaer.fand_num()
    path=os.getcwd()+"\config.cfg"
    key=cfg(file=path,name='manager',key='page')
    page=None
    #判断全量还是增量
    if key.query()=='0':
        try:
            for page in range(1,num+1):
                urls= Mangaer.fand_url(page)
                Threadstart(method=Mangerdata,urls=urls,num=10)
        finally:
            key.write(page)
    else:
        try:
            for page in range(int(key.query()),num+1):
                urls= Mangaer.fand_url(page)
                Threadstart(method=Mangerdata,urls=urls,num=10)
        finally:
            key.write(page)
