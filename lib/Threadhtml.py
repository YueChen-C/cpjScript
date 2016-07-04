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
            url = self.task.get()
            self.method(url)
            self.task.task_done()

def Threadstart(method,urls,num):
    '''
    :param method:执行函数
    :param urls: urls数组
    :param num: 线程数量
    :return:
    '''
    quene = Queue.Queue()
    for _ in xrange(num):
        t = MyThread(method=method,task=quene)
        t.setDaemon(True)
        t.start()
    # url入队列
    for url in urls:
        quene.put(url)
    quene.join()




