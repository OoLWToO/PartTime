import random
import time

import pandas
import pandas as pd
import requests
from lxml import etree
from matplotlib import pyplot as plt
from wordcloud import WordCloud


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    'Cookie': 'lianjia_ssid=3306c31a-1748-440a-9360-74e5dd7a5315; lianjia_uuid=62b46ef9-c80b-4d23-b1c3-e6cffb316b19; Hm_lvt_46bf127ac9b856df503ec2dbf942b67e=1734934313; HMACCOUNT=CD82991D93936EF5; _jzqa=1.80855173081169230.1734934313.1734934313.1734934313.1; _jzqc=1; _jzqckmp=1; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22193f224b89719ca-029068245990a3-26031051-1327104-193f224b89821fd%22%2C%22%24device_id%22%3A%22193f224b89719ca-029068245990a3-26031051-1327104-193f224b89821fd%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _ga=GA1.2.2048597721.1734934324; _gid=GA1.2.258617979.1734934324; select_city=500000; _qzjc=1; crosSdkDT2019DeviceId=u8qwx3--ics2qa-2do2pvnnl6yw43t-1othxnu9w; login_ucid=2000000038985323; lianjia_token=2.00125688476a9f3bc003fba1762556ed76; lianjia_token_secure=2.00125688476a9f3bc003fba1762556ed76; security_ticket=LpBQjrCC1R8+sLNVHiJGZLQU+20OyR8uDbpcpcepwrefi+Iq5Xv7dQmXzR686UfB9yZT2041Ddo/nkThh+RMo7a6QwRSDLK4W0+Kz0MjO5vfCBFU9NCvgSvxKZf2ch/JbW4WlTEi/azUIebD7dcS7rrt7EZhRhvLfagN5tCVNZ4=; ftkrc_=3a4595dc-6ef2-434f-8363-f74f1e1b15c0; lfrc_=8ca2b90e-a545-4bbc-9750-dc975b9deffd; _ga_PV625F3L95=GS1.2.1734934814.1.1.1734934868.0.0.0; Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e=1734934876; _qzja=1.1823195102.1734934802967.1734934802967.1734934802967.1734934857700.1734934876092.0.0.0.3.1; _qzjb=1.1734934802967.3.0.0.0; _qzjto=3.1.0; _jzqb=1.5.10.1734934313.1; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiZWQwMTAxNjgwNGRmM2YwMTQzODUyNmQwNmE4Y2Q0NDY4MTM5ZmI4NmQyNTk5ZTg0OWQ3Y2ViYzcxNzlkNmVjNmIxOWQ2OThmNmNiZDE2MmQwZDE0ZGUyODQ4MGQ0NWUyMDIyYmJkYWI1OGMyZWJhMzRkNmNmNDY0MmUyOTA4MmVjNmY3NDA4MTkzNDQzYzdhMTA0ZWI2MjM1Y2YwMzgxNGQ4ODgwMzQ1NmFkNzM3YTIzZTQwYzFhNzJhMDRjZWVjOWVhYmM4ZjRkZjdhMjY2Y2VlOTU2MGVlMjg1YTkxNjYwY2Y1MTdmNmU4ZjI0MDU5Y2FmZjU5YTc5Y2ZmOTFmMlwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI3NTNmM2U4NFwifSIsInIiOiJodHRwczovL2NxLmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvamlhbmdiZWkvcGcyLyIsIm9zIjoid2ViIiwidiI6IjAuMSJ9',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

data = {
    '标题': [],
    '小区名称': [],
    '区域': [],
    '总价（万）': [],
    '单价（元/平方米）': [],
    '房屋户型': [],
    '房屋面积（㎡）': [],
    '朝向': [],
    '装修情况': [],
    '楼层': [],
    '建筑类型': [],
    '关注人数': [],
    '发布时间': [],
    '标签': [],
}


