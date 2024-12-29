import random
import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
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
    'Cookie': 'lianjia_uuid=6f006fa1-6eca-467a-a506-9ba73db0d28c; crosSdkDT2019DeviceId=-yrjp1r-sbyxd0-czwdv7rmys0ug2t-37ieceqbd; ftkrc_=bac7d312-8a09-4b70-94ef-2afc76f73db6; lfrc_=55c625bb-0592-4564-bfba-acac6b870952; _ga=GA1.2.1019673696.1735353903; _ga_EYZV9X59TQ=GS1.2.1735353903.1.1.1735354091.0.0.0; _ga_DX18CJBZRT=GS1.2.1735353903.1.1.1735354091.0.0.0; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221940b26d4441852-093bea2540e941-26011851-3686400-1940b26d4452988%22%2C%22%24device_id%22%3A%221940b26d4441852-093bea2540e941-26011851-3686400-1940b26d4452988%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _jzqx=1.1735353881.1735354907.2.jzqsr=clogin%2Elianjia%2Ecom|jzqct=/.jzqsr=cq%2Elianjia%2Ecom|jzqct=/ershoufang/nanan/; _ga_PV625F3L95=GS1.2.1735354126.1.1.1735355296.0.0.0; lianjia_ssid=c0e493de-63d3-48f8-982f-58f6ad712196; Hm_lvt_46bf127ac9b856df503ec2dbf942b67e=1735353881,1735354907,1735456312; HMACCOUNT=53BEF1F68DC70C31; _jzqa=1.4172086402817953000.1735353881.1735354907.1735456312.3; _jzqc=1; _jzqckmp=1; select_city=440300; _qzjc=1; _gid=GA1.2.68208787.1735456332; _ga_C4R21H79WC=GS1.2.1735456331.1.0.1735456331.0.0.0; login_ucid=2000000038985323; lianjia_token=2.0010d808e36811bb64017521d22b8d897d; lianjia_token_secure=2.0010d808e36811bb64017521d22b8d897d; security_ticket=cKOHLGnFgF+GgWDHLHbHDwwjrSL/7qsCDcephteXai/esl07+H6mA8LQODAWwn/YCVHXVn3AcR4cNhjp+MkbRzPdsc2T2cnGiHfd5XYf+X+RryXwfZMXPE+uCX1fzhdbhaFLb1gaDg/SxwsvR45OBFuGetLots7MH3SUCL8OtbY=; _qzja=1.741976075.1735456318914.1735456318914.1735456318914.1735456318914.1735456514551.0.0.0.2.1; _qzjb=1.1735456318914.2.0.0.0; _qzjto=2.1.0; _jzqb=1.4.10.1735456312.1; Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e=1735456515; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiYTE4ODAxNTk3YWY0MzdiYWUzMDhlYWFmMDlhOTU1ZDViOWUwZDQ1ZGIwNTViNTVjMmY4M2VhY2E4NWI1NjVmYmUwNzJiN2ZjOTBiZjFiYzJlNzM4MjMzMzA5Mjk3ZjY1Y2JmYTY4MWUzMDY2NmYzNTM1MDI5YjBlNzg2MDdhZTE2ZThhMGE3NThhNDZmYTM2MTgzNDQ5OTlhNzVmM2QzMTZhZTQ0ZmQyMmQzNmNmYmVmNGZiNWQ4YTMzZmFlNDE5M2IzYTM4N2ZjZmZlMDY2MDEwYWFkYTVhZGQxMGIzZWJiNGI1NDA5NTE0ZjU5YzNmOGEyZGRmMDhlYzRkMGJjOVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI2YWJkNDdjZFwifSIsInIiOiJodHRwczovL3N6LmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvcGc2LyIsIm9zIjoid2ViIiwidiI6IjAuMSJ9',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

data = {
    '标题': [],
    '总价': [],
    '单价': [],
    '地址': [],
    '信息': [],
    '标签': []
}


def create_area_chart():
    item = ['49平米-', '50-59平米', '60-69平米', '70-79平米', '80-89平米', '90-99平米', '100-109平米', '110-119平米', '120-129平米',
            '130-139平米', '140-149平米', '150平米+']
    value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    areas = []
    for d in data['信息']:
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
    plt.title('链家深圳在售二手房面积统计条形图')
    plt.xlabel('面积（㎡）')
    plt.ylabel('数量')
    plt.savefig('链家深圳在售二手房面积统计条形图.png')


def create_price_chart():
    item = ['99万-', '100-119万', '120-139万', '300-399万', '400-499万', '500-599万', '600-699万', '700-799万', '800-899万',
            '900-999万', '200万+']
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
    plt.title('链家深圳在售二手房总价统计条形图')
    plt.xlabel('总价')
    plt.ylabel('数量')
    plt.savefig('链家深圳在售二手房总价统计条形图.png')


def create_type_chart():
    item = []
    value = []
    house_type = []
    for d in data['信息']:
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
    plt.title('链家深圳在售二手房房型统计饼图')
    plt.savefig('链家深圳在售二手房房型统计饼图.png')
    
def create_word_chart():
    word_str = ''
    for d in data['标题']:
        word_str += d
    wc = WordCloud(font_path="simsun.ttc", width=800, height=600, mode="RGBA", background_color=None).generate(word_str)
    plt.imshow(wc, interpolation='bilinear')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.axis("off")
    plt.title('链家深圳在售二手房标题统计词云')
    wc.to_file("链家深圳在售二手房标题统计词云.png")

if __name__ == '__main__':
    for i in range(100):
        # 发送请求
        url = f'https://sz.lianjia.com/ershoufang/pg{i + 1}/'
        r = requests.get(url, headers=headers)
        print(url)
        # time.sleep一下，防止被封ip
        time.sleep(round(random.uniform(5, 20), 2))
        soup = BeautifulSoup(r.content, 'html.parser')
        # 根据class获取房屋列表
        house_list = soup.find_all('li', class_='clear')
        for house in house_list:
            # 获取标题、总价、单价、地址、信息、标签
            title = house.find('div', class_='title').a.text
            price = house.find('div', class_='totalPrice totalPrice2').span.text
            unit_price = house.find('div', class_='unitPrice').span.text
            address = [x.text for x in house.find('div', class_='positionInfo').find_all('a')]
            info = house.find('div', class_='houseInfo').text
            tag = [x.text for x in house.find('div', class_='tag').find_all('span')]
            # 数据预处理
            title = title.strip()
            price = f'{price}万'
            address = '-'.join(address)
            tag = '/'.join(tag)
            print(f'{title}   {price}   {unit_price}   {address}   {info}   {tag}')
            # 存入data
            data['标题'].append(title)
            data['总价'].append(price)
            data['单价'].append(unit_price)
            data['地址'].append(address)
            data['信息'].append(info)
            data['标签'].append(tag)
    df = pd.DataFrame(data)
    df.to_csv('链家深圳在售二手房数据.csv', encoding='utf-8-sig', index=False)
    create_area_chart()
    create_price_chart()
    create_type_chart()
    create_word_chart()
