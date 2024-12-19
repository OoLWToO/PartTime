import re
import time
import pandas as pd

import requests
from lxml import etree
from matplotlib import pyplot as plt

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'Hm_lvt_e9daa3d2d6076d2d8ec79d05f050c0d5=1716811706,1716825458; Hm_lvt_029c70397ba7bba8caeb29017c83b8d8=1716811706,1716825458; Hm_lpvt_029c70397ba7bba8caeb29017c83b8d8=1716825462; Hm_lpvt_e9daa3d2d6076d2d8ec79d05f050c0d5=1716825462',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

data = {
    '名称': [],
    '总价': [],
    '每平方单价': [],
    '小区名称': [],
    '地址': [],
    '房型': [],
    '面积': [],
    '朝向': [],
    '楼层': [],
    '建造时间': []
}


def create_area_chart():
    item = ['49平米-', '50-59平米', '60-69平米', '70-79平米', '80-89平米', '90-99平米', '100-109平米', '110-119平米', '120-129平米', '130-139平米', '140-149平米', '150平米+']
    value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    areas = []
    for d in data['面积']:
        areas.append(d.replace('㎡', ''))
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
    plt.title('深圳二手房面积统计条形图')
    plt.xlabel('面积（㎡）')
    plt.ylabel('数量')
    plt.savefig('深圳二手房面积统计条形图.png')


def create_price_chart():
    item = ['99万-', '100-199万', '200-299万', '300-399万', '400-499万', '500-599万', '600-699万', '700-799万', '800-899万', '900-999万', '1000万+']
    value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for d in data['总价']:
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
            elif 500 <= float(d[:-1]) <= 599:
                value[5] += 1
            elif 600 <= float(d[:-1]) <= 699:
                value[6] += 1
            elif 700 <= float(d[:-1]) <= 799:
                value[7] += 1
            elif 800 <= float(d[:-1]) <= 899:
                value[8] += 1
            elif 900 <= float(d[:-1]) <= 999:
                value[9] += 1
            elif float(d[:-1]) >= 1000:
                value[10] += 1
        except:
            continue
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(12, 6))
    plt.bar(item, value)
    plt.title('深圳二手房总价统计条形图')
    plt.xlabel('总价')
    plt.ylabel('数量')
    plt.savefig('深圳二手房总价统计条形图.png')


def create_type_chart():
    item = []
    value = []
    for d in data['房型']:
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
    plt.title('深圳二手房房型统计饼图')
    plt.savefig('深圳二手房房型统计饼图.png')

if __name__ == '__main__':
    # 这里爬取50页，每页60条数据，共3000条，页数可调
    for i in range(50):
        # 发送请求
        url = f'https://sz.58.com/ershoufang/p{i + 1}/'
        print(url)
        r = requests.get(url, headers=headers)
        # 58有反爬，必须要等一会再爬，不然ip很快就给封了
        time.sleep(10)
        # 转化成HTML格式
        html = etree.HTML(r.text)
        house_list = html.xpath('//section[@class="list"]/div')
        for house in house_list:
            # 获取名称、总价、每平方单价、小区名称、地址、房型、面积、朝向、楼层、建造时间
            name = house.xpath('.//*[@class="property-content-title-name"]/text()')[0]
            total_price = ''.join(house.xpath('.//*[@class="property-price-total"]/span/text()'))
            unit_price = house.xpath('.//*[@class="property-price-average"]/text()')[0]
            community_name = house.xpath('.//*[@class="property-content-info-comm-name"]/text()')[0]
            address = '-'.join(house.xpath('.//*[@class="property-content-info-comm-address"]/span/text()'))
            house_type = ''.join(house.xpath('.//*[@class="property-content-info"]/p[1]/span/text()'))
            house_area = house.xpath('.//*[@class="property-content-info"]/p[2]/text()')[0]
            house_facing = house.xpath('.//*[@class="property-content-info"]/p[3]/text()')[0]
            # 根据网站信息，一般都是没有楼层，如果获取不到建造时间，证明楼层为空
            try:
                house_floor = house.xpath('.//*[@class="property-content-info"]/p[4]/text()')[0]
            except:
                house_floor = ''
            try:
                build_time = house.xpath('.//*[@class="property-content-info"]/p[5]/text()')[0]
            except:
                build_time = house_floor
                house_floor = '-'
            # 数据预处理
            unit_price = unit_price.replace(' ', '').replace('\n', '')
            community_name = community_name.replace(' ', '')
            house_area = house_area.replace(' ', '').replace('\n', '')
            house_facing = house_facing.replace(' ', '')
            house_floor = house_floor.replace(' ', '').replace('\n', '')
            build_time = build_time.replace(' ', '').replace('\n', '')
            # 存入data
            data['名称'].append(name)
            data['总价'].append(total_price)
            data['每平方单价'].append(unit_price)
            data['小区名称'].append(community_name)
            data['地址'].append(address)
            data['房型'].append(house_type)
            data['面积'].append(house_area)
            data['朝向'].append(house_facing)
            data['楼层'].append(house_floor)
            data['建造时间'].append(build_time)
            print(f'{name}   {total_price}   {unit_price}   {community_name}   {address}   {house_type}   {house_area}   {house_facing}   {house_floor}   {build_time}')
        # 转成pandas形式，并存入csv
        df = pd.DataFrame(data)
        df.to_csv('58同城深圳二手房数据.csv', encoding='utf-8-sig', index=False)
    create_area_chart()
    create_price_chart()
    create_type_chart()