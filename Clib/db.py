# coding=utf8
# 数据库操作
import MySQLdb
from Clib.httplog import log
from Clib.config_db import db



class Dict(dict):
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' 没找到 '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

class CreateMysql(object):

    def __init__(self):
        self.connection = None
        self.conn = MySQLdb.connect(host=db['host'], user=db['user'], passwd=db['passwd'], db=db['db'], charset=db['charset'])

    def cursors(self):
        if self.connection is None:
            self.connection = self.conn
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def cleanup(self):
        if self.connection:
            connection = self.connection
            self.connection = None
            connection.close()


class Connection():
    def update(self, sql, *args):
        create = CreateMysql()
        cursors = None
        try:
            cursors = create.cursors()
            cursors.execute(sql,*args)
            r = cursors.rowcount
            create.commit()
            return r
        except Exception:
            log('db').log.exception(sql+u"执行失败")
            create.rollback()
        finally:
            cursors.close()

    def updateMany(self, sql, values):
        create = CreateMysql()
        cursors = None
        try:
            cursors = create.cursors()
            cursors.executemany(sql, values)
            r = cursors.rowcount
            create.commit()
            return r
        except Exception:
            log('db').log.exception(sql+u"执行失败")
            create.rollback()
        finally:
            cursors.close()

    def table(self, sql):
        create = CreateMysql()
        cursors = None
        try:
            cursors = create.cursors()
            cursors.execute(sql)
            r = cursors.rowcount
            return r
        except Exception:
            log('db').log.exception(sql+u"执行失败")
        finally:
            cursors.close()

    def select(self, sql, type=''):
        '''
        :param sql:
        :param type:type=1时，返回字段名
        :return:
        '''
        cteate = CreateMysql()
        cursore = None
        try:
            cursore = cteate.cursors()
            cursore.execute(sql)
            if cursore.description:
                names1 = [x[0] for x in cursore.description]
                if type==1:
                    return names1
                else:
                    return [Dict(names1, x) for x in cursore.fetchall()]
        except Exception:
            log('db').log.exception(sql+u"执行失败")

        finally:
            cursore.close()


def insert(sql,values):
    return Connection().update(sql, values)


def insertDict(table, repeat=None, key=None, **kw):
    '''
    sql插入字典数据
    :param table: 表名称
    :param kw: 字典格式数据{'a':100,'b':200}
    :param repeat: repeat=1数据去重时必须有唯一键
                   repeat=2重复时覆盖以前数据
                   repeat=3重复时更新数据
                   repeat=4多条件去重
    '''
    cols, args = zip(*kw.iteritems())
    if repeat == 1:
        sql = "insert IGNORE into `%s` (%s) values (%s)" % (
        table, ','.join(['`%s`' % i for i in cols]), ','.join(['%s' for i in range(len(args))]))
    elif repeat == 2:
        sql = "REPLACE into `%s` (%s) values (%s)" % (
        table, ','.join(['`%s`' % i for i in cols]), ','.join(['%s' for i in range(len(args))]))
    elif repeat == 3:
        sql = "insert into `%s` (%s) values (%s) on duplicate key update %s " % (
        table, ','.join(['`%s`' % i for i in cols]), ','.join(['%s' for i in range(len(args))]),
        ','.join(["%s" % i + '=values(' + i + ')' for i in cols]))
    elif repeat==4:
        connet=select(key,table)
        if connet:
            key='`id`='+str(connet[0]['id'])
            update(table,kw,key)
            return
        else:
            sql = "insert into `%s` (%s) values (%s)" % (
        table, ','.join(['`%s`' % i for i in cols]), ','.join(['%s' for i in range(len(args))]))
    else:
        sql = "insert into `%s` (%s) values (%s)" % (
        table, ','.join(['`%s`' % i for i in cols]), ','.join(['%s' for i in range(len(args))]))
    return Connection().update(sql, args)


