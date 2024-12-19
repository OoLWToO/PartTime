# 导库
import os
import requests
import json
import re
import sqlite3

# 1.  基础网页
base = "http://www.ptpress.com.cn/"
head = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; "
                      "Win64; x64) AppleWebKit 537.36 "
                      "(KHTML, like Gecko) Chrome/127.0.0.0 "
                      "Safari/537.36 Edg/127.0.0.0"}
res = requests.get(base, headers=head)
s = res.text
# 分析网页脚本 提取脚本中地址信息？？？
pattern = re.compile("getTagList.*?url:(?P<addr>.*?),", re.S)
v = re.search(pattern, s)
typeListUrl = v.group('addr')
typeListUrl = typeListUrl.strip()
typeListUrl = typeListUrl.strip(" ' ")

# 2 . 推荐的分类列表地址
# typeListUrl = "recommendBook/getRecommendTypeListForPortal"
reqUrl = base + typeListUrl  #
res = requests.get(reqUrl, headers=head)  # 发起请求
html = res.text  # 获取网页
print(html)  # 打印网页
datas = json.loads(html)  # 解析json数据
# print(datas)
types = datas['data']  # 通过键 ‘data' 提取数据
print(types)

# 3 . 重要荣誉地址
# honorUrl = "honor/getHonorListForPortal"
reqUrl = base + 'honor/getHonorListForPortal'  #
res = requests.get(reqUrl, headers=head)  # 发起请求
html = res.text  # 获取网页
print(html)  # 打印网页
datas = json.loads(html)  # 解析json数据
honors = datas['data']  # 通过键 ‘data' 提取数据
print(honors)

# 4 . 获奖出版物地址
# prizeUrl = "prizeBook/getPrizeType"
reqUrl = base + 'prizeBook/getPrizeType'  #
res = requests.get(reqUrl, headers=head)  # 发起请求
html = res.text  # 获取网页
print(html)  # 打印网页
datas = json.loads(html)  # 解析json数据
prizes = datas['data']  # 通过键 ‘data' 提取数据
print(prizes)


# 检查路径是否存在
if not os.path.exists('新书推荐'):
    # 如果路径不存在，则创建路径
    os.makedirs('新书推荐')
if not os.path.exists('重要荣誉'):
    os.makedirs('重要荣誉')
if not os.path.exists('获奖出版物'):
    os.makedirs('获奖出版物')
conn = sqlite3.connect("masterbook.db")  # 打开或创建数据库文件
c = conn.cursor()  # 获取游标
try:
    # 创建数据库表头: 栏目、分类、书名、作者、价格、折扣价格、作者简介、内容简介
    sql = '''
    create table book
            (columns text not null,
            categories text not null,
            name text not null,
            authors text not null,
            prices REAL,
            discounts REAL,
            authors_intro text not null,
            content_intro text not null);
    '''
    c.execute(sql)  # 执行sql语句
except sqlite3.OperationalError as e:
    print('book表已存在')
