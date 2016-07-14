# -*-coding:utf-8 -*-
import threading
import Queue

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
    for _ in xrange(num):
        t = MyThread(method=method,task=quene)
        t.setDaemon(True)
        t.start()
    # url入队列
    for arr in arrs:
        quene.put(arr)
    quene.join()





