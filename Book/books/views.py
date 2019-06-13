from django.shortcuts import render,redirect,reverse
from ad.models import Ad
from books.models import *
# import logging
from django.core.paginator import Paginator
from django_redis import get_redis_connection
from django.views import View
from django.http import JsonResponse,HttpResponse
# logger = logging.getLogger('django.request')
# Create your views here.
#首页视图函数


def index(request):
    #取销量最高的三本
    python_new = Books.objects.get_books_by_type(PYTHON, limit=3, sort='hot')
    #评分最高的三本
    python_hot = Books.objects.get_books_by_type(PYTHON, limit=4, sort='score')
    javascript_new = Books.objects.get_books_by_type(JAVASCRIPT, limit=3, sort='hot')
    javascript_hot = Books.objects.get_books_by_type(JAVASCRIPT, limit=4, sort='score')
    algorithms_new = Books.objects.get_books_by_type(ALGORITHMS, limit=3, sort='hot')
    algorithms_hot = Books.objects.get_books_by_type(ALGORITHMS, limit=4, sort='score')
    machinelearning_new = Books.objects.get_books_by_type(MACHINELEARNING, limit=3, sort='hot')
    machinelearning_hot = Books.objects.get_books_by_type(MACHINELEARNING, limit=4, sort='score')
    operatingsystem_new = Books.objects.get_books_by_type(OPERATINGSYSTEM, limit=3, sort='hot')
    operatingsystem_hot = Books.objects.get_books_by_type(OPERATINGSYSTEM, limit=4, sort='score')
    database_new = Books.objects.get_books_by_type(DATABASE, limit=3, sort='hot')
    database_hot = Books.objects.get_books_by_type(DATABASE, limit=4, sort='score')
    other_new = Books.objects.get_books_by_type(OTHER, limit=3, sort='hot')
    other_hot = Books.objects.get_books_by_type(OTHER, limit=4, sort='score')
	#四张广告图片
    ads=Ad.objects.filter(is_delete=False)[0:4]

    # 定义模板上下文
    context = {
        'python_new': python_new,
        'python_hot': python_hot,
        'javascript_new': javascript_new,
        'javascript_hot': javascript_hot,
        'algorithms_new': algorithms_new,
        'algorithms_hot': algorithms_hot,
        'machinelearning_new': machinelearning_new,
        'machinelearning_hot': machinelearning_hot,
        'operatingsystem_new': operatingsystem_new,
        'operatingsystem_hot': operatingsystem_hot,
        'database_new': database_new,
        'database_hot': database_hot,
        'other_new': other_new,
        'other_hot': other_hot,
		'ads':ads,
    }
    # 使用模板
    return render(request, 'books/index.html', context)

#详情页，会记录用户浏览
def detail(request, books_id):
    '''显示商品的详情页面'''
    # 获取商品的详情信息
    books = Books.objects.get_books_by_id(books_id=books_id)

    if books is None:
        # 商品不存在，跳转到首页
        return redirect(reverse('books:index'))

    # 新品推荐
    books_li = Books.objects.get_books_by_type(type_id=books.type_id, limit=2, sort='new')
    type_title = BOOKS_TYPE[books.type_id]
    # 用户登录之后，才记录浏览记录
    # 每个用户浏览记录对应redis中的一条信息 格式:'history_用户id':[10,9,2,3,4]
    # [9, 10, 2, 3, 4]
    if request.session.has_key('islogin'):
        # 用户已登录，记录浏览记录
        con = get_redis_connection('default')
        key = 'history_%d' % request.session.get('passport_id')
        # 先从redis列表中移除books.id,表示最近浏览的不包括本商品
        con.lrem(key, 0, books.id)
        #将本商品插入到列表头部
        con.lpush(key, books.id)
        # 对列表进行修剪，保存用户最近浏览的5个商品
        con.ltrim(key, 0, 4)


    # 定义上下文
    context = {'books': books, 'books_li': books_li,'type_title':type_title}

    # 使用模板
    return render(request, 'books/detail.html', context)


