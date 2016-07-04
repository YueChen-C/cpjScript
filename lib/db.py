# coding=utf8
# 数据库操作
import MySQLdb
from lib.httplog import httplog
from config_db import db


class Dict(dict):
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

class create_mysql(object):

    def __init__(self):
        self.connection = None
        self.conn = MySQLdb.connect(host='localhost', user='', passwd='', db='test', charset='utf8')

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


class _Connection():
    def _update(self, sql):
        create = create_mysql()
        cursors = None
        try:
            cursors = create.cursors()
            cursors.execute(sql)
            r = cursors.rowcount
            create.commit()
            return r
        except:
            httplog.log.fatal(sql+'执行失败')
            create.rollback()
        finally:
            cursors.close()

    def _update_many(self, sql, values):
        create = create_mysql()
        cursors = None
        try:
            cursors = create.cursors()
            cursors.executemany(sql, values)
            r = cursors.rowcount
            create.commit()
            return r
        except:
            httplog.log.fatal(sql+'执行失败')
            create.rollback()
        finally:
            cursors.close()

    def _table(self, sql):
        create = create_mysql()
        cursors = None
        try:
            cursors = create.cursors()
            cursors.execute(sql)
            r = cursors.rowcount
            return r
        except:
            httplog.log.fatal(sql+'执行失败')
        finally:
            cursors.close()

    def _select(self, sql):
        cteate = create_mysql()
        cursore = None
        try:
            cursore = cteate.cursors()
            cursore.execute(sql)
            if cursore.description:
                names1 = [x[0] for x in cursore.description]
            return [Dict(names1, x) for x in cursore.fetchall()]
        except:
            httplog.log.fatal(sql+'执行失败')
        finally:
            cursore.close()

def insert(sql):
    return _Connection()._update(sql)


def insert_dict(table, repeat=None, **kw):
    '''
    sql插入字典数据
    :param table: 表名称
    :param kw: 字典格式数据{'a':100,'b':200}
    :param repeat: repeat=1数据去重时必须有唯一键
                   repeat=2重复时覆盖以前数据
                   repeat=3重复时更新数据
    '''
    cols, args = zip(*kw.iteritems())
    if repeat == 1:
        sql = "insert IGNORE into `%s` (%s) values (%s)" % (
        table, ','.join(['`%s`' % i for i in cols]), ','.join(["'%s'" % k for k in args]))
    elif repeat == 2:
        sql = "REPLACE into `%s` (%s) values (%s)" % (
        table, ','.join(['`%s`' % i for i in cols]), ','.join(["'%s'" % k for k in args]))
    elif repeat == 3:
        sql = "insert into `%s` (%s) values (%s) on duplicate key update %s " % (
        table, ','.join(['`%s`' % i for i in cols]), ','.join(["'%s'" % k for k in args]),
        ','.join(["%s" % i + '=values(' + i + ')' for i in cols]))
    else:
        sql = "insert into `%s` (%s) values (%s)" % (
        table, ','.join(['`%s`' % i for i in cols]), ','.join(["'%s'" % k for k in args]))
    return _Connection()._update(sql)


def insert_tuple(table, keys, values, repeat=None):
    '''
    sql批量插入元组数据
    :param table: 表名称
    :param keys: 表字段
    :param values: 元组格式插入内容[(1,2,3),(4,5,6),(7,8,9)]
    :param repeat: repeat=1数据去重时必须有唯一键
                   repeat=2重复时覆盖以前数据
                   repeat=3重复时更新数据
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
    else:
        sql = "INSERT INTO `%s` (%s) VALUES (%s)" % (
        table, (','.join(keys)), (','.join(['%s' for i in range(len(keys))])))
    print sql,values
    return _Connection()._update_many(sql, values)


def insert_one(table, keys, values, repeat=None):
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
        table, (','.join(keys)), (','.join(["'%s'" % i for i in values])))
    elif repeat == 2:
        sql = "REPLACE INTO `%s` (%s) VALUES (%s)" % (table, (','.join(keys)), (','.join(["'%s'" % i for i in values])))
    elif repeat == 3:
        sql = "INSERT INTO `%s` (%s) VALUES (%s) on duplicate key update %s" % (
        table, (','.join(keys)), (','.join(["'%s'" % i for i in values])),
        ','.join(["%s" % i + '=values(' + i + ')' for i in keys]))
    else:
        sql = "INSERT INTO `%s` (%s) VALUES (%s)" % (table, (','.join(keys)), (','.join(["'%s'" % i for i in values])))
    return _Connection()._update(sql)


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
    sql="UPDATE `%s` SET %s WHERE %s;" % (table,text,key)
    return _Connection()._update(table, sql)


def create_table(table, keys):
    '''
    sql创建表
    :param table: 表名称
    :param keys: 创建表字段例如('`passwd` nvarchar(50)','`email` nvarchar(50)'）
    '''
    sql = "create table `%s` (%s)" % (table, (','.join(keys)))
    return _Connection()._table(sql)


def select(sql):
    # sql查询并生成字典
    return _Connection()._select(sql)


def delete(table, key, values):
    '''
    单行删除
    :param table: 表名称
    :param key: 表字段
    :param values: 匹配单个
    '''
    sql = "DELETE FROM `%s` WHERE `%s`=%s" % (table, key, values)
    return _Connection()._select(sql)


def delete_arr(table, key, values):
    '''
    批量删除
    :param table: 表名称
    :param key: 表字段
    :param values: 元组（1,2,3,4）
    '''
    sql = "DELETE FROM `%s` WHERE `%s` IN %s" % (table, key, values)
    return _Connection()._table(sql)

def empty_table(table):
    '''
    :param table: 清空表
    '''
    sql = "TRUNCATE TABLE %s"%table
    return _Connection()._table(sql)

