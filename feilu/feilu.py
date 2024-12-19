import time

import pandas as pd
import requests
from lxml import etree
from matplotlib import pyplot as plt

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Cookie': '__jsluid_s=c9bf2381199315a3f9d70fab5efbea9b; __jsl_clearance_s=1718590950.375|0|BNVMH65p0N9580f3nELVxfBlj1g%3D; PHPSESSID=mnnnrrlijttt606feek3bkdvg0; mfw_uuid=666f9de7-be92-5b8a-42db-f09d461618a6; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222024-06-17+10%3A22%3A31%22%3B%7D; __mfwc=direct; __mfwa=1718590951232.55084.1.1718590951232.1718590951232; __mfwlv=1718590951; __mfwvn=1; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1718590951; uva=s%3A150%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1718590952%3Bs%3A10%3A%22last_refer%22%3Bs%3A82%3A%22https%3A%2F%2Fwww.mafengwo.cn%2Flocaldeals%2F0-0-M10132-0-0-0-0-0.html%3Ffrom%3Dlocaldeals_index%22%3Bs%3A5%3A%22rhost%22%3BN%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1718590952%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=666f9de7-be92-5b8a-42db-f09d461618a6; __mfwb=7d6d46205828.2.direct; __mfwlt=1718590972; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1718590973; bottom_ad_status=0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

data = {
    '书名': [],
    '作者': [],
    '总点击量': [],
    '字数': [],
    '简介': [],
}


def create_click_chart():
    item = ['999万-', '1000-1499万', '1500-1999万', '2000-2499万', '2500-2999万', '3000-3499万', '3500-3999万', '4000-4499万', '4500-4999万', '5000万+']
    value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for d in data['总点击量']:
        try:
            if float(d[:-1]) <= 999:
                value[0] += 1
            elif 1000 <= float(d[:-1]) <= 1499:
                value[1] += 1
            elif 1500 <= float(d[:-1]) <= 1999:
                value[2] += 1
            elif 2000 <= float(d[:-1]) <= 2499:
                value[3] += 1
            elif 2500 <= float(d[:-1]) <= 2999:
                value[4] += 1
            elif 3000 <= float(d[:-1]) <= 3499:
                value[5] += 1
            elif 3500 <= float(d[:-1]) <= 3999:
                value[6] += 1
            elif 4000 <= float(d[:-1]) <= 4499:
                value[7] += 1
            elif 4500 <= float(d[:-1]) <= 4999:
                value[8] += 1
            elif float(d[:-1]) >= 5000:
                value[9] += 1
        except:
            continue
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(12, 6))
    plt.bar(item, value)
    plt.title('飞卢小说网书籍总点击量统计条形图')
    plt.xlabel('总点击量')
    plt.ylabel('数量')
    plt.savefig('飞卢小说网书籍总点击量统计条形图.png')


def create_words_chart():
    item = ['99万-', '100-199万', '200-299万', '300-399万', '400-499万', '500万+']
    value = [0, 0, 0, 0, 0, 0]
    for d in data['字数']:
        try:
            if float(d[:-1]) <= 99:
                value[0] += 1
            elif 100 <= float(d[:-1]) <= 199:
                value[1] += 1
            elif 200 <= float(d[:-1]) <= 299:
                value[2] += 1
            elif 300 <= float(d[:-1]) <= 399:
                value[3] += 1
            elif 400 <= float(d[:-1]) <= 499:
                value[4] += 1
            elif float(d[:-1]) >= 500:
                value[5] += 1
        except:
            continue
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(12, 6))
    plt.bar(item, value)
    plt.title('飞卢小说网书籍字数统计条形图')
    plt.xlabel('字数')
    plt.ylabel('数量')
    plt.savefig('飞卢小说网书籍字数统计条形图.png')


if __name__ == '__main__':
    # 这里爬取100页，每页30条数据，共3000条
    for i in range(100):
        # 发送请求
        url = f'https://b.faloo.com/y_0_0_0_0_0_3_{i+1}.html'
        r = requests.get(url, headers=headers)
        print(url)
        time.sleep(3)
        html = etree.HTML(r.text)
        # 根据xpath获取书本列表
        book_list = html.xpath('//*[@id="BookContent"]/div/div')
        for book in book_list:
            # 获取书名、作者、总点击量、字数、简介
            name = book.xpath('.//div[@class="TwoBox02_08"]//a/text()')[0]
            author = book.xpath('.//*[@class="TwoBox02_09"]//a/text()')[0]
            total_clicks = book.xpath('.//span[contains(text(),"总点击")]/text()')[0]
            words = book.xpath('.//span[contains(text(),"字数")]/text()')[0]
            introduce = book.xpath('.//*[@class="TwoBox02_06"]/a/text()')[0]
            # 数据预处理
            name = name.replace('\n', '')
            author = author.replace('\n', '')
            total_clicks = total_clicks.replace('总点击：', '')
            words = words.replace('字数：', '')
            introduce = introduce.replace(' ', '')
            print(f'{name}   {author}   {total_clicks}   {words}   {introduce}')
            # 存入data
            data['书名'].append(name)
            data['作者'].append(author)
            data['总点击量'].append(total_clicks)
            data['字数'].append(words)
            data['简介'].append(introduce)
    df = pd.DataFrame(data)
    df.to_csv('飞卢小说网书籍数据.csv', encoding='utf-8-sig', index=False)
    create_click_chart()
    create_words_chart()