#coding=utf8
#配置文件操作

import os

import ConfigParser
cf = ConfigParser.ConfigParser()
#配置文件读写
class cfg():
    def __init__(self,file,name,):
        '''
        :param file: 文件地址
        :param type: 分类名
        :param key: 字段名
        '''
        self.file=file
        self.type=name


    def query(self,key):
        cf.read(self.file)
        content=cf.get(self.type,key)
        return content

    def write(self,key,content):
        '''
        :param content: 写入内容
        :return:
        '''
        cf.set(self.type,key,content)
        cf.write(open(self.file,"w"))
        cf.read(self.file)
        text=cf.get(self.type,key)
        assert text==str(content)#检查是否写入成功

