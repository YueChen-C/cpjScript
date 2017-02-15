# -*- coding: utf-8 -*-
#http数据请求
import urllib2,urllib
import lxml.html as HTML
import json,os,gzip
import cookielib
from random import choice
import time
from Clib.httplog import log
from StringIO import StringIO





class _Http(object):


    def __init__(self,header=None,data=None,proxy=None):
        '''
        :param header: 请求header
        :param data: 请求数据
        :param proxy: 代理列表proxy={'http':'http://some-proxy.com:8080'}
        '''
        self.data=data
        self.proxy=proxy
        if header is None:
            self.header= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
                          'Accept-Language': 'zh-CN,zh;q=0.8'}
        else:
            self.header=header
        #获取cookie
        self.cj = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj),urllib2.HTTPHandler)
        urllib2.install_opener(self.opener)
        #设置代理
        if self.proxy is not None:
            opener = urllib2.build_opener(urllib2.ProxyHandler({choice(self.proxy)}))
            urllib2.install_opener(opener)


    def getReq(self, req_url):
        req = urllib2.Request(url=req_url,data=self.data,headers=self.header)
        content = urllib2.urlopen(req, timeout=5)
        return content

    def getCode(self, req_url):
        statusCode = self.getReq(req_url).getcode()
        return statusCode

    def putReq(self, req_url):
        req = urllib2.Request(url=req_url,data=self.data,headers=self.header)
        req.get_method = lambda:'PUT'
        content = urllib2.urlopen(req, timeout=5)
        return content


    def getHeader(self, req_url, key):
        '''
        :param key: 要取的headers（"set-cookie","Content-Type"）
        :return: {'set-cookie': 'PHPSESSID', 'Content-Type': 'text/html; charset=utf-8'}
        '''
        doc = self.getReq(req_url).info()
        text={}
        for i in key:
            text[i]=doc.getheader(i)
        return text



    def downImage(self,imageUrl,path):
        '''
        :param imageUrl: 文件，图片，mp4等
        :param path: 存储地址
        :return: imageName
        '''
        try:
            isExisist = os.path.exists(path)
            if not isExisist:
                os.makedirs(path)
            urlArr = imageUrl.split(u"/")
            imageName = str(urlArr[len(urlArr)-1])
            local = os.path.join(path,imageName)
            urllib.urlretrieve(imageUrl,local)
            return imageName
        except Exception:
            log('http').log.exception(u'文件下载失败'+imageUrl)


    def getData(self, req_url, num=None, type=None):
        '''
        :param req_url: 要获取的url
        :param num: 重试次数
        :param type: 解析类型1=xpath，2=json
        '''
        try:
            get_req= self.getReq(req_url)
            if get_req.info().get('Content-Encoding') == 'gzip':
                buf = StringIO(get_req.read())
                f = gzip.GzipFile(fileobj=buf)
                content = f.read()
            else:
                content=get_req.read()
            if isinstance(content, unicode):
                pass
            else:
                content = content.decode('utf-8')
            if type==1:
                htmlxpath = HTML.fromstring(content)
                return htmlxpath
            elif type==2:
                str = "".join(content)
                htmljson = json.loads(str)
                return htmljson
            return content
        except Exception:
            if num > 0:
                time.sleep(2)
                return self.getData(req_url=req_url, num=num - 1)
            else:
                log('http').log.exception(u'与服务器连接异常错误链接'+req_url)

