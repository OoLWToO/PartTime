import csv

import requests
from lxml import etree
import re

from matplotlib import pyplot as plt
from wordcloud import WordCloud

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Host': 'dg.zu.ke.com',
    'referer': '',
    'sec-ch-ua': '\'Google Chrome\';v=\'131\', \'Chromium\';v=\'131\', \'Not_A Brand\';v=\'24\'',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '\'Windows\'',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'Cookie': '__jsluid_s=c9bf2381199315a3f9d70fab5efbea9b; __jsl_clearance_s=1718590950.375|0|BNVMH65p0N9580f3nELVxfBlj1g%3D; PHPSESSID=mnnnrrlijttt606feek3bkdvg0; mfw_uuid=666f9de7-be92-5b8a-42db-f09d461618a6; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222024-06-17+10%3A22%3A31%22%3B%7D; __mfwc=direct; __mfwa=1718590951232.55084.1.1718590951232.1718590951232; __mfwlv=1718590951; __mfwvn=1; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1718590951; uva=s%3A150%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1718590952%3Bs%3A10%3A%22last_refer%22%3Bs%3A82%3A%22https%3A%2F%2Fwww.mafengwo.cn%2Flocaldeals%2F0-0-M10132-0-0-0-0-0.html%3Ffrom%3Dlocaldeals_index%22%3Bs%3A5%3A%22rhost%22%3BN%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1718590952%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=666f9de7-be92-5b8a-42db-f09d461618a6; __mfwb=7d6d46205828.2.direct; __mfwlt=1718590972; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1718590973; bottom_ad_status=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}


def create_area_chart(data):
    item = ['49平米-', '50-69平米', '70-89平米', '90-109平米', '110-129平米', '130-149平米', '150平米+']
    value = [0, 0, 0, 0, 0, 0, 0]
    for d in data:
        if float(d) <= 49:
            value[0] += 1
        elif 50 <= float(d) <= 69:
            value[1] += 1
        elif 70 <= float(d) <= 89:
            value[2] += 1
        elif 90 <= float(d) <= 109:
            value[3] += 1
        elif 110 <= float(d) <= 129:
            value[4] += 1
        elif 130 <= float(d) <= 149:
            value[5] += 1
        elif float(d) >= 150:
            value[6] += 1
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(10, 6))
    plt.bar(item, value)
    plt.title('东莞租房面积统计条形图')
    plt.xlabel('面积（㎡）')
    plt.ylabel('数量')
    plt.savefig('东莞租房面积统计条形图.png')


def create_price_chart(data):
    item = ['0-999', '1000-1999', '2000-2999', '3000-3999', '4000-4999', '5000-5999', '6000-6999', '7000-7999',
            '8000-8999', '9000-9999']
    value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for d in data:
        try:
            if float(d) <= 999:
                value[0] += 1
            elif 1000 <= float(d) <= 1999:
                value[1] += 1
            elif 2000 <= float(d) <= 2999:
                value[2] += 1
            elif 3000 <= float(d) <= 3999:
                value[3] += 1
            elif 4000 <= float(d) <= 4999:
                value[4] += 1
            elif 5000 <= float(d) <= 5999:
                value[5] += 1
            elif 6000 <= float(d) <= 6999:
                value[6] += 1
            elif 7000 <= float(d) <= 7999:
                value[7] += 1
            elif 8000 <= float(d) <= 8999:
                value[8] += 1
            elif 9000 <= float(d) <= 9999:
                value[9] += 1
        except:
            continue
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(10, 6))
    plt.bar(item, value)
    plt.title('东莞租房租金统计条形图')
    plt.xlabel('价格（元/月）')
    plt.ylabel('数量')
    plt.savefig('东莞租房租金统计条形图.png')


