import re

from django.core.paginator import Paginator
from django.http import JsonResponse
import redis
from django_redis import get_redis_connection
from django.shortcuts import render, redirect, reverse
from django.views import View
from itsdangerous import SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from utils.utils import login_required
from .tasks import send_active_email
from users.models import Passport,Address
from users.models import *
from books.models import *
from cart.models import *
from order.models import *
from django.views.decorators.cache import cache_page
# Create your views here.

#注册,需要验证邮箱
class Register(View):
    def get(self,request):
        return render(request, 'users/register.html')
    '''进行用户注册处理'''
    def post(self,request):
        #接收post过来的数据
        username=request.POST.get('user_name')
        password=request.POST.get('pwd')
        email=request.POST.get('email')

        #进行数据校验
        if not all([username,password,email]):
            #有数据为空
            return render(request,'users/register.html',context={'errmsg':'参数不能为空'})
        if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            #邮箱不合法
            return render(request, 'users/register.html', {'errmsg': '邮箱不合法!'})
        # 注册，向数据库中添加账户
        try:
            passport=Passport.objects.add_one_passport(username=username,password=password,email=email)
        except Exception as e:
            print('error:',e)
            return render(request,'users/register.html',{'errmsg':'用户名已存在！'})

        serializer = Serializer(settings.SECRET_KEY, 3600)
        token = serializer.dumps({'confirm': passport.id})  # 返回bytes
        token = token.decode()
        #发送激活邮箱
        send_active_email.delay(token, email)
        passport.save()

        # 注册完，还是返回注册页。
        # return redirect(reverse('user:register'))
        return HttpResponse("注册成功！请检查邮箱以激活您的账户！")

#邮箱验证
def register_active(request, token):
    '''用户账户激活'''
    serializer = Serializer(settings.SECRET_KEY, 3600)
    try:
        info = serializer.loads(token)
        passport_id = info['confirm']
        # 进行用户激活
        passport = Passport.objects.get(id=passport_id)
        passport.is_active = True
        passport.save()
        # 跳转的登录页
        return redirect(reverse('user:login'))
    except SignatureExpired:
        # 链接过期
        return HttpResponse('激活链接已过期')

#登录
class Login(View):
    #请求登录页面
    def get(self,request):
        #用cookie自动填用户名和密码
        if request.COOKIES.get('username'):
            username=request.COOKIES.get('username')
            checked='checked'
        else:
            username=''
            checked=''
        if request.COOKIES.get('password'):
            password=request.COOKIES.get('password')
        else:
            password=''
        context={
            'username':username,
            'password':password,
            'checked':checked,
        }
        return render(request,'users/login.html',context=context)

    #提交登录请求
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        verifycode = request.POST.get('verifycode')
        # 数据校验
        if not all([username, password]):
            # 有数据为空
            return JsonResponse({'res': 0})
        #验证码是否正确
        if verifycode.upper() != request.session['verifycode']:
            return JsonResponse({'res': 1})
        # 数据库中查找账户信息
        passport = Passport.objects.get_one_passport(username=username, password=password)
        #验证通过,跳转到首页
        if passport:
            #反转函数，即通过视图反转得到url
            next_url=reverse('books:index')
            print(next_url)
            #需要返回的JsonResponse对象，是HttpResponse的子类
            jres=JsonResponse({'res':2,'next_url':next_url})

            #判断是否需要记住用户名和密码
            #json传递过来的都是字符串，
            if remember=='true':
                #调用HttpResponse对象的方法设置cookie
                jres.set_cookie('username',username,max_age=7*24*3600)
                jres.set_cookie('password',password,max_age=7*24*3600)
            else:
                #不记住用户名和密码
                jres.delete_cookie('username')
                jres.delete_cookie('password')
            #设置会话，记住用户的登录状态
            request.session['islogin']=True
            request.session['username']=username
            request.session['passport_id']=passport.id
            #登录成功后清理图片缓存
            del request.session['verifycode']
            return jres

        else:
            #用户名或密码错误
            return JsonResponse({'res':0})


