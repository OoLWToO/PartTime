import os
import re

import requests
from lxml import etree
import pymssql

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '_YS_userAccect=3ddad132a7a44c12a095cc7d8ec69fe5; UM_distinctid=193de2dcd4530d-0ea991217481cd-26031051-144000-193de2dcd46566; hingecloud=2c35e07cd1aa4f09889e1ed348a9bc6b; CNZZDATA1281138311=258010894-1734599364-%7C1734677450',
    'Host': 'www.poly.com.cn',
    'If-Modified-Since': 'Fri, 13 Dec 2024 08:49:01 GMT',
    'If-None-Match': 'W/"675bf4fd-b94d"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}

username = 'sa'
password = '123456'
database = 'my_database'

if __name__ == '__main__':
    # 链接数据库: server改成你的服务器名, port不要改其参数,user你的用户名, password你的密码, database你的数据库名
    connect = pymssql.connect(host='localhost', server='DESKTOP-IFQ46VM', port='1433', user='sa', password='123456',
                              database='my_database')
    cursor = connect.cursor()
    # 创建表sql
    create_table_sql = """
    IF OBJECT_ID('poly', 'U') IS NOT NULL
        DROP TABLE poly
    CREATE TABLE poly (
        标题 NVARCHAR(255),
        日期 NVARCHAR(255),
        摘要 NVARCHAR(255),
        链接 NVARCHAR(255),
        图片链接 NVARCHAR(255),
        内容 NVARCHAR(MAX)
    )
    """
    # 插入sql
    insert_sql = """
    INSERT INTO poly (标题, 日期, 摘要, 链接, 图片链接, 内容)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    # 创建表
    cursor.execute(create_table_sql)
    # 检查路径是否存在
    if not os.path.exists('保利集团图片'):
        os.makedirs('保利集团图片')
    base_urls = ['https://www.poly.com.cn/poly/xwdt/jtxw/A044003001.json',
                 'https://www.poly.com.cn/poly/xwdt/szyw/A044003002.json',
                 'https://www.poly.com.cn/poly/xwdt/gzdt/A044003003.json',
                 'https://www.poly.com.cn/poly/xwdt/qyxw/A044003004.json',
                 'https://www.poly.com.cn/poly/xwdt/mtji/A044003005.json']
    for base_url in base_urls:
        # 获取四个栏目的json数据
        r = requests.get(base_url, headers=headers)
        news_datas = r.json()['result']
        # 数据较多，为倒序排列，最新的新闻在最后，循环最后10条新闻
        for news_data in news_datas[-10:]:
            # 根据json数据获取: 标题、日期、摘要、链接、图片链接、内容
            title = news_data['title']
            title = re.sub(r'[^\w\s.-]', '', title)  # 去掉特殊符号
            date = news_data['pubTime']
            source = news_data['desp']
            link = f'https://www.poly.com.cn{news_data["filePath"]}'
            image_url = f'https://www.poly.com.cn{news_data["coverPath"]}'
            # 请求新闻详细页获取内容
            r = requests.get(link, headers=headers)
            html = etree.HTML(r.text)
            content = '\n'.join(html.xpath('//*[@id="BodyLabel"]//text()'))
            print(f'{title}   {date}   {source[:20]}   {link}   {image_url}')
            # 图片保存到本地
            if image_url:
                r = requests.get(image_url, headers=headers)
                with open(f'保利集团图片/{title[:10]}.jpg', 'wb') as news_image:
                    news_image.write(r.content)
            # 数据插入数据库
            cursor.execute(insert_sql, (title, date, source, link, image_url, content))
    # 提交事务
    connect.commit()
    # 关闭游标和连接
    cursor.close()
    connect.close()
