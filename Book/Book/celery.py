'''
创建celery的一个实例，供其他模块导入
'''
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

#设置celery默认的django设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Book.settings')
#创建一个celery实例
app=Celery('Book',broker='redis://127.0.0.1:6379/2')
#用来加载configuration对象中的配置文件
app.config_from_object('django.conf:settings', namespace='CELERY')
#自动发现所有已按照应用程序中的任务task.py
app.autodiscover_tasks()