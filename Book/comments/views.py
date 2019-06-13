# comments/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from comments.models import Comments
from books.models import Books
from users.models import Passport
from django.views.decorators.csrf import csrf_exempt
import json
import redis
from utils.utils import login_required
from datetime import datetime
# Create your views here.
# 设置过期时间


# 连接redis数据库
#redis连接池

@login_required
def comment(request):
    a=1
    book_id = request.POST.get('book_id')
    user_id = request.POST.get('user_id')
    content = request.POST.get('content')

    book = Books.objects.get(id=book_id)
    user = Passport.objects.get(id=user_id)

    try:
        # 保存评论到数据库
        comment = Comments(book=book, user=user, content=content)
        comment.save()
        #记录当前时间
        time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return JsonResponse({
            'code': 0,
            'msg': '评论失败，原因：' + str(e),
        })
    # 评论成功
    return JsonResponse({
        'code': 1,
        'msg': '评论成功！',
        'time':time,
    })