#列表页
def list(request, type_id, page):
    '''商品列表页面'''
    # 获取排序方式
    sort = request.GET.get('sort', 'default')

    # 判断type_id是否合法
    if int(type_id) not in range(1,8):
        #不合法则返回主页
        return redirect(reverse('books:index'))

    # 根据商品种类id和排序方式查询数据
    books_li = Books.objects.get_books_by_type(type_id=type_id, sort=sort)

    # 分页，每页条数据
    paginator = Paginator(books_li, 15)

    # 获取分页之后的总页数
    num_pages = paginator.num_pages

    # 取第page页数据，超出则回到第一页
    if page > num_pages:
        page = 1

    # 返回值是一个Page类的实例对象
    books_li = paginator.page(page)

    # 进行页码控制
    # 1.总页数<5, 显示所有页码
    # 2.当前页是前3页，显示1-5页
    # 3.当前页是后3页，显示后5页 10 9 8 7
    # 4.其他情况，显示当前页前2页，后2页，当前页
    if num_pages < 5:
        pages = range(1, num_pages+1)
    elif page <= 3:
        pages = range(1, 6)
    elif num_pages - page <= 2:
        pages = range(num_pages-4, num_pages+1)
    else:
        pages = range(page-2, page+3)

    # 新品推荐
    books_new = Books.objects.get_books_by_type(type_id=type_id, limit=2, sort='new')
    type_title = BOOKS_TYPE[int(type_id)]

    # 获取书籍类别
    context = {
        'books_li': books_li,
        'books_new': books_new,
        'type_id': type_id,
        'sort': sort,
        'pages': pages,
        'type_title': type_title,
    }

    # 使用模板
    return render(request, 'books/list.html', context)

import requests
from bs4 import BeautifulSoup
import time
import random
import os
from django.conf import settings
from fake_useragent import UserAgent
import lxml
from users.models import *
from django.db import transaction
class Collection(View):
    def get(self,request):
        user=request.session.get('username')
        if user:
            mail=Passport.objects.get(username=user)
            if mail.email=='3335093743@qq.com':
                return render(request,'books/collection.html')
            else:
                return HttpResponse('非管理员不得入内！！')
        else:
            return render(request, 'users/login.html')

    def post(self,request):
        type=request.POST.get('type')
        type_id=int(type)
        book=request.POST.get('book')
        #添加失败
        defeat=0
        #添加总数
        count=0
        success=0
        #初始网址
        base_url='https://book.douban.com/tag/'
        #随机ua
        # ua=UserAgent().random
        # 请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',

        }
        proxies = {
            'http': 'http://220.173.37.80:8118',
            'https': 'http://220.173.37.80:8118',

        }

        # 请求url
        url = base_url + book
        while True:
            #响应
            html=requests.get(url=url,headers=headers)
            #解析后的bs对象
            soup=BeautifulSoup(html.content,'lxml')
            #获取每页的书籍列表
            books_list=soup.find_all('div',attrs={'class':'info'})
            if not books_list:
                break
            #对每一本书有
            for every_book in books_list:
                # 拿到书名
                book_name = every_book.h2.a.get_text().strip().replace('\n','')
                # 书名重复就不用继续了
                if Books.objects.filter(name=book_name):
                    defeat = defeat + 1
                    continue
                book_url=every_book.h2.a.attrs['href']


                #没有商品详情的,下一个
                if not every_book.find('p'):
                    continue

                book_desc=every_book.find('div',attrs={'class':'pub'}).get_text()
                #去除空格和换行
                book_desc=book_desc.replace(' ','').replace('\n','')
                # #随机休息0-1秒,防止根据频率反爬
                #草，不等了
                # time.sleep(random.random())
                #发起请求
                book_html=requests.get(book_url,headers=headers)
                book_soup=BeautifulSoup(book_html.content,'lxml')

                #拿到书籍图片
                image_url=book_soup.find('a',class_='nbg').img.get('src')
                path=str(image_url).split('/')[-1]
                #保存到数据库的路径，必须要正斜杠
                book_path='books/'+type+'/'+path
                #根据平台选择文件分隔符
                abs_path=os.path.join(settings.BASE_DIR, 'static','books',type,path)
                #拿到评分，
                book_score=book_soup.find('div',class_='rating_self').strong.get_text()
                #去除空格
                book_score=book_score.strip()
                #如果没有评分
                if book_score==' ' or book_score=='':
                    book_score='暂无评分'
                # 拿到介绍,是一个含<p>的列表
                detail=book_soup.find('div',class_='intro').contents
                book_detail=''
                for p in detail:
                    book_detail=book_detail+str(p)
                #拿到价格
                price=str(book_desc).split('/')[-1]
                book_price=str(price).replace('元','')

                try:
                    # 实例化
                    book = Books(type_id=type_id, name=book_name, desc=book_desc, price=book_price, score=book_score,
                                 stock=10, sales=0, detail=book_detail, image=book_path)
                    book.save()
                    # 下载图片到本地
                    with open(abs_path, 'wb') as f:
                        book_image = requests.get(image_url, headers=headers)
                        f.write(book_image.content)
                    success=success+1
                except Exception as e:
                    defeat=defeat+1
                    print('error:', e)
            #下一页的url
            try:
                if soup.find('span',class_='next').find('a'):
                    url='https://book.douban.com'+soup.find('span',class_='next').a['href']
                else:
                    break
            except Exception as e:
                break

            #返回ajax响应
        context={
            'count':defeat+success,
            'success':success,
            'defeat':defeat,
        }
        return JsonResponse(data=context)

import re
class Modify(View):
    def get(self,request):
        return HttpResponse('ok')





