from django.urls import path,include
from . import views

app_name='cart'

urlpatterns=[
    path('add/',views.cart_add,name='add'),#添加购物车
    path('count/',views.cart_count,name='count'),#商品数量
    path('del/',views.cart_del,name='delete'),
    path('update/',views.cart_update,name='update'),
    path('',views.cart_show,name='show'),
]