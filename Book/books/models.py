'''
商品信息管理
'''
from django.template.defaultfilters import truncatechars
from django.db import models
from db.base_model import BaseModel
from django.contrib.auth.hashers import make_password
from tinymce.models import HTMLField
from books.enums import *
# Create your models here.
#书籍种类


class BooksManager(models.Manager):
    '''商品模型管理器类'''
    # sort='new' 按照创建时间进行排序
    # sort='hot' 按照商品销量进行排序
    # sort='price' 按照商品的价格进行排序
    # sort= 按照默认顺序排序
    def get_books_by_type(self, type_id, limit=None, sort='default'):
        '''根据商品类型id查询商品信息'''
        if sort == 'new':
            #按照更新时间排
            order_by = ('-update_time',)
        elif sort == 'hot':
            #按照销量
            order_by = ('-sales',)
        elif sort == 'price':
            #价格从低到高
            order_by = ('price', )
        elif sort=='score':
            #评分从高到低
            order_by = ('-score', ) # 按照评分降序排列。
        else:
            order_by=('-score',)
        # 按照种类筛选数据
        books_li = self.filter(type_id=type_id).order_by(*order_by)
        # 查询结果集的限制
        if limit:
            books_li = books_li[:limit]
        return books_li

    def get_books_by_id(self, books_id):
        '''根据商品的id获取商品信息'''
        try:
            books = self.get(id=books_id)
        except self.model.DoesNotExist:
            # 不存在商品信息
            books = None
        return books


#书籍
class Books(BaseModel):
    '''商品模型类'''
    books_type_choices = ((k, v) for k, v in BOOKS_TYPE.items())
    status_choices = ((k, v) for k,v in STATUS_CHOICE.items())
    type_id = models.SmallIntegerField(default=PYTHON, choices=books_type_choices, verbose_name='商品种类')
    name = models.CharField(max_length=100, unique=True,verbose_name='商品名称')
    desc = models.CharField(max_length=200, verbose_name='商品简介')

    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='商品价格',db_index=True)
    #改了一下，把评分改为varchar
    score = models.DecimalField(max_digits=3,decimal_places=1, verbose_name='豆瓣评分',db_index=True)
    stock = models.IntegerField(default=10, verbose_name='商品库存')
    sales = models.IntegerField(default=0, verbose_name='商品销量')
    detail = HTMLField(blank=True,verbose_name='商品详情')
    image = models.ImageField(upload_to='books', verbose_name='商品图片')
    status = models.SmallIntegerField(default=ONLINE, choices=status_choices, verbose_name='商品状态')
    #管理器
    objects = BooksManager()

    # admin显示书籍的名字
    def __str__(self):
        return self.name


    class Meta:
        verbose_name = '商品管理'
        verbose_name_plural = '商品管理'