#
# # 一、爬取新书推荐中书籍
# for type in types:
#     bookId = type['bookTagId']  # # 提取数据
#     categories = type['name']  # 提取数据
#     print(bookId, categories)  # 打印数据
#     # 3. 推荐分类对应的书目地址
#     bookListUrl = "recommendBook/getRecommendBookListForPortal"  # 推荐书目地址
#     reUrl = base + bookListUrl + "?bookTagId=" + bookId  # 拼接地址
#     res = requests.get(reUrl, headers=head)  # 发起请求
#     html = res.text  # 获取网页
#     # print(html)  # 打印网页
#     boosInfo = json.loads(html)  # 解析json数据
#     books = boosInfo['data']  # 通过键 ‘data' 提取数据
#     for book in books:  # 提取数据
#         picPath = book['picPath']
#         bookName = book['bookName']
#         bookName = re.sub(r'[^\w\s.-]', '', bookName)  # 去掉特殊符号
#         bookId = book['bookId']
#         print(picPath, bookName, bookId)  # 打印数据
#
#         # requests.get(picPath,bookName,bookId)  # 下载图片
#         rt = requests.get(picPath)  # 获取图片
#         file = open(f'新书推荐/{bookName}.jpg', 'wb')  # 保存图片
#         file.write(rt.content)  # 保存图片
#         file.close()
#
#         detail_url = f'{base}bookinfo/getBookDetailsById?bookId={bookId}'
#         response = requests.post(url=detail_url, headers=head)
#         bookDetailInfo = response.json()['data']
#         name = bookDetailInfo['bookName']
#         authors = bookDetailInfo['author']
#         prices = bookDetailInfo['price']
#         discounts = bookDetailInfo['discountPrice']
#         authors_intro = bookDetailInfo['authorIntro']['data']
#         content_intro = bookDetailInfo['resume']['data']
#         insert_sql = '''
#         INSERT INTO book (columns, categories, name, authors, prices, discounts, authors_intro, content_intro)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?);
#         '''
#         c.execute(insert_sql, ('新书推荐', categories, name, authors, float(prices), float(discounts), authors_intro, content_intro))
#         # 提交事务
#         conn.commit()
#
# # 二、爬取重要荣誉中的内容
# for honor in honors:
#     honor_url = base + honor['picPath']
#     res = requests.get(honor_url, headers=head)
#     file = open(f'重要荣誉/{honor["honorName"]}.jpg', 'wb')  # 保存图片
#     file.write(res.content)  # 保存图片
#     file.close()

# 三、爬取获奖出版物的中书籍
for prize in prizes:
    bookId = prize['id']  # # 提取数据
    categories = prize['name']  # 提取数据
    print(bookId, categories)  # 打印数据
    bookListUrl = "prizeBook/getPrizeInfo"  # 获奖出版物书目地址
    reUrl = base + bookListUrl + "?prizeTypeId=" + bookId  # 拼接地址
    res = requests.get(reUrl, headers=head)  # 发起请求
    html = res.text  # 获取网页
    boosInfo = json.loads(html)  # 解析json数据
    # 先循环第几届，再循环书本
    book_year = boosInfo['data']  # 通过键 ‘data' 提取数据
    for year in book_year:  # 提取数据
        for book in year['prizeBook']:
            picPath = 'https://cdn.ptpress.cn/' + book['ossPath']
            bookName = book['bookName']
            bookName = re.sub(r'[^\w\s.-]', '', bookName)  # 去掉特殊符号

            rt = requests.get(picPath)  # 获取图片
            file = open(f'获奖出版物/{bookName}.jpg', 'wb')  # 保存图片
            file.write(rt.content)  # 保存图片
            file.close()

            try:
                bookId = book['bookUrl'].replace('https://www.ptpress.com.cn/shopping/buy?bookId=', '')
            except:
                print(f'{bookName}无法查看详细')
                continue
            print(picPath, bookName, bookId)  # 打印数据

            detail_url = f'{base}bookinfo/getBookDetailsById?bookId={bookId}'
            response = requests.post(url=detail_url, headers=head)
            bookDetailInfo = response.json()['data']
            if not bookDetailInfo:
                print(f'{bookName}无法查看详细')
                continue
            name = bookDetailInfo['bookName']
            authors = bookDetailInfo['author']
            prices = bookDetailInfo['price']
            discounts = bookDetailInfo['discountPrice']
            try:
                authors_intro = bookDetailInfo['authorIntro']['data']
            except:
                authors_intro = ''
            content_intro = bookDetailInfo['resume']['data']
            insert_sql = '''
            INSERT INTO book (columns, categories, name, authors, prices, discounts, authors_intro, content_intro)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            '''
            c.execute(insert_sql, ('获奖出版物', categories, name, authors, float(prices), float(discounts), authors_intro, content_intro))
            # 提交事务
            conn.commit()

# 关闭连接
conn.close()
