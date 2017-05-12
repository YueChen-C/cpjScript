#coding=utf8

import sys,os
import requests
from BeautifulSoup import BeautifulSoup
import json
reload(sys)
sys.setdefaultencoding('utf-8')


postman={
    "h": {
        "appToken": "{{appToken}}",
        "device": "{{device}}",
        "deviceId": "{{deviceId}}",
        "group": '',
        "method": '',
        "siteId": "{{siteId}}",
        "siteVersion": "{{siteVersion}}",
        "ticket": "{{ticket}}",
        "version": "{{version}}"
    },
    "b": {}
}
url='{{url}}/platform-rest/service.jws'



class Confluence():
    def __init__(self):
        self.Cookie={'confluence.browse.space.cookie':'space-blogposts','confluence.list.pages.cookie':'list-content-tree','seraph.confluence':'10715152%3A4f84c069ae702034b256cc65d66957af2fb0eac6','mywork.tab.task':'false','JSESSIONID':'AD502645A17067DD3A15808AEB2A7F81'}
        self.Modular={}

    def gettext(self,page):
        url="http://pms.txcap.com/pages/viewpage.action?pageId=%s"%page
        print url
        bd_session = requests.Session()
        text=bd_session.get(url=url,cookies=self.Cookie).text
        soup = BeautifulSoup(text)
        return soup

    def pagelist(self,pagearr):
        souplists=[]
        for page in pagearr:
            url='http://pms.txcap.com/plugins/pagetree/naturalchildren.action?decorator=none&excerpt=false&sort=position&reverse=false&disableLinks=false&expandCurrent=true&hasRoot=true&pageId=%s&treeId=0&startDepth=0&mobile=false&treePageId=12125233&_=1487297020773'%page[0]
            bd_session = requests.Session()
            text=bd_session.get(url=url,cookies=self.Cookie).text
            soup = BeautifulSoup(text)
            arr=soup.findAll('span',{'class':"plugin_pagetree_children_span"})

            if arr:
                self.Modular[page[1]]=[]
                for i in arr:
                    souplists.append((i.find('a').get('href').split('=')[1],i.getText()))
                    self.Modular[page[1]].append(i.find('a').get('href').split('=')[1])
        if souplists:
            return self.pagelist(souplists)
        else:
            return self.Modular



