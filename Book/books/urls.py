from django.urls import path,include
from . import views
app_name='books'

urlpatterns =[
    path('books/<int:books_id>/',views.detail,name='detail'),
    path('list/<int:type_id>/<int:page>/',views.list,name='list'),
    path('',views.index,name='index'), #首页
    path('collection/',views.Collection.as_view(),name='collection'),#书籍采集
    path('modify/',views.Modify.as_view(),name='modify')#书籍修改

]