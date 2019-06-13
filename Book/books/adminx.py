import xadmin
from .models import *

# #主题设置
# class BaseSetting(object):
#     enable_themes=True
#     use_bootswatch=True
#
# #全局设置
# class GlobalSetting(object):
#     #标题
#     site_title='图灵书城后台管理系统'
#     #底部
#     site_footer='ECNU'
#     #修改菜单栏，改成收缩形式
#     menu_style='accordion'


#账户管理表
class BooksAdmin(object):
    #显示字段,显示id便于查看
    list_display=['id','type_id','name','desc','price','score','stock','sales','image','status','is_delete','create_time','update_time']
    search_fields=['id','type_id','name','desc','price','score','stock','sales','detail','status','is_delete']
    list_filter=['id','type_id','name','desc','price','score','stock','sales','detail','status','is_delete','create_time','update_time']
    list_editable = ['is_delete','price','type_id','sales' ]
    model_icon = 'fa fa-book'


#注册管理表
xadmin.site.register(Books,BooksAdmin)

# #注册主题
# xadmin.site.register(views.BaseAdminView,BaseSetting)
# #注册设置
# xadmin.site.register(views.CommAdminView,GlobalSetting)
