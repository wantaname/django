from django.shortcuts import render
from utils.utils import *
from django.http import JsonResponse
from books.models import Books
from django_redis import get_redis_connection
# Create your views here.
#购物车展示

@login_required
def cart_add(request):
    '''向购物车中添加数据'''

    # 接收数据
    books_id = request.POST.get('books_id')
    books_count = request.POST.get('books_count')


    # 进行数据校验
    if not all([books_id, books_count]):
        return JsonResponse({'res':1 , 'errmsg':'数据不完整'})

    books = Books.objects.get_books_by_id(books_id=books_id)
    if books is None:
        # 商品不存在
        return JsonResponse({'res':2, 'errmsg':'商品不存在'})

    try:
        count = int(books_count)
    except Exception as e:
        # 商品数目不合法
        return JsonResponse({'res':3, 'errmsg':'商品数量必须为数字'})

    # 添加商品到购物车
    # 每个用户的购物车记录用一条hash数据保存，格式:cart_用户id: 商品id 商品数量
    conn = get_redis_connection('default')
    cart_key = 'cart_%d' % request.session.get('passport_id')

    res = conn.hget(cart_key, books_id)
    if res is None:
        # 如果用户的购车中没有添加过该商品，则添加数据
        res = count
    else:
        # 如果用户的购车中已经添加过该商品，则累计商品数目
        res = int(res) + count

    # 判断商品的库存
    if res > books.stock:
        # 库存不足
        return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})
    else:
        #cart_key标识用户，books_id标识商品id，res标识商品数量
        conn.hset(cart_key, books_id, res)

    # 返回结果
    return JsonResponse({'res': 5})

#购物车显示页面
@login_required
def cart_show(request):
    #获取用户的id
    passport_id=request.session.get('passport_id')
    #实例化一个本地redis连接客户端
    conn=get_redis_connection()
    cart_key='cart_%d'%passport_id
    #获得redis缓存中用户的购物车信息，得到的值是一个字典,不存在则返回空列表
    res_dict=conn.hgetall(cart_key)
    books_li=[]

    total_count=0

    total_price=0

    #遍历商品id
    for id,count in res_dict.items():
        books=Books.objects.get_books_by_id(books_id=id)
        #数量
        books.count=int(count)
        #金额
        books.amount=int(count)*books.price
        #加到商品列表中
        books_li.append(books)
        #总数量
        total_count+=int(count)
        #总价格
        total_price+=int(count)*books.price

    context={
            'books_li':books_li,
            'total_count':total_count,
            'total_price':total_price,
    }

    return render(request,'cart/cart.html',context)

from django.http import HttpResponse
@login_required
def cart_count(request):
    '''获取用户购物车中商品的数目'''
    # 计算用户购物车商品的数量
    conn = get_redis_connection('default')
    cart_key = 'cart_%d' % request.session.get('passport_id')
    # res = conn.hlen(cart_key) #显示商品的条目数
    res=0
    #获取所有值，key不存在则返回空表
    res_list = conn.hvals(cart_key)

    for i in res_list:
        res += int(i)

    # 返回结果
    return JsonResponse({'res': res})

@login_required
def cart_del(request):
    '''删除用户购物车中商品的信息,要在缓存中删除商品信息'''

    # 接收数据
    books_id = request.POST.get('books_id')

    # 校验商品是否存放
    if not all([books_id]):
        return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

    books = Books.objects.get_books_by_id(books_id=books_id)
    if books is None:
        return JsonResponse({'res': 2, 'errmsg': '商品不存在'})

    # 删除购物车商品信息
    conn = get_redis_connection('default')
    cart_key = 'cart_%d' % request.session.get('passport_id')
    #删除指定用户的指定商品
    conn.hdel(cart_key, books_id)

    # 返回信息
    return JsonResponse({'res': 3})

@login_required
def cart_update(request):
    '''更新购物车商品数目,要在缓存中进行更新'''

    # 接收数据
    books_id = request.POST.get('books_id')
    books_count = request.POST.get('books_count')

    # 数据的校验
    if not all([books_id, books_count]):
        return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

    books = Books.objects.get_books_by_id(books_id=books_id)
    if books is None:
        return JsonResponse({'res': 2, 'errmsg': '商品不存在'})

    try:
        books_count = int(books_count)
    except Exception as e:
        print("e: ", e)
        return JsonResponse({'res': 3, 'errmsg': '商品数目必须为数字'})

    # 更新操作
    conn = get_redis_connection('default')
    cart_key = 'cart_%d' % request.session.get('passport_id')

    # 判断商品库存
    if books_count > books.stock:
        return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})

    conn.hset(cart_key, books_id, books_count)

    return JsonResponse({'res': 5})