def create_type_chart(data):
    item = []
    value = []
    for d in data:
        if d in item:
            index = item.index(d)
            value[index] += 1
        else:
            item.append(d)
            value.append(1)
    combined = list(zip(item, value))
    sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)
    sorted_item, sorted_value = zip(*sorted_combined)
    sorted_item = tuple(list(sorted_item[:8]) + ['其他'])
    sorted_value = tuple(list(sorted_value[:8]) + [sum(sorted_value[8:])])
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.pie(sorted_value, labels=sorted_item, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('东莞租房房型统计饼图')
    plt.savefig('东莞租房房型统计饼图.png')


def create_word_chart(tag_data):
    word_str = ''
    for tag in tag_data:
        word_str += tag
    wc = WordCloud(font_path="simsun.ttc", width=800, height=600, mode="RGBA", background_color=None).generate(word_str)
    plt.imshow(wc, interpolation='bilinear')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.axis("off")
    plt.title('东莞租房标签统计词云')
    wc.to_file("东莞租房标签统计词云.png")


def create_scatter_chart(table_name, data1, data2):
    clean_data1 = []
    clean_data2 = []
    for i in range(100):
        if '-' not in data2[i]:
            clean_data1.append(data1[i])
            clean_data2.append(round(float(data2[i]), 0))
    combined = list(zip(clean_data1, clean_data2))
    sorted_combined = sorted(combined, key=lambda x: x[1], reverse=False)
    sorted_item, sorted_value = zip(*sorted_combined)
    # 创建散点图
    plt.figure(figsize=(26, 18))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 创建散点图
    plt.scatter(sorted_item, sorted_value)
    # 添加标题和标签
    plt.title(table_name)
    plt.xticks(rotation=45)  # 旋转x轴标签，以便更好地显示
    plt.xlabel(table_name)
    plt.ylabel('租金')
    # 保存图表
    plt.savefig(f'东莞租房{table_name}与租金散点图')


if __name__ == '__main__':
    area_data = []
    house_type_data = []
    price_data = []
    tag_data= []
    with open('贝壳东莞租房数据.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['标题', '房源', '面积', '朝向', '房型', '租金', '标签'])
    # 这里爬取100页，每页30条数据，共3000条
    for i in range(5):
        # 发送请求
        url = f'https://dg.zu.ke.com/zufang/pg{i + 1}/'
        headers["referer"] = url
        r = requests.get(url, headers=headers)
        print(url)
        # 转化成HTML格式
        html = etree.HTML(r.text)
        house_list = html.xpath('//*[@class="content__list--item"]')
        for house in house_list:
            # 获取标题、房源、面积、朝向、房型、租金、标签
            name = house.xpath('.//*[contains(@class,"title")]/a/text()')[0]
            house_info = ''.join(house.xpath('.//*[@class="content__list--item--des"]//text()'))
            price = house.xpath('.//*[@class="content__list--item-price"]/em/text()')[0]
            tag = '|'.join(house.xpath('.//*[@class="content__list--item--bottom oneline"]/i/text()'))
            try:
                house_source = house.xpath('.//*[@class="brand"]/text()')[0]
            except:
                house_source = ''
            # 数据预处理
            name = name.replace('\n', '').replace(' ', '')
            house_area_match = re.search(r'(\d+\.\d+)\s*㎡', house_info)
            if house_area_match:
                house_area = house_area_match.group(1)
            else:
                house_area = ''
            house_facing_match = re.search(r'[东南西北]+', house_info)
            if house_facing_match:
                house_facing = house_facing_match.group(0)
            else:
                house_facing = ''
            house_type_match = re.search(r'\d+室\d+厅\d+卫', house_info)
            if house_type_match:
                house_type = house_type_match.group(0)
            else:
                house_type = ''
            house_source = house_source.replace('\n', '').replace(' ', '')
            with open('贝壳东莞租房数据.csv', 'a', encoding='utf-8-sig', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([name, house_source, house_area, house_facing, house_type, price, tag])
            area_data.append(house_area)
            house_type_data.append(house_type)
            price_data.append(price)
            tag_data.append(tag)
            print(f'{name}   {house_source}   {house_area}   {house_facing}   {house_type}   {price}   {tag}')
    # 可视化数据
    create_area_chart(area_data)
    create_price_chart(price_data)
    create_type_chart(house_type_data)
    create_word_chart(tag_data)
    create_scatter_chart('面积', area_data, price_data)
    create_scatter_chart('房型', house_type_data, price_data)
