import xadmin
from xadmin import views
from .models import *


#订单信息管理表
class OrderInfoAdmin(object):
    #显示字段,显示id便于查看
    list_display=['order_id','passport','addr','total_count','transit_price','pay_method','status','trade_id','total_price','is_delete','create_time','update_time']
    search_fields=['order_id','passport__username','addr__recipient_addr','total_count','transit_price','pay_method','status','trade_id','total_price','is_delete']
    list_filter=['order_id','passport__username','addr__recipient_addr','total_count','transit_price','pay_method','status','trade_id','total_price','is_delete']
    model_icon='fa fa-money'
    list_editable = [ 'is_delete',]

#地址管理
class OrderBooksAdmin(object):
    list_display=['id','order','books','count','price','is_delete','create_time','update_time']
    #passport是外键，搜索和过滤都要指定属性
    search_fields=['id','order','books','count','price','is_delete',]
    list_filter=['id','order','books','count','price','is_delete',]
    model_icon='fa fa-shopping-cart'
    list_editable = [ 'is_delete',]





#注册管理表
xadmin.site.register(OrderInfo,OrderInfoAdmin)
xadmin.site.register(OrderBooks,OrderBooksAdmin)

