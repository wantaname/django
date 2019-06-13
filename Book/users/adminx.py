import xadmin
from xadmin import views
from .models import *

#主题设置
class BaseSetting(object):
    enable_themes=True
    use_bootswatch=True

#全局设置
class GlobalSetting(object):
    #标题
    site_title='图灵书城后台管理系统'
    #底部
    site_footer='ECNU'
    #修改菜单栏，改成收缩形式
    menu_style='accordion'


#账户管理表
class PassportAdmin(object):
    #显示字段,显示id便于查看
    list_display=['id','username','password','email','is_active','is_delete','create_time','update_time']
    search_fields=['id','username','password','email','is_active','is_delete']
    list_filter=['id','username','password','email','is_active','is_delete','create_time','update_time']
    model_icon = 'fa fa-user'
    list_editable = [ 'is_delete',]

#地址管理
class AddressAdmin(object):
    list_display=['id','recipient_name','recipient_addr','zip_code','recipient_phone','is_default','passport','is_delete','create_time','update_time']
    #passport是外键，搜索和过滤都要指定属性
    search_fields=['id','recipient_name','recipient_addr','zip_code','recipient_phone','is_default','passport__username','is_delete']
    list_filter=['id','recipient_name','recipient_addr','zip_code','recipient_phone','is_default','passport__username','is_delete']
    model_icon='fa fa-map-marker'
    list_editable = [ 'is_delete',]


#注册管理表
xadmin.site.register(Passport,PassportAdmin)
xadmin.site.register(Address,AddressAdmin)

#注册主题
xadmin.site.register(views.BaseAdminView,BaseSetting)
#注册设置
xadmin.site.register(views.CommAdminView,GlobalSetting)
