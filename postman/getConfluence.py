#coding=utf8
import requests
from BeautifulSoup import BeautifulSoup
import json


class Confluence():
    def __init__(self):
        self.Cookie={'confluence.browse.space.cookie':'space-blogposts','confluence.list.pages.cookie':'list-content-tree','seraph.confluence':'10715152%3A4f84c069ae702034b256cc65d66957af2fb0eac6','mywork.tab.task':'false','JSESSIONID':'C19647D3E581BA4E48C03514E1DFFCD3'}

    def gettext(self,url):
        bd_session = requests.Session()
        text=bd_session.get('http://pms.txcap.com%s'%url,cookies=self.Cookie).text
        soup = BeautifulSoup(text)
        return soup

    def portslist(self,page):
        url='http://pms.txcap.com/plugins/pagetree/naturalchildren.action?decorator=none&excerpt=false&sort=position&reverse=false&disableLinks=false&expandCurrent=true&hasRoot=true&pageId=%s&treeId=0&startDepth=0&mobile=false&treePageId=12125233&_=1487297020773'%page
        bd_session = requests.Session()
        text=bd_session.get(url=url,cookies=self.Cookie).text
        souplist = BeautifulSoup(text)
        return souplist

    def pagelist(self):
        url='http://pms.txcap.com/plugins/pagetree/naturalchildren.action?decorator=none&excerpt=false&sort=position&reverse=false&disableLinks=false&expandCurrent=true&hasRoot=true&pageId=9216089&treeId=0&startDepth=0&mobile=false&ancestors=9216089&treePageId=12125233'
        bd_session = requests.Session()
        text=bd_session.get(url=url,cookies=self.Cookie).text
        soup = BeautifulSoup(text)
        souplist=soup.find(id='child_ul12125233-0')
        pagelist=[]
        for i  in souplist.findAll('a'):
            href=i.get('href')
            if href!=' ':
                pagelist.append([href.split('=')[1],i.getText()])
        return pagelist



