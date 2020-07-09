import smtplib
# 负责构造文本
from email.mime.text import MIMEText
# 负责构造图片
from email.mime.multipart import MIMEMultipart
from email.header import Header


class SendEmail:
    def __init__(self, mail_host, mail_sender, mail_license):
        self.__mail_host = mail_host
        self.__mail_sender = mail_sender
        self.__mail_license = mail_license

    # 邮件发送
    def send_email(self, email, code):
        try:
            # 邮件主题
            subject_content = '用户注册，邮箱验证！'
            mm = MIMEMultipart('related')
            mm['From'] = 'Code<' + self.__mail_sender + '>'
            mm['To'] = 'receiver<' + email + '>'
            mm['Subject'] = Header(subject_content, 'utf-8')

            #正文文本
            body_content = '''尊敬的用户您好！
            注册验证码为：{}，请在五分钟内完成注册。
            '''.format(code)
            message_text = MIMEText(body_content, 'plain', 'utf-8')
            mm.attach(message_text)

            mail_receiver = [email]
            # 发送邮件
            stp = smtplib.SMTP()
            stp.connect(self.__mail_host, 25)
            # set_debuglevel(1) 打印SMTP和服务器交互的所有信息
            # stp.set_debuglevel(1)
            stp.login(self.__mail_sender, self.__mail_license)
            stp.sendmail(self.__mail_sender, mail_receiver, mm.as_string())
            data = {'error': 0, 'reason': '邮件发送成功！'}
            return data
        except:
            data = {'error': 1, 'reason': '邮件发送失败！'}
            return data
