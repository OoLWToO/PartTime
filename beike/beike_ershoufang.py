import time

import re
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
    '名称': [],
    '位置': [],
    '总价': [],
    '每平方单价': [],
    '介绍': [],
}


def create_area_chart():
    item = ['49平米-', '50-59平米', '60-69平米', '70-79平米', '80-89平米', '90-99平米', '100-109平米', '110-119平米', '120-129平米', '130-139平米', '140-149平米', '150平米+']
    value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    areas = []
    for d in data['介绍']:
        match = re.search(r'(\d+\.\d+平米)', d)
        if match:
            areas.append(match.group().replace('平米', ''))
    for area in areas:
        try:
            if float(area) <= 49:
                value[0] += 1
            elif 50 <= float(area) <= 59:
                value[1] += 1
            elif 60 <= float(area) <= 69:
                value[2] += 1
            elif 70 <= float(area) <= 79:
                value[3] += 1
            elif 80 <= float(area) <= 89:
                value[4] += 1
            elif 90 <= float(area) <= 99:
                value[5] += 1
            elif 100 <= float(area) <= 109:
                value[6] += 1
            elif 110 <= float(area) <= 119:
                value[7] += 1
            elif 120 <= float(area) <= 129:
                value[8] += 1
            elif 130 <= float(area) <= 139:
                value[9] += 1
            elif 140 <= float(area) <= 149:
                value[10] += 1
            elif float(area) >= 150:
                value[11] += 1
        except:
            continue
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(16, 6))
    plt.bar(item, value)
    plt.title('大连二手房面积统计条形图')
    plt.xlabel('面积（㎡）')
    plt.ylabel('数量')
    plt.savefig('大连二手房面积统计条形图.png')


def create_price_chart():
    item = ['49万-', '50-59万', '60-69万', '70-79万', '80-89万', '90-99万', '100-109万', '110-119万', '120-129万', '130-139万', '140-149万', '150万+']
    value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for d in data['总价']:
        try:
            if float(d) <= 49:
                value[0] += 1
            elif 50 <= float(d) <= 59:
                value[1] += 1
            elif 60 <= float(d) <= 69:
                value[2] += 1
            elif 70 <= float(d) <= 79:
                value[3] += 1
            elif 80 <= float(d) <= 89:
                value[4] += 1
            elif 90 <= float(d) <= 99:
                value[5] += 1
            elif 100 <= float(d) <= 109:
                value[6] += 1
            elif 110 <= float(d) <= 119:
                value[7] += 1
            elif 120 <= float(d) <= 129:
                value[8] += 1
            elif 130 <= float(d) <= 139:
                value[9] += 1
            elif 140 <= float(d) <= 149:
                value[10] += 1
            elif float(d) >= 150:
                value[11] += 1
        except:
            continue
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(12, 6))
    plt.bar(item, value)
    plt.title('大连二手房总价统计条形图')
    plt.xlabel('总价')
    plt.ylabel('数量')
    plt.savefig('大连二手房总价统计条形图.png')


def create_type_chart():
    item = []
    value = []
    house_type = []
    for d in data['介绍']:
        match = re.search(r'(\d+室\d+厅)', d)
        if match:
            house_type.append(match.group())
    for d in house_type:
        if d in item:
            index = item.index(d)
            value[index] += 1
        else:
            item.append(d)
            value.append(1)
    combined = list(zip(item, value))
    sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)
    sorted_item, sorted_value = zip(*sorted_combined)
    # 将第七个以后整合成'其他'
    sorted_item = tuple(list(sorted_item[:7]) + ['其他'])
    sorted_value = tuple(list(sorted_value[:7]) + [sum(sorted_value[7:])])
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.pie(sorted_value, labels=sorted_item, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('大连二手房房型统计饼图')
    plt.savefig('大连二手房房型统计饼图.png')

if __name__ == '__main__':
    # 这里爬取100页，每页30条数据，共3000条
    for i in range(100):
        # 发送请求
        url = f'https://dl.ke.com/ershoufang/pg{i + 1}/'
        r = requests.get(url, headers=headers)
        print(url)
        time.sleep(2)
        # 转化成HTML格式
        html = etree.HTML(r.text)
        house_xpath = '//*[@class="sellListContent"]'
        # 获取名称、位置、总价、每平方单价、介绍数据
        name = html.xpath(f'{house_xpath}//*[@class="title"]/a/@title')
        position = html.xpath(f'{house_xpath}//*[@class="positionInfo"]/a/text()')
        price = html.xpath(f'{house_xpath}//*[@class="totalPrice totalPrice2"]/span/text()')
        unit_price = html.xpath(f'{house_xpath}//*[@class="unitPrice"]/span/text()')
        # 数据预处理
        price = [string.replace(' ', '') for string in price]
        info = html.xpath(f'{house_xpath}//*[@class="houseInfo"]/text()')
        info = [string.replace('\n', '').replace(' ', '') for string in info]
        info = [x for x in info if x != '']
        for j in range(30):
            print(f'{name[j]}   {position[j]}   {price[j]}  {unit_price[j]}   {info[j]}')
            # 存入data
            data['名称'].append(name[j])
            data['位置'].append(position[j])
            data['总价'].append(price[j])
            data['每平方单价'].append(unit_price[j])
            data['介绍'].append(info[j])
            data['介绍'].append(info[j])
    df = pd.DataFrame(data)
    df.to_csv('贝壳大连二手房数据.csv', encoding='utf-8-sig', index=False)
    create_area_chart()
    create_price_chart()
    create_type_chart()