def create_price_chart():
    item = ['199万-', '200-299万', '300-399万', '400-499万', '500-599万', '600-699万', '700-799万', '800-899万', '900-999万',
            '1000万+']
    value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for index, row in df.iterrows():
        try:
            if float(row['总价（万）']) <= 199:
                value[0] += 1
            elif 200 <= float(row['总价（万）']) <= 299:
                value[1] += 1
            elif 300 <= float(row['总价（万）']) <= 399:
                value[2] += 1
            elif 400 <= float(row['总价（万）']) <= 499:
                value[3] += 1
            elif 500 <= float(row['总价（万）']) <= 599:
                value[4] += 1
            elif 600 <= float(row['总价（万）']) <= 699:
                value[5] += 1
            elif 700 <= float(row['总价（万）']) <= 799:
                value[6] += 1
            elif 800 <= float(row['总价（万）']) <= 899:
                value[7] += 1
            elif 900 <= float(row['总价（万）']) <= 999:
                value[8] += 1
            elif float(row['总价（万）']) >= 1000:
                value[9] += 1
        except:
            continue
    plt.clf()
    plt.rcParams['font.family'] = 'Microsoft YaHei'
    plt.figure(figsize=(12, 6))
    plt.bar(item, value)
    plt.title('链家上海在售二手房总价统计条形图')
    plt.xlabel('总价')
    plt.ylabel('数量')
    plt.savefig('链家上海在售二手房总价统计条形图.png')


def create_area_chart():
    item = ['49平米-', '50-59平米', '60-69平米', '70-79平米', '80-89平米', '90-99平米', '100-109平米', '110-119平米',
            '120-129平米',
            '130-139平米', '140-149平米', '150平米+']
    value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for index, row in df.iterrows():
        try:
            if float(row['房屋面积（㎡）']) <= 49:
                value[0] += 1
            elif 50 <= float(row['房屋面积（㎡）']) <= 59:
                value[1] += 1
            elif 60 <= float(row['房屋面积（㎡）']) <= 69:
                value[2] += 1
            elif 70 <= float(row['房屋面积（㎡）']) <= 79:
                value[3] += 1
            elif 80 <= float(row['房屋面积（㎡）']) <= 89:
                value[4] += 1
            elif 90 <= float(row['房屋面积（㎡）']) <= 99:
                value[5] += 1
            elif 100 <= float(row['房屋面积（㎡）']) <= 109:
                value[6] += 1
            elif 110 <= float(row['房屋面积（㎡）']) <= 119:
                value[7] += 1
            elif 120 <= float(row['房屋面积（㎡）']) <= 129:
                value[8] += 1
            elif 130 <= float(row['房屋面积（㎡）']) <= 139:
                value[9] += 1
            elif 140 <= float(row['房屋面积（㎡）']) <= 149:
                value[10] += 1
            elif float(row['房屋面积（㎡）']) >= 150:
                value[11] += 1
        except:
            continue
    plt.clf()
    plt.rcParams['font.family'] = 'Microsoft YaHei'
    plt.figure(figsize=(16, 6))
    plt.bar(item, value)
    plt.title('链家上海在售二手房面积统计条形图')
    plt.xlabel('面积（㎡）')
    plt.ylabel('数量')
    plt.savefig('链家上海在售二手房面积统计条形图.png')


def create_type_chart():
    item = []
    value = []
    for index, row in df.iterrows():
        if row['房屋户型'] in item:
            index = item.index(row['房屋户型'])
            value[index] += 1
        else:
            item.append(row['房屋户型'])
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
    plt.title('链家上海在售二手房房型统计饼图')
    plt.savefig('链家上海在售二手房房型统计饼图.png')


def create_word_chart():
    word_str = ''
    for index, row in df.iterrows():
        word_str += row['标题']
    wc = WordCloud(font_path="simsun.ttc", width=800, height=600, mode="RGBA", background_color=None).generate(word_str)
    plt.imshow(wc, interpolation='bilinear')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.axis("off")
    plt.title('链家上海在售二手房标题统计词云')
    wc.to_file("链家上海在售二手房标题统计词云.png")


def create_scatter_chart():
    x_data = []
    y_data = []
    for index, row in df.iterrows():
        if row['朝向'] in ['东', '南', '西', '北', '东南', '东北', '西南', '西北']:
            x_data.append(row['朝向'])
            y_data.append(float(row['单价（元/平方米）']))
    combined = list(zip(x_data, y_data))
    sorted_combined = sorted(combined, key=lambda x: x[1], reverse=False)
    sorted_item, sorted_value = zip(*sorted_combined)
    # 创建散点图
    plt.figure(figsize=(26, 18))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 创建散点图
    plt.scatter(sorted_item, sorted_value)
    # 添加标题和标签
    plt.title('上海在售二手房朝向与单价散点图')
    plt.xticks(rotation=45)  # 旋转x轴标签，以便更好地显示
    plt.xlabel('朝向')
    plt.ylabel('租金')
    # 保存图表
    plt.savefig(f'链家上海在售二手房朝向与单价散点图')


