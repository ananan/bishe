from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

mail_host = 'smtp.qq.com'
mail_user = '1242670917@qq.com'
mail_pwd = 'jyounnlllnrxhchh'
mail_to = '15917916221@163.com'

msg = MIMEMultipart()

att = MIMEText(open('/home/peter/PycharmProjects/zhihu/answer.html', 'r').read())
att["Content-Type"] = 'application/octet-stream'
att["Content-Disposition"] = 'attachment;filename="zhuxuan_answer.html"'
msg.attach(att)

message = 'attached is the answer from zhihu user zhuxuan, please read it !'
body = MIMEText(message)
msg.attach(body)
msg['To'] = mail_to
msg['from'] = mail_user
msg['subject'] = 'zhihu user zhuxuan answer'

try:
    s = smtplib.SMTP_SSL()
    s.connect(mail_host,'465')
    s.login(mail_user, mail_pwd)

    s.sendmail(mail_user, mail_to, msg.as_string())
    s.close()

    print ('success')
except Exception as e:
    print (e)
