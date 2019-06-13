#bs学习
import requests
import lxml
from bs4 import BeautifulSoup
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Cookie':'ll="108296"; bid=iec_l7DKLhA; gr_user_id=202d6424-c687-42ef-9433-edfba0db8559; _vwo_uuid_v2=D11FF3B549B3D9CDE97D663570497D7A5|751cd2c7d2e64ecb7b49a07a240572ca; __yadk_uid=GqCrNlnIJ9TC2aZ0x9gBwK1pCITrceTv; __gads=ID=46ed7035e419df0a:T=1558409035:S=ALNI_MZZZ7UHfvypGMD7A_216lR-08kHjQ; douban-fav-remind=1; __utmc=30149280; __utmc=81379588; __utmz=81379588.1559018854.9.7.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmz=30149280.1559018854.14.12.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; viewed="3032251_2130190_26829016_25900156_26612779_10792216"; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1559024169%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.3ac3=*; __utma=30149280.1610361895.1558409031.1559018854.1559024175.15; __utma=81379588.1006620.1558409032.1559018854.1559025300.10; __utmb=81379588.1.10.1559025300; _pk_id.100001.3ac3=522c7543b305c5cc.1558409032.10.1559026803.1559022207.; ap_v=0,6.0; __utmt=1; __utmb=30149280.13.10.1559024175'
}
params={'search_text':'java','cat':'1001'}
# url='https://book.douban.com/subject_search?search_text=java&cat=1001'
# html=requests.get(url,headers=headers)
html='''<html><head><title>The Dormouse's story</title></head><body>你好！<p id="1" class="2 4">ppt</p><a href="www.baidu.com">百度</a><a href="www.test.com">百度</a></body><html>'''
soup=BeautifulSoup(html,'lxml')

#得到漂亮的输出
# print(soup.prettify())

'''soup对象后面直接加标签，得到的还是一个soup对象，所以可以链式查找'''
#找到title标签
print(soup.title)
#找到title标签名字
print(soup.title.name)
#得到title标签的内容，返回的不是字符串
print(soup.title.string)
#得到title的父节点名字s
print(soup.title.parent.name)

'''find方法查找标签'''
a=soup.find('a')
#获取属性
print(a.get('href'))


'''对象：Tag'''
print(soup.a)#只能得到第一个tag
#属性：name
print(soup.a.name)
#属性：attributes
print(soup.a.attrs)#点取，返回字典
print(soup.a['href'])
#对于多值属性同样的道理，返回列表

'''NavigableString 对象'''
print(soup.a.string)


"""
遍历文档树
"""
'''节点：标签+标签内容'''
#.contents:将tag的子节点以列表方式输出
print(soup.html.contents)#直接子节点
#.children:子节点生成器
print(soup.html.children)#是一个生成器
#.descendants:子孙节点生成器
print(soup.html.descendants)
#.strings 和 stripped_strings

#父节点：.parent
print(soup.title.parent)
#父节点生成器：.parents
print(soup.title.parents)

#.next_sibling：下一个兄弟
print(soup.head.next_sibling)
#.previou_sibling同理

#.next_siblings和.previou_sibling用于迭代

'''html的解析规则是顺序解析'''
#next_element下一个被解析的对象
print(soup.html.next_element)
#.previous_element:上一个被解析的对象
print(soup.title.previous_element)

#next_elements和previous_elements用于迭代

"""
搜索文档树
"""
#常用：find()、find_all()
#过滤器：搜索就会用到过滤器
#可用于tag的name中、节点属性中、字符串或者他们的混合
print(soup.find_all('a'))#返回节点列表
#可以传入正则表达式
import re
print(soup.find_all(re.compile('hea')))

#传入列表：返回任一匹配
print(soup.html.find_all(['a','title']))

#True：返回所有节点

#还可以传入一个自定义的方法

#find_all( name , attrs , recursive , text , **kwargs )
print(soup.html.find_all('p',attrs={'class':'2','id':'1'}))
"""参数说明"""
'''name,attrs,text参数都接受字符串，正则，列表和True'''
#name:名字为tag的name，可以是任一类型的过滤器
#attrs:可以直接用attrs参数，也可以用关键字参数
#关键字参数：搜索时会当作指定tag的属性,可以使用多个关键字参数
print(soup.find_all(id=True))
#有些属性不能用作关键字参数，比如data-*,但可以用attrs参数
print(soup.find_all(attrs={'id':True}))#这样也可以

#按css搜索
#因为class是python中的保留字，故用class_替代
print(soup.find_all(attrs={'class':'2'}))#在attr中正常使用
print(soup.find_all(class_='2'))
#注：属性是多值是，只满桌子一个属性即可，就好比把属性分开来写

#text参数:字符串内容
print(soup.find_all(text=re.compile("你好"))) #返回的是字符串

#limit参数:限制返回结果的数量

#recursive参数：递归查找，为False则只查字节点

#因为find_all()过于常用，所以我们定义了一种简便方式,以下两种方式等价
print(soup.html('a'))
print(soup.html.find_all('a'))

#bs支持大部分的css选择器，用select
print(soup.select('title'))
print(soup.select('body a'))
print(soup.select('html > a'))
print(soup.a.attrs['href'])#点取，返回字典
print(soup.html.find('a').attrs)

#get_text()与string的区别
#string:不是字符串
#get_text():是字符串

print(soup.a.attrs['href'])
print(soup.find_all('a'))
a=soup.find_all('a')
print(type(a))
print(soup.find('body').a.find('p'))
print(type(soup.find('a').get_text()))