header=[]
postMan={}
postMan['variables']=[]
postMan['info']={}
postMan['info']['name']='大时代接口文档'
postMan['info']['description']=''
postMan['info']['_postman_id']='cc32089d-e271-0688-1985-888d64d39aff'
postMan['info']['schema']='https://schema.getpostman.com/json/collection/v2.0.0/collection.json'
postMan['item']=[]
#
#
Confluence1=Confluence()
pagelist= Confluence1.pagelist([('12126514',u'大时代接口文档-v1.0')])
# pagelist={u'\u6211\u7684\u6536\u85cfV1.0': [u'12128168', u'12128166', u'12128176'], u'\u76f4\u64ad\u6211\u7684': [u'12127631', u'12126943', u'12127069', u'12126981', u'12127097', u'12126891', u'12126847'], u'\u5165\u4f4f\u673a\u6784V1.0': [u'12128233', u'12128235', u'12128237', u'12128103', u'12128101', u'12128021', u'12128024'], u'\u76f4\u64ad\u6392\u884c': [u'12126955', u'12127000', u'12126898'], u'APP\u9996\u9875V1.0': [u'12127751', u'12127754', u'12128059', u'12128173', u'12128084'], u'\u76f4\u64ad\u7533\u8bf7': [u'12127227', u'12127703', u'12127623', u'12127151'], u'\u76f4\u64ad\u56de\u653e': [u'12128140', u'12127329', u'12127025'], u'_2.\u5e38\u89c1\u7f16\u7801': [u'12128156', u'12128159', u'12128161'], u'\u767b\u5f55\u6a21\u5757V1.0': [u'12127498', u'12127515'], u'\u4ea7\u54c1\u6a21\u5757v1.0': [u'12127810', u'12127325', u'12127808', u'12127821', u'12128006', u'12128012'], u'\u5df2\u53d1\u5e03\u4fe1\u606fV1.0': [u'12128135', u'12128087', u'12128137'], u'\u76f4\u64ad\u6a21\u5757V1.0': [u'12126769', u'12126777', u'12127635', u'12127549', u'12126762', u'12126771', u'12126773', u'12126765', u'12126767', u'12126758'], u'\u6211\u7684\u9884\u7ea6V1.0': [u'12128056', u'12128044', u'12128049'], u'\u76f4\u64ad\u4fe1\u606f': [u'12127273', u'12127278', u'12127374', u'12127379', u'12127357', u'12127300', u'12127294', u'12127332', u'12127365', u'12127368'], u'\u76f4\u64ad\u9996\u9875': [u'12127158', u'12127846', u'12127165'], u'\u76f4\u64ad\u9884\u544a': [u'12127446', u'12127254', u'12127626', u'12127312', u'12127264'], u'\u76f4\u64ad\u641c\u7d22': [u'12127234'], u'app\u542f\u52a8\u63a5\u53e3': [u'12127784'], u'\u76f4\u64ad\u5206\u4eab': [u'12127637'], u'\u8c03\u67e5\u95ee\u5377\u6a21\u5757V1.0': [u'12127426', u'12127424', u'12127419'], u'\u7528\u6237\u6a21\u5757V1.0': [u'12127772', u'12127779', u'12127777', u'12128276'], u'\u9879\u76ee\u6a21\u5757V1.0': [u'12127987', u'12127999', u'12128105', u'12127473', u'12127864', u'12128107', u'12127871', u'12127750'], u'\u76f4\u64ad\u4e2a\u4eba\u4e3b\u9875': [u'12127611', u'12127591', u'12127600', u'12127606'], u'\u5927\u65f6\u4ee3\u63a5\u53e3\u6587\u6863-v1.0': [u'12128145', u'12128151', u'12127781', u'12127744', u'12127323', u'12128019', u'12128079', u'12128058', u'12128163', u'12128033', u'12127494', u'12127582', u'12127491', u'12126756', u'12127502', u'12127469'], u'\u6ce8\u518c\u6a21\u5757V1.0': [u'12127577', u'12127565'], u'\u6211\u7684\u6295\u9012V1.0': [u'12128077', u'12128068', u'12128075']}
pagelist.pop(u'大时代接口文档-v1.0')
pagelist.pop(u'直播模块V1.0')
for pagename in pagelist:
    postModule={}
    postModule['name']=pagename
    postModule['description']=''
    postModule['item']=[]
    for page in pagelist[pagename]:
        print page
        soup= Confluence1.gettext(page=page)
        scriptExec=['/*','*/']
        postman['b']={}
        for i in soup.findAll('div',{'class':'table-wrap'}):

            if u'负责人' in i.getText():
                keys=i.findAll('td',{'class':'confluenceTd'})
                postman['h']['group']=keys[1].getText()
                method=keys[2].getText()
                if method.encode( 'UTF-8' ).replace('_', '').isalpha():
                    postman['h']['method']=method
                else:
                    postman['h']['method']=keys[3].getText()

            if u'是否必传' in i.getText():
                try:
                    keytr=i.find('tbody').findAll('tr')
                    for k in keytr:
                        key= k.findAll('td')[0].getText()
                        postman['b'][key]= k.findAll('td')[1].getText()
                    scriptExec.insert(-1,i.getText())
                except:
                    pass
            else:continue
            break
        postMItem={}#接口
        postMItem['name']=soup.find(id='title-text').getText()
        postMItem['response']=[]
        postMItem['event']=[{}]
        postMItem['request']={}
        postMItem['event'][0]['listen']='prerequest'
        postMItem['event'][0]['script']={}
        postMItem['event'][0]['script']['type']='text/javascript'
        postModule['item'].append(postMItem)
        postMItem['event'][0]['script']['exec']=scriptExec
        postMItem['request']['url']=url
        postMItem['request']['method']='POST'
        postMItem['request']['header']=header
        postMItem['request']['body']={}
        postMItem['request']['body']['mode']='raw'
        postMItem['request']['description']=''
        postmanjson=json.dumps(postman,ensure_ascii=False,indent=1,encoding="UTF-8")
        postMItem['request']['body']['raw']='%s'%postmanjson
    postMan['item'].append(postModule)

jsonStr = json.dumps(postMan,ensure_ascii=False,indent=1,encoding="UTF-8")
print jsonStr
filename = os.getcwd()+"/"+"postmanV1.json"
f = open(filename, 'w')
f.write(jsonStr)
f.close()