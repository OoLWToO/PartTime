import pandas as pd
import requests
from lxml import etree
from matplotlib import pyplot as plt

# 设置请求头
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'Hm_lvt_e9daa3d2d6076d2d8ec79d05f050c0d5=1716811706,1716825458; Hm_lvt_029c70397ba7bba8caeb29017c83b8d8=1716811706,1716825458; Hm_lpvt_029c70397ba7bba8caeb29017c83b8d8=1716825462; Hm_lpvt_e9daa3d2d6076d2d8ec79d05f050c0d5=1716825462',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

data = {
    '书名': [],
    '价格': [],
    '作者': [],
    '出版社': [],
    '好评率': [],
    '简介': []
}


def create_price_chart():
    item = ['19元-', '20-29元', '30-39元', '40-49元', '50-59元', '60-69元', '70-79元', '80-89元', '90-99元', '100元+']
    value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for d in data['价格']:
        try:
            if float(d) <= 19:
                value[0] += 1
            elif 20 <= float(d) <= 29:
                value[1] += 1
            elif 30 <= float(d) <= 39:
                value[2] += 1
            elif 40 <= float(d) <= 49:
                value[3] += 1
            elif 50 <= float(d) <= 59:
                value[4] += 1
            elif 60 <= float(d) <= 69:
                value[5] += 1
            elif 70 <= float(d) <= 79:
                value[6] += 1
            elif 80 <= float(d) <= 89:
                value[7] += 1
            elif 90 <= float(d) <= 99:
                value[8] += 1
            elif float(d) >= 100:
                value[9] += 1
        except:
            continue
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(12, 6))
    plt.bar(item, value)
    plt.title('当当网书籍价格统计条形图')
    plt.xlabel('总价')
    plt.ylabel('数量')
    plt.savefig('当当网书籍价格统计条形图.png')


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


def create_star_chart():
    item = ['好评', '中评', '差评']
    value = [0, 0, 0]
    for d in data['价格']:
        try:
            if float(d[:-1]) <= 39:
                value[0] += 1
            elif 40 <= float(d[:-1]) <= 69:
                value[1] += 1
            elif float(d[:-1]) >= 70:
                value[2] += 1
        except:
            continue
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.bar(item, value)
    plt.title('当当网书籍好评率统计条形图')
    plt.xlabel('评价')
    plt.ylabel('数量')
    plt.savefig('当当网书籍好评率统计条形图.png')

if __name__ == '__main__':
    # 爬取50页数据，每页60条数据，共3000条，页数可调最大100
    for page in range(50):
        # 发送请求，用etree转成html
        url = f'https://category.dangdang.com/pg{page + 1}-cp01.49.01.00.00.00.html'
        r = requests.get(url, headers=headers)
        print(url)
        html = etree.HTML(r.text)
        # 根据xpath获取书本列表
        book_list = html.xpath('//*[@class="bigimg"]/li')
        for book in book_list:
            # 获取书名、价格、作者、出版社、店铺、简介
            name = book.xpath('./*[@class="name"]/a/text()')[0]
            price = book.xpath('.//*[@class="search_now_price"]/text()')[0]
            author = book.xpath('.//*[@name="itemlist-author"]/text()')
            try:
                publish = book.xpath('.//*[@name="P_cbs"]/text()')[0]
            except:
                publish = ''
            try:
                star = book.xpath('.//*[@class="search_star_line"]/span/span/@style')[0]
            except:
                star = '0%'
            try:
                introduce = book.xpath('.//*[@class="detail"]/text()')[0]
            except:
                introduce = ''
            # 数据预处理
            name = name.replace(' ', '')
            price = price.replace('¥', '')
            author = '、'.join(author)
            publish = publish.replace(' ', '').replace('\n', '')
            star = star.replace('width:', '').replace(';', '')
            print(f'{name}   {price}   {author}   {publish}   {star}   {introduce}')
            # 存入data
            data['书名'].append(name)
            data['价格'].append(price)
            data['作者'].append(author)
            data['出版社'].append(publish)
            data['好评率'].append(star)
            data['简介'].append(introduce)
    df = pd.DataFrame(data)
    df.to_csv('当当网书籍统计.csv', encoding='utf-8-sig', index=False)
    # create_price_chart()
    # create_publish_chart()
    # create_star_chart()

