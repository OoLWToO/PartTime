import time
from datetime import datetime

import pandas as pd
import requests
from lxml import etree
from matplotlib import pyplot as plt
from wordcloud import WordCloud

# 设置请求头
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': '__permanent_id=20241216144216388783570476774906337; dangdang.com=email=MTg2NjU0NDg0NzI4MDg5MEBkZG1vYmlscGhvbmVfX3VzZXIuY29t&nickname=&display_id=4766850823709&customerid=pHb+Fh5jzxhaYY5fEB+3EA==&viptype=ayHYXk7x4cc=&show_name=186****8472; __visit_id=20241220163438756375720133582533937; __out_refer=; secret_key=22f3133e23d4f3adee29f838b4af8e2a; MDD_channelId=70000; MDD_fromPlatform=307; producthistoryid=1901349244; ddscreen=2; dest_area=country_id%3D9000%26province_id%3D111%26city_id%3D0%26district_id%3D0%26town_id%3D0; pos_9_end=1734683971912; pos_0_end=1734683972071; ad_ids=3618801%7C%231; pos_0_start=1734683981904; sessionID=pc_9acc76d9a2892b72577dbf62dcd3b8023636c5f0cbc251e6d0a8f5bbce01dd3e; USERNUM=31L5l/h0tGSDYvFwilByaQ==; login.dangdang.com=.ASPXAUTH=fIDHc6OZ19F19nnaQ93AvozkhkvUjGacGaHuev/d2xvcUHPGfN2NHw==; ddoy=email=1866544847280890@ddmobilphone__user.com&nickname=&validatedflag=0&uname=&utype=1&.ALFG=off&.ALTM=1734684008570; LOGIN_TIME=1734684009378; pos_6_end=1734684057238; pos_6_start=1734684057354; __trace_id=20241220164059903172719220825530478; __rpm=%7Cp_21055821.comment_long_body..1734684065159',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

data = {
    '书名': [],
    '评论数': [],
    '推荐比例': [],
    '作者': [],
    '出版时间': [],
    '出版社': [],
    '现价': [],
    '原价': [],
    '折扣': []
}


def create_physical_price_chart():
    item = ['9元-', '10-19元', '20-29元', '30-39元', '40-49元', '50-59元', '60-69元', '70-79元', '80-89元', '90元+']
    value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for d in data['现价']:
        try:
            if float(d) <= 9:
                value[0] += 1
            elif 10 <= float(d) <= 19:
                value[1] += 1
            elif 20 <= float(d) <= 29:
                value[2] += 1
            elif 30 <= float(d) <= 39:
                value[3] += 1
            elif 40 <= float(d) <= 49:
                value[4] += 1
            elif 50 <= float(d) <= 59:
                value[5] += 1
            elif 60 <= float(d) <= 69:
                value[6] += 1
            elif 70 <= float(d) <= 79:
                value[7] += 1
            elif 80 <= float(d) <= 89:
                value[8] += 1
            elif float(d) >= 90:
                value[9] += 1
        except:
            continue
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(12, 6))
    plt.bar(item, value)
    plt.title('当当网书籍现价统计条形图')
    plt.xlabel('价格')
    plt.ylabel('数量')
    plt.savefig('当当网书籍现价统计条形图.png')


def create_original_price_chart():
    item = ['9元-', '10-19元', '20-29元', '30-39元', '40-49元', '50-59元', '60-69元', '70-79元', '80-89元', '90元+']
    value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for d in data['原价']:
        try:
            if float(d) == 0:
                continue
            if float(d) <= 9:
                value[0] += 1
            elif 10 <= float(d) <= 19:
                value[1] += 1
            elif 20 <= float(d) <= 29:
                value[2] += 1
            elif 30 <= float(d) <= 39:
                value[3] += 1
            elif 40 <= float(d) <= 49:
                value[4] += 1
            elif 50 <= float(d) <= 59:
                value[5] += 1
            elif 60 <= float(d) <= 69:
                value[6] += 1
            elif 70 <= float(d) <= 79:
                value[7] += 1
            elif 80 <= float(d) <= 89:
                value[8] += 1
            elif float(d) >= 90:
                value[9] += 1
        except:
            continue
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(12, 6))
    plt.bar(item, value)
    plt.title('当当网书籍原价统计条形图')
    plt.xlabel('价格')
    plt.ylabel('数量')
    plt.savefig('当当网书籍原价统计条形图.png')


