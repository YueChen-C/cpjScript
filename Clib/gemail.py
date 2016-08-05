#coding:utf8
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText


class mail():
    def __init__(self,title,text,to_mail):
        '''
        :param title: 邮件头
        :param text: 正文
        :param to_mail: 发送数组
        :return:
        '''
        self.mail_subject=title
        self.mail_text=text
        self.to_mail=to_mail
        self.mail_info = {
            "from": "549042238@qq.com",
            "to": "cpjsf@163.com",
            "hostname": "smtp.qq.com",
            "username": "549042238@qq.com",
            "password": "sltmzzibhdxcbcij",
            "mail_encoding": "utf-8"
        }

    def MailMin(self):
            smtp = SMTP_SSL(self.mail_info["hostname"])
            smtp.set_debuglevel(1)
            smtp.ehlo(self.mail_info["hostname"])
            smtp.login(self.mail_info["username"], self.mail_info["password"])
            msg = MIMEText(self.mail_text, "plain", self.mail_info["mail_encoding"])
            msg["Subject"] = Header(self.mail_subject,self. mail_info["mail_encoding"])
            msg["from"] =self. mail_info["from"]
            msg["to"] =','.join(self.to_mail)
            smtp.sendmail(self.mail_info["from"], self.to_mail, msg.as_string())
            smtp.quit()

