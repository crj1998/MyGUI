import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

def sEmail(theme='TEST',content='IGNORE ME'):
    s='2088737914@qq.com'
    pw='oitecwcidermeiid'
    r='3257575985@qq.com'
    msg=MIMEText(content,'plain','utf-8')
    msg['From']=formataddr(['Py_Robot',s])      
    msg['To']=formataddr(['User',r])
    msg['Subject']=theme
    try:
        smtp='smtp.'+s.split('@')[-1]
        server=smtplib.SMTP_SSL(smtp,465)
        server.login(s,pw)
        server.sendmail(s,[r,],msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return False

if __name__ == '__main__':
    if sendEmail():
        print("邮件发送成功")
    else:
        print("邮件发送失败")