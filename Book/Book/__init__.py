'''
__init_.py文件是一个空文件，因为Django连接MySQL时默认使用MySQLdb驱动，
但MySQLdb不支持Python3，因此这里将MySQL驱动设置为pymysql。
'''
from __future__ import absolute_import, unicode_literals
import pymysql
pymysql.install_as_MySQLdb()

#确保django启动时app被加载
from .celery import app as celery_app
__all__ = ('celery_app',)