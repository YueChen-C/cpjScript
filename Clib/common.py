#coding=utf8

import os,random,string
from datetime import date,timedelta
def listSplit(num, tied):
    '''平均分组
    :return:[[1, 51], [51, 101], [101, 151], [151, 201]]
    '''
    list=[]
    for i in range(1,num,tied):
        p=[i,i+tied]
        if i+tied>num:
            p=[i,num]
        list.append(p)
    return list


def listAllDict(dict_a, dict_key=None):
    '''遍历所有键
    :param dict_a:
    :param _key: 需要的key值('msg','name')
    :return:
    '''
    keys=[]
    def listDict(dict_a):
        if isinstance(dict_a,dict):
            for x in range(len(dict_a)):
                if dict_key:
                    key= dict_a.keys()[x]
                    value = dict_a[key]
                    for i in dict_key:
                        connet={}
                        if key==i:
                            connet[key]=value
                            keys.append(connet)
                    listDict(value)
                else:
                    key= dict_a.keys()[x]
                    value = dict_a[key]
                    listDict(value)
                    keys.append(key)
            return keys
    return listDict(dict_a)




class getRandom():

    def getDistrictDode(self):
        DC_PATH = os.getcwd()  + "\districtcode.txt"
        with open(DC_PATH) as file:
            data = file.read()
            districtlist = data.split('\n')
        for node in districtlist:
        #print node
            if node[10:11] != ' ':
                state = node[10:].strip()
            if node[10:11]==' 'and node[12:13]!=' ':
                city = node[12:].strip()
            if node[10:11] == ' 'and node[12:13]==' ':
                district = node[14:].strip()
                code = node[0:6]
                codelist.append({"state":state,"city":city,"district":district,"code":code})

    def gennerator(self):
        #随机身份证
        global codelist
        codelist = []
        if not codelist:
            self.getDistrictDode()
        id = codelist[random.randint(0,len(codelist))]['code'] #地区项
        id = id + str(random.randint(1930,2013)) #年份项
        da = date.today()+timedelta(days=random.randint(1,366)) #月份和日期项
        id = id + da.strftime('%m%d')
        id = id+ str(random.randint(100,300))#，顺序号简单处理
        i = 0
        count = 0
        weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2] #权重项
        checkcode ={'0':'1','1':'0','2':'X','3':'9','4':'8','5':'7','6':'6','7':'5','8':'5','9':'3','10':'2'} #校验码映射
        for i in range(0,len(id)):
            count = count +int(id[i])*weight[i]
            id = id + checkcode[str(count%11)] #算出校验码
            return id

    def createPhone(self):
        #手机号
        prelist=["130","131","132","133","134","135","136","137","138","139","147","150","151","152","153","155","156","157","158","159","186","187","188"]
        return random.choice(prelist)+"".join(random.choice("0123456789") for i in range(8))

    def createMail(self):
        #邮箱
        mail=str(''.join(random.sample(string.ascii_lowercase,random.randint(1,20))))+(random.choice(['@qq.com','@163.com','@126.com','@sina.com ','@yahoo.com','@163.net']))
        return mail

    def GB2312(self):
        #随机中文字符
        try:
            Chinese=''
            for i in range(3):
                head = random.randint(0xB0, 0xCF)
                body = random.randint(0xA, 0xF)
                tail = random.randint(0, 0xF)
                val = ( head << 8 ) | (body << 4) | tail
                Chinese += "%x" % val

            return Chinese.decode('hex').decode('gb2312')
        except Exception,E:
            return u"测试"+str(random.randint(1,10000))


print getRandom().createMail()
