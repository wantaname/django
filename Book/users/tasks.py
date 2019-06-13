from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

@shared_task
def send_active_email(token, email):
    '''发送激活邮件'''
    subject = '图灵书城用户激活' # 标题
    message = ''
    sender = settings.EMAIL_FROM # 发件人
    receiver = [email] # 收件人列表
    html_message = '点击下方链接激活您的账户：<br /><a href="http://www.37ys.top/user/active/%s/">http://www.37ys.top/user/active/</a>'%token
    send_mail(subject, message, sender, receiver, html_message=html_message)
