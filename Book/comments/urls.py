from django.urls import path,include
from . import views

app_name='comment'

urlpatterns=[
    path('comment/',views.comment,name='comment'),#评论
]