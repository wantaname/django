import xadmin
from xadmin import views
from .models import *


#评论模块
class CommentsAdmin(object):
    list_display=['id','user','book','content','is_delete','create_time','update_time']
    search_fields=['id','user','book','content','is_delete',]
    list_filter=['id','user','book','content','is_delete','create_time','update_time']
    list_editable = [ 'is_delete',]
    model_icon='fa fa-comment'


#注册
xadmin.site.register(Comments,CommentsAdmin)



