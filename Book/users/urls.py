from django.urls import path,re_path
from . import views
app_name='user'

urlpatterns =[
    path('register/',views.Register.as_view(),name='register'),#用户注册
    re_path(r'^active/(?P<token>.*)/$', views.register_active, name='active'),#邮箱激活

    path('login/',views.Login.as_view(),name='login'),#登录
    path('verifycode/',views.verifycode,name='verifycode'),#验证码
    path('logout/',views.logout,name='logout'),#退出

    re_path(r'^order/(?P<page>\d+)?/?$',views.order,name='order'),#订单
    path('address/', views.address, name='address'),#收货地址
    path('default_address/',views.default_address,name='default_address'),
    path('delete_address/',views.delete_address,name='delete_address'),
    path('test/',views.SqlTest.as_view(),name='test'),#sql注入演示
    path('',views.user,name='user'), #用户中心
]