def create_box_chart():
    total_prices = []
    # 区域标签
    regions = []
    for index, row in df.iterrows():
        if row['区域'] not in regions:
            total_prices.append([])
            regions.append(row['区域'])
        total_prices[regions.index(row['区域'])].append(row['总价（万）'])
    # 创建箱型图
    plt.figure(figsize=(26, 18))
    plt.boxplot(total_prices, labels=regions, patch_artist=True)
    plt.title('不同区域总价箱型图', fontsize=16)
    plt.xlabel('区域', fontsize=14)
    plt.ylabel('总价（万元）', fontsize=14)
    plt.xticks(rotation=90)
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # 添加网格线
    plt.savefig(f'链家上海在售二手房区域与总价箱型图')


def get_data():
    for page in range(35):
        # 发送请求
        url = f'https://sh.lianjia.com/ershoufang/pg{page + 1}/'
        r = requests.get(url, headers=headers)
        print(url)
        # time.sleep一下，防止被封ip
        time.sleep(round(random.uniform(1, 5), 2))
        html = etree.HTML(r.text)
        house_list = html.xpath('//*[@class="sellListContent"]/li')
        for house in house_list:
            # 标题、小区名称、区域、总价（万）、单价（元 / 平方米）、房屋户型、房屋面积（㎡）、朝向、装修情况、楼层、建筑类型、关注人数、发布时间、标签
            title = house.xpath('.//div[@class="title"]/a/text()')[0]
            community_name = house.xpath('.//*[@class="positionInfo"]/a[1]/text()')[0]
            region = house.xpath('.//*[@class="positionInfo"]/a[2]/text()')[0]
            price = house.xpath('.//*[contains(@class,"totalPrice")]/span/text()')[0]
            unit_price = house.xpath('.//*[@class="unitPrice"]/@data-price')[0]
            house_info = house.xpath('.//*[@class="houseInfo"]/text()')[0]
            follow_info = house.xpath('.//*[@class="followInfo"]/text()')[0]
            tag = house.xpath('.//*[@class="tag"]/span/text()')
            # 数据预处理
            house_info = house_info.replace(' ', '').split('|')
            house_type = house_info[0]
            house_area = house_info[1].replace('平米', '')
            towards = house_info[2]
            renovation_situation = house_info[3]
            floor = house_info[4]
            if '年' in house_info[5]:
                building_type = house_info[6]
            else:
                building_type = house_info[5]
            follow_info = follow_info.replace(' ', '').split('/')
            followers_num = follow_info[0]
            publish_time = follow_info[1]
            tag = '|'.join(tag)
            print(f'{title}   {community_name}   {region}   {price}   {unit_price}   {house_type}   '
                  f'{house_area}   {towards}   {renovation_situation}   {floor}   {building_type}   '
                  f'{followers_num}   {publish_time}   {tag}')
            # 存入data
            data['标题'].append(title)
            data['小区名称'].append(community_name)
            data['区域'].append(region)
            data['总价（万）'].append(price)
            data['单价（元/平方米）'].append(unit_price)
            data['房屋户型'].append(house_type)
            data['房屋面积（㎡）'].append(house_area)
            data['朝向'].append(towards)
            data['装修情况'].append(renovation_situation)
            data['楼层'].append(floor)
            data['建筑类型'].append(building_type)
            data['关注人数'].append(followers_num)
            data['发布时间'].append(publish_time)
            data['标签'].append(tag)
    df = pd.DataFrame(data)
    df.to_csv('上海链家在售二手房数据.csv', encoding='utf-8-sig', index=False)


if __name__ == '__main__':
    # get_data()
    df = pandas.read_csv('上海链家在售二手房数据.csv')
    create_price_chart()
    create_area_chart()
    create_type_chart()
    create_word_chart()
    create_scatter_chart()
    create_box_chart()