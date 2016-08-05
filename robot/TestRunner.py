# -*- coding:utf-8 -*-


import unittest
import HTMLTestRunner,sys,StringIO,os,time



#测试用例

class MyTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


    def testCase1(self):
        self.assertEqual(2,2,"testError")


    def testCase2(self):
        self.assertEqual(2,3,"testError")


#添加Suite

# def Suite():
#     suiteTest = unittest.TestSuite()
#     suiteTest.addTest(MyTestCase)
#     return suiteTest


if __name__ == '__main__':
    #确定生成报告的路径
    suite=unittest.makeSuite(MyTestCase)
    time1=time.strftime('%Y%m%d',time.localtime(time.time()))
    filePath = os.getcwd()+"/"+time1+"robot.html"
    fp = file(filePath,'wb')

    #生成报告的Title,描述
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='Python Test Report',description='This  is Python  Report')
    runner.run(suite)