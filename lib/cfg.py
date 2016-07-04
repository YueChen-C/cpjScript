#coding=utf8
#配置文件操作

import os

import ConfigParser
cf = ConfigParser.ConfigParser()
#配置文件读写
class cfg():
    def __init__(self,file,name,key):
        '''
        :param file: 文件地址
        :param type: 分类名
        :param key: 字段名
        '''
        self.file=file
        self.type=name
        self.key=key

    def query(self):
        cf.read(self.file)
        content=cf.get(self.type,self.key)
        return content

    def write(self,content):
        '''
        :param content: 写入内容
        :return:
        '''
        cf.set(self.type,self.key,content)
        cf.write(open(self.file,"w"))
        cf.read(self.file)
        text=cf.get(self.type,self.key)
        assert text==str(content)#检查是否写入成功

