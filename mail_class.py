#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""this is a class for sendmail"""

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib

class sendMail:
    def __init__(self, user='1242670917@qq.com', passwd='jyounnlllnrxhchh'):
        self._user = user
        self._passwd = passwd
        server = smtplib.SMTP_SSL()
        server.connect('smtp.qq.com','465')
        server.login(self._user, self._passwd)
        self._server = server

    def send_txt_mail(self,to_list,subject,content,subtype):
        '''this is send text mail function
            usage： send_txt_mail(mail_to_list,subject,context,mail_type(html,plain...)
            '''
        msg = MIMEText(content,_subtype=subtype,_charset='utf8')
        msg['Subject'] = subject
        msg['From'] = self._user
        msg['To'] = to_list
        try:
            self._server.sendmail(self._user,to_list,msg.as_string())
            print("sendmail success !")
        except Exception as e:
            print(str(e))
            print("failed to sendmail !!!")

    def send_attach_mail(self,to_list,subject,content,attach_path,filename):
        '''this is a function for send mail with attachments:
            usage: send_attach_mail( to_list,subject,content,attach_path)
            '''
        msg = MIMEMultipart()
        attachs = MIMEText(open((attach_path),'rb').read(),)
        attachs['Content-Type'] = 'application/octet-stream'
        attachs['Content-disposition'] = 'attachment;filename = %s' %filename
        msg.attach(attachs)
        message = content
        body = MIMEText(message)
        msg.attach(body)
        msg['Subject'] = subject
        msg['From'] = self._user
        msg['To'] = ";".join(to_list)
        try:
            self._server.sendmail(self._user,to_list,msg.as_string())
            print("sendmail with attachments success !")
        except Exception as e:
            print(e)

if __name__=="__main__":

    mailto = ['15917916221@163.com','1242670917@qq.com']
    att1 = '/home/peter/PycharmProjects/zhihu/test.py'
    mail = sendMail()
    mail.send_attach_mail(mailto,'this is from peter','nihaoma !',att1)