def create_publish_chart():
    item = []
    value = []
    for d in data['出版社']:
        if d in item:
            index = item.index(d)
            value[index] += 1
        else:
            item.append(d)
            value.append(1)
    combined = list(zip(item, value))
    sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)
    sorted_item, sorted_value = zip(*sorted_combined)
    # 将第九个以后整合成'其他'
    sorted_item = tuple(list(sorted_item[:9]) + ['其他'])
    sorted_value = tuple(list(sorted_value[:9]) + [sum(sorted_value[9:])])
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(12, 12))
    plt.pie(sorted_value, labels=sorted_item, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('当当网书籍出版社统计饼图')
    plt.savefig('当当网书籍出版社统计饼图.png')


def create_word_chart():
    comment_str = ''
    for page in range(30):
        print(f'正在爬取第{page + 1}页评论...')
        url = f'https://product.dangdang.com/index.php?r=comment%2Flist&productId=21055821&categoryPath=01.05.16.00.00.00&mainProductId=21055821&mediumId=0&pageIndex={page + 1}&sortType=1&filterType=1&isSystem=1&tagId=0&tagFilterCount=0&template=publish&long_or_short=short'
        r = requests.get(url, headers=headers)
        time.sleep(5)
        # 这里报错了可能是有验证码了，进到https://product.dangdang.com/21055821.html进行手动验证
        html = etree.HTML(r.json()['data']['list']['html'])
        for comment in html.xpath('//*[@class="describe_detail"]/span/a/text()'):
            comment_str += comment
    wc = WordCloud(font_path="simsun.ttc", width=800, height=600, mode="RGBA", background_color=None).generate(
        comment_str)
    plt.imshow(wc, interpolation='bilinear')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.axis("off")
    plt.title('《我与地坛》评论统计词云')
    wc.to_file("《我与地坛》评论统计词云.png")


def getData():
    # 设置月份
    for month in range(1, 12):
        # 爬取25页数据，每页20条数据，共500条
        for page in range(25):
            # 发送请求，用etree转成html
            url = f'http://bang.dangdang.com/books/ebooks/98.01.00.00.00.00-month-2024-11-1-{page + 1}'
            r = requests.get(url, headers=headers)
            print(url)
            html = etree.HTML(r.text)
            # 根据xpath获取书本列表
            book_list = html.xpath('//*[@class="bang_list_box"]//*[contains(@class,"bang_list")]/li')
            for book in book_list:
                # 获取书名、评论数、推荐比例、作者、出版时间、出版社、现价、原价、折扣、电子书价格
                name = book.xpath('./*[@class="name"]/a/@title')[0]
                comment_num = book.xpath('./*[@class="star"]/a/text()')[0]
                recommended_ratio = book.xpath('.//*[@class="tuijian"]/text()')[0]
                try:
                    author = book.xpath('./*[@class="publisher_info"][1]/a[1]/@title')[0]
                except:
                    author = ''
                try:
                    publish_time = book.xpath('./*[@class="publisher_info"][2]/span/text()')[0]
                    # 格式化日期
                    date_obj = datetime.strptime(publish_time, "%Y-%m-%d")
                    publish_time = date_obj.strftime("%Y年%m月%d日")
                except:
                    publish_time = ''
                try:
                    publish_house = book.xpath('./*[@class="publisher_info"][2]/a/text()')[0]
                except:
                    publish_house = ''
                physical_price_now = book.xpath('./*[@class="price"]/p[1]//span[@class="price_n"]/text()')[0]
                physical_price_original = book.xpath('./*[@class="price"]/p[1]//span[@class="price_r"]/text()')[0]
                physical_price_discount = book.xpath('./*[@class="price"]/p[1]//span[@class="price_s"]/text()')[0]
                # 数据预处理
                name = name.replace(' ', '')
                comment_num = comment_num.replace('条评论', '')
                recommended_ratio = recommended_ratio.replace('推荐', '')
                physical_price_now = physical_price_now.replace('¥', '')
                physical_price_original = physical_price_original.replace('¥', '')
                physical_price_discount = physical_price_discount.replace('折', '')
                saveData(name, comment_num, recommended_ratio, author, publish_time, publish_house, physical_price_now,
                         physical_price_original, physical_price_discount)


def saveData(name, comment_num, recommended_ratio, author, publish_time, publish_house, physical_price_now,
             physical_price_original, physical_price_discount):
    print(f'{name}   {comment_num}   {recommended_ratio}   {author}   {publish_time}   {publish_house}   '
          f'{physical_price_now}   {physical_price_original}   {physical_price_discount}')
    # 存入data
    data['书名'].append(name)
    data['评论数'].append(comment_num)
    data['推荐比例'].append(recommended_ratio)
    data['作者'].append(author)
    data['出版时间'].append(publish_time)
    data['出版社'].append(publish_house)
    data['现价'].append(physical_price_now)
    data['原价'].append(physical_price_original)
    data['折扣'].append(physical_price_discount)


if __name__ == '__main__':
    getData()
    df = pd.DataFrame(data)
    df.to_excel('当当网2024年1-11月top500电子书统计.xlsx', index=False)
    create_physical_price_chart()
    create_original_price_chart()
    create_publish_chart()
    create_word_chart()
