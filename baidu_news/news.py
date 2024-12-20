import os
import re

import requests
from lxml import etree
import pymssql

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

username = 'sa'
password = '123456'
database = 'my_database'

if __name__ == '__main__':
    # 链接数据库: server改成你的服务器名, port不要改其参数,user你的用户名, password你的密码, database你的数据库名
    connect = pymssql.connect(host='localhost', server='DESKTOP-IFQ46VM', port='1433', user='sa', password='123456', database='my_database')
    cursor = connect.cursor()
    # 创建表sql
    create_table_sql = """
    IF OBJECT_ID('news', 'U') IS NOT NULL
        DROP TABLE news
    CREATE TABLE news (
        标题 NVARCHAR(255),
        日期 NVARCHAR(255),
        来源 NVARCHAR(255),
        链接 NVARCHAR(255),
        图片链接 NVARCHAR(255),
        内容 NVARCHAR(MAX)
    )
    """
    # 插入sql
    insert_sql = """
    INSERT INTO news (标题, 日期, 来源, 链接, 图片链接, 内容) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    # 创建表
    cursor.execute(create_table_sql)
    # 检查路径是否存在
    if not os.path.exists('新闻图片'):
        os.makedirs('新闻图片')
    # https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=徐念沙&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&goods_entry_switch=1&pn=10
    for page in range(1, 4):
        url = f'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=%E5%BE%90%E5%BF%B5%E6%B2%99&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&goods_entry_switch=1&pn={page * 10}'
        r = requests.get(url, headers=headers)
        html = etree.HTML(r.text)
        # 获取新闻列表遍历
        news_list = html.xpath('//*[@id="content_left"]/div[@id]')
        for news in news_list:
            # 获取标题、日期、来源、链接、图片链接、内容
            title = news.xpath('.//*[contains(@aria-label,"标题")]/@aria-label')[0].replace('标题：', '')
            title = re.sub(r'[^\w\s.-]', '', title)  # 去掉特殊符号
            try:
                date = news.xpath('.//*[contains(@aria-label,"发布于")]/@aria-label')[0].replace('发布于：', '')
            except:
                date = ''
            source = news.xpath('.//*[contains(@aria-label,"新闻来源")]/@aria-label')[0].replace('新闻来源：', '')
            link = news.xpath('.//*[contains(@aria-label,"标题")]/@href')[0]
            try:
                image_url = news.xpath('.//*[@class="c_photo"]//img/@src')[0]
            except:
                image_url = ''
            content = news.xpath('.//*[contains(@aria-label,"摘要")]/@aria-label')[0].replace('摘要', '')
            print(f'{title}   {date}   {source}   {link}   {image_url}   {content}')
            # 图片保存到本地
            if image_url:
                r = requests.get(image_url, headers=headers)
                with open(f'新闻图片/{title[:10]}.png', 'wb') as news_image:
                    news_image.write(r.content)
            # 数据插入数据库
            cursor.execute(insert_sql, (title, date, source, link, image_url, content))
    # 提交事务
    connect.commit()
    # 关闭游标和连接
    cursor.close()
    connect.close()