def insertTuple(table, keys, values, key=None, repeat=None):
    '''
    sql批量插入元组数据
    :param table: 表名称
    :param keys: 表字段
    :param values: 元组格式插入内容[(1,2,3),(4,5,6),(7,8,9)]
    :param repeat: repeat=1数据去重时必须有唯一键
                   repeat=2重复时覆盖以前数据
                   repeat=3重复时更新数据
                   repeat=4多条件去重
    '''
    if repeat == 1:
        sql = "INSERT IGNORE INTO `%s` (%s) VALUES (%s)" % (
        table, (','.join(keys)), (','.join(['%s' for i in range(len(keys))])))
    elif repeat == 2:
        sql = "REPLACE INTO `%s` (%s) VALUES (%s)" % (
        table, (','.join(keys)), (','.join(['%s' for i in range(len(keys))])))
    elif repeat == 3:
        sql = "INSERT INTO `%s` (%s) VALUES (%s) on duplicate key update %s " % (
        table, (','.join(keys)), (','.join(['%s' for i in range(len(keys))])),
        ','.join(["%s" % i + '=values(' + i + ')' for i in keys]))
    elif repeat==4:
        if select(key,table):
            return
        else:
            sql = "INSERT INTO `%s` (%s) VALUES (%s)" % (
        table, (','.join(keys)), (','.join(['%s' for i in range(len(keys))])))
    else:
        sql = "INSERT INTO `%s` (%s) VALUES (%s)" % (
        table, (','.join(keys)), (','.join(['%s' for i in range(len(keys))])))
    return Connection().updateMany(sql, values)


def insertOne(table, keys, values, key=None, repeat=None):
    '''
    sql插入单行数据
    :param table: 表名称
    :param keys: 表字段
    :param values: 单行数据
    :param repeat: repeat=1数据去重时必须有唯一键，
                   repeat=2重复时覆盖以前数据
                   repeat=3重复时更新数据
    '''
    if repeat == 1:
        sql = "INSERT IGNORE INTO `%s` (%s) VALUES (%s)" % (
        table, (','.join(keys)), ','.join(['%s' for i in range(len(keys))]))
    elif repeat == 2:
        sql = "REPLACE INTO `%s` (%s) VALUES (%s)" % (table, (','.join(keys)), ','.join(['%s' for i in range(len(keys))]))
    elif repeat == 3:
        sql = "INSERT INTO `%s` (%s) VALUES (%s) on duplicate key update %s" % (
        table, (','.join(keys)), (','.join(['%s' for i in range(len(keys))])),
        ','.join(["%s" % i + '=values(' + i + ')' for i in keys]))
    elif repeat==4:
        if select(key,table):
            return
        else:
            sql = "INSERT INTO `%s` (%s) VALUES (%s)" % (table, (','.join(keys)), ','.join(['%s' for i in range(len(keys))]))
    else:
        sql = "INSERT INTO `%s` (%s) VALUES (%s)" % (table, (','.join(keys)), ','.join(['%s' for i in range(len(keys))]))
    return Connection().update(sql, values)


def update(table, content,key):
    '''
    :param table: 表
    :param content: 字典{'a':100,'b':200,'c':300,'d':'test1'}
    :param key: 更新key '`id`=1'
    :return:
    '''
    text=[]
    for k,v in content.iteritems():
        text.append(('`%s`'%k+'=''\'%s\''%v))
    text=','.join(text)
    sql="UPDATE `%s` SET %s WHERE %s;"%(table,text,key)
    return Connection().update(sql)


def createTable(table, keys):
    '''
    sql创建表
    :param table: 表名称
    :param keys: 创建表字段例如('`passwd` nvarchar(50)','`email` nvarchar(50)'）
    '''
    sql = "create table `%s` (%s)" % (table, (','.join(keys)))
    return Connection().table(sql)


def select(key,table='',type=''):
    '''
    :param content: 多条件字典['id':'1','title':'test']
    :param table: 表名称
    :param type: type=1时查询字段名
    :return:
    '''
    # sql查询并生成字典
    if isinstance(key,dict):
        text=[]
        for k,v in key.iteritems():
            text.append(('`%s`'%k+'=''\'%s\''%v))
        text=' AND '.join(text)

        sql="SELECT * FROM `%s` WHERE %s"%(table,text)
    else:
        sql=key
    return Connection().select(sql, type=type)


def delete(table, key, values):
    '''
    单行删除
    :param table: 表名称
    :param key: 表字段
    :param values: 匹配单个
    '''
    sql = "DELETE FROM `%s` WHERE `%s`=%s" % (table, key, values)
    return Connection().select(sql)


def deleteArr(table, key, values):
    '''
    批量删除
    :param table: 表名称
    :param key: 表字段
    :param values: 元组（1,2,3,4）
    '''
    sql = "DELETE FROM `%s` WHERE `%s` IN %s" % (table, key, values)
    return Connection().table(sql)

def emptyTable(table):
    '''
    :param table: 清空表
    '''
    sql = "TRUNCATE TABLE %s"%table
    return Connection().table(sql)





