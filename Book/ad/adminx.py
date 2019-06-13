import xadmin
from .models import *

class AdAdmin(object):
    list_display=['id','name','image','url','is_delete','create_time','update_time']
    search_fields=['id','name','url','is_delete']
    list_filter=['id','name','url','is_delete']
    model_icon="fa fa-hand-o-right"
    list_editable = ['is_delete', ]

xadmin.site.register(Ad,AdAdmin)
