# -*-coding:utf-8 -*-
import threading
import Queue,sys,logging

class MyThread(threading.Thread):
    def __init__(self, task,method):

        threading.Thread.__init__(self)
        self.task = task
        self.method = method

    def run(self):
        while True:
            arr = self.task.get()
            self.method(arr)
            self.task.task_done()

def Threadstart(method,arrs,num):
    '''
    :param method:执行函数
    :param arr: arr数组
    :param num: 线程数量
    :return:
    '''
    quene = Queue.Queue()
    for _ in range(num):
        t = MyThread(method=method,task=quene)
        t.setDaemon(True)
        t.start()
        print >> sys.stderr,t
    # url入队列
    for arr in arrs:
        quene.put(arr)
    quene.join()




def Threadstartone(method,num):
    '''
    :param method:执行函数
    :param num: 线程数量
    :return:
    '''
    Threads=[]
    # quene = Queue.Queue()
    for i in range(num):
        t = threading.Thread(target=method, name="T"+str(i))
        t.setDaemon(True)
        Threads.append(t)

    for t in Threads:
        t.start()
        print >> sys.stderr,t

    for t in Threads:
        t.join()
        print >> sys.stderr,t