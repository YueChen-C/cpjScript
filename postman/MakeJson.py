#coding=utf8
import json,os
from getConfluence import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



header=[{"key": "token","value": "{{token}}","description": ""},{"key": "appversion","value": "{{appversion}}","description": ""}]
postMan={}
postMan['variables']=[]
postMan['info']={}
postMan['info']['name']='大时代接口文档'
postMan['info']['description']=''
postMan['info']['_postman_id']='cc32089d-e271-0688-1985-888d64d39aff'
postMan['info']['schema']='https://schema.getpostman.com/json/collection/v2.0.0/collection.json'
postMan['item']=[]


Confluence1=Confluence()
pagelist= Confluence1.pagelist()
del pagelist[2],pagelist[3],pagelist[3],pagelist[6]
for page in pagelist:
    postModule={}
    postModule['name']=page[1]
    postModule['description']=''
    postModule['item']=[]

    portslist=Confluence1.portslist(page[0]).findAll('a')
    for ports in portslist:
        # ports=portslist[0]
        DetailsName=ports.getText()
        postMItem={}#接口
        postMItem['name']=DetailsName
        postMItem['response']=[]
        postMItem['event']=[{}]
        postMItem['request']={}
        postMItem['event'][0]['listen']='prerequest'
        postMItem['event'][0]['script']={}
        postMItem['event'][0]['script']['type']='text/javascript'
        postModule['item'].append(postMItem)
        Details=Confluence1.gettext(ports.get('href'))
        arr=Details.findAll('table',{'class':'confluenceTable'})
        try:
            url= arr[0].findAll('td')[1].getText()
            method= arr[0].findAll('td')[3].getText().upper()
        except:
            try:
                url =arr[0].findAll('td')[1].getText()
                method =arr[0].findAll('td')[2].getText().upper()
            except:
                method ='GET'

        keytr=arr[1].find('tbody').findAll('tr')
        scriptExec,keys=['/*','*/'],[]
        for i in keytr:
            try:
                key= i.findAll('td')[0].getText()
                keys.append(key)#postMIRFormdata['key']
            except:pass
            scriptExec.insert(-1,i.getText())

        postMItem['event'][0]['script']['exec']=scriptExec
        postMItem['request']['url']='{{url}}/%s'%url
        postMItem['request']['method']=method
        postMItem['request']['header']=header
        postMItem['request']['body']={}
        postMItem['request']['body']['mode']='formdata'
        postMItem['request']['body']['formdata']=[]
        postMItem['request']['description']=''
        if keys:
            for i in keys:
                postMIRFormdata={}
                postMIRFormdata['key']=i
                postMIRFormdata['value']=''
                postMIRFormdata['type']='text'
                postMIRFormdata['enabled']=True
                postMItem['request']['body']['formdata'].append(postMIRFormdata)
    postMan['item'].append(postModule)

jsonStr = json.dumps(postMan,ensure_ascii=False,indent=1,encoding="UTF-8")
filename = os.getcwd()+"/"+"postman.json"
f = open(filename, 'w')
f.write(jsonStr)
f.close()
print jsonStr