#图片验证码
from django.http import HttpResponse
from django.conf import settings
import os
from PIL import Image,ImageDraw,ImageFont
import random
def verifycode(request):
    #背景色
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    #宽高
    width=100
    height=25
    size=(width,height)
    #创建画面对象
    im=Image.new('RGB',size,bgcolor)
    #创建画笔对象
    draw=ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in  range(0,100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象
    font = ImageFont.truetype(os.path.join(settings.BASE_DIR, "ALGER.TTF"), 15)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw

    #将验证码存入session
    request.session['verifycode']=rand_str

    import io
    buf=io.BytesIO()
    im.save(buf,'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


#用户订单
@login_required
def order(request, page):
    '''用户中心-订单页'''
    # 查询用户的订单信息
    passport_id = request.session.get('passport_id')

    # 获取用户的所有订单信息
    order_li = OrderInfo.objects.filter(passport_id=passport_id)

    # 遍历获取订单的商品信息
    # order->OrderInfo实例对象
    for order in order_li:
        # 根据订单id查询订单商品信息
        order_id = order.order_id
        order_books_li = OrderBooks.objects.filter(order_id=order_id)

        # 计算商品的小计
        # order_books ->OrderGoods实例对象
        for order_books in order_books_li:
            count = order_books.count
            price = order_books.price
            amount = count * price
            # 保存订单中每一个商品的小计
            order_books.amount = amount

        # 给order对象动态增加一个属性order_books_li,保存订单中商品的信息
        order.order_books_li = order_books_li

    paginator = Paginator(order_li, 3)  # 每页显示3个订单

    num_pages = paginator.num_pages

    if not page:  # 首次进入时默认进入第一页
        page = 1
    if page == '' or int(page) > num_pages:
        page = 1
    else:
        page = int(page)

    order_li = paginator.page(page)

    if num_pages < 5:
        pages = range(1, num_pages + 1)
    elif page <= 3:
        pages = range(1, 6)
    elif num_pages - page <= 2:
        pages = range(num_pages - 4, num_pages + 1)
    else:
        pages = range(page - 2, page + 3)

    context = {
        'order_li': order_li,
        'pages': pages,
    }

    return render(request, 'users/user_center_order.html', context)


#用户中心,要判断用户是否登录，没有登录则跳转到登录界面，这里用装饰器
@login_required
def user(request):
    '''用户中心-信息页'''
    passport_id = request.session.get('passport_id')
    # 获取用户的基本信息
    addr = Address.objects.get_default_address(passport_id=passport_id)

    # 获取用户的最近浏览信息
    con = get_redis_connection('default')
    key = 'history_%d' % passport_id
    # 取出用户最近浏览的5个商品的id
    history_li = con.lrange(key, 0, 4)
    # history_li = [21,20,11]
    # print(history_li)
    # 查询数据库,获取用户最近浏览的商品信息
    # books_li = Books.objects.filter(id__in=history_li)
    books_li = []
    for id in history_li:
        books = Books.objects.get_books_by_id(books_id=id)
        books_li.append(books)

    return render(request, 'users/user_center_info.html', {'addr': addr,
                                                           'page': 'user',
                                                           'books_li': books_li})




#退出
def logout(request):
    # 清空用户的session信息
    request.session.flush()
    # 跳转到首页
    return redirect(reverse('books:index'))

@login_required
def address(request):
    '''用户中心-地址页'''
    # 获取登录用户的id
    passport_id = request.session.get('passport_id')

    if request.method == 'GET':
        # 显示地址页面
        # 查询用户的默认地址
        addr = Address.objects.get_default_address(passport_id=passport_id)
        #查询用户的所有地址,是一个列表
        addrs=Address.objects.filter(passport_id=passport_id).filter(is_delete=False)

        return render(request, 'users/user_center_site.html', {'addr': addr, 'addrs': addrs})
    else:
        # 添加收货地址
        # 1.接收数据
        recipient_name = request.POST.get('username')
        recipient_addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        recipient_phone = request.POST.get('phone')

        # 2.进行校验
        if not all([recipient_name, recipient_addr, zip_code, recipient_phone]):
            return render(request, 'users/user_center_site.html', {'errmsg': '参数不能为空!'})

        # 3.添加收货地址
        Address.objects.add_one_address(passport_id=passport_id,
                                        recipient_name=recipient_name,
                                        recipient_addr=recipient_addr,
                                        zip_code=zip_code,
                                        recipient_phone=recipient_phone)

        # 4.返回应答
        return redirect(reverse('user:address'))

def default_address(request):
    addr_id=request.POST.get("addr_id")
    addr_id=int(addr_id)
    passport_id=request.session.get('passport_id')
    #原来的默认地址
    default=Address.objects.get_default_address(passport_id=passport_id)
    #如果有则移除
    if default:
        default.is_default=False
        default.save()
    #将现在提交的地址设置为默认地址
    default_now=Address.objects.filter(id=addr_id).update(is_default=True)
    return JsonResponse({'res':1})

def delete_address(request):
    addr_id = request.POST.get("addr_id")
    addr_id = int(addr_id)
    Address.objects.filter(id=addr_id).update(is_delete=True)
    return JsonResponse({'res': 1})

import pymysql
#sql注入测试
class SqlTest(View):
    def get(self,request):
        return render(request, 'test/test.html')

    def post(self,request):
        #获取用户输入
        username=request.POST.get('username')
        password=request.POST.get('password')
        #假装不知道用户输入的是sql语句
        conn=pymysql.connect(host='127.0.0.1',user='Book',password='981011yzp',database='Book',charset='utf8')
        cursor=conn.cursor()
        sql="SELECT * FROM users_passport WHERE username='{0}' AND password='{1}' AND is_active=1".format(username,password)
        result=cursor.execute(sql)
        #返回的是一个元组
        user=cursor.fetchone()
        if user:
            request.session['islogin'] = True
            request.session['username'] = user[4]
            request.session['passport_id'] = user[0]
            context={
                'res':1,
                'next_url':reverse('books:index'),
            }
            return JsonResponse(data=context)
        else:
            return JsonResponse(data={'res':0})