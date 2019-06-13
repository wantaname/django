'''
豆瓣爬虫，爬取指定类别书籍到mysql数据库
'''
import lxml
from bs4 import BeautifulSoup
import requests

#各种类对应的书籍搜索
#计算机&操作系统
computer=['计算机','操作系统','windows','linux','unix']
#数据结构
algorithm=['数据结构','算法']
#后端开发
backend=['python','java','php','c语言','c++','c#','go语言','asp','ruby','servlet','vb','Lua','Node.js']
#前端开发
frontend=['html','css','javascript','web','jquery','Bootstrap','vue','react']
#人工智能
AI=['人工智能','机器学习','深度学习','神经网络','大数据','云计算']
#数据库
database=['数据库','mysql','sql','redis','MongoDB','Memcached']

#初始的
base_url='https://book.douban.com/subject_search?search_text=%s'
#将种类和搜索字段构造成字典
books={
    '计算机&操作系统':computer,
    '数据结构&算法':algorithm,
    '后端开发':backend,
    '前端开发':frontend,
    '人工智能&大数据':AI,
    '数据库':database,
}
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
}

def douban(url,book_type):
    #发起请求
    html=requests.get(url,headers=headers)
    #bs对象
    soup=BeautifulSoup(html.content,'lxml')



#对每一个类目循环爬虫
for book in books.items():  #元组
    #对一个类中的书籍遍历搜索
    for search in book[1]:
        #拼接url
        url=base_url%book[0]
        #执行爬虫和保存到数据库
        douban(url,book[0])

