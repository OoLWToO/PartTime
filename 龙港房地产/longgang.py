import re

import pandas as pd
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

data = {
    '详细地址': [],
    '区域': [],
    '房型': [],
    '户型': [],
    '面积(㎡)': [],
    '出售价格(万)': [],
    '登记时间': [],
}

if __name__ == '__main__':
    # 设置页数
    for page in range(1, 10):
        url = f'https://www.lgfdcw.com/cs/index.php?userid=&infotype=&dq=&fwtype=&hx=&price01=&price02=&pricetype=&fabuday=&addr=&PageNo={page}'
        r = requests.get(url, headers=headers)
        # 设置编码格式，不然会乱码
        r.encoding = 'gb2312'
        html = etree.HTML(r.text)
        house_list = html.xpath('//*[@name="ershoufang"]/following-sibling::table//tr')
        for house in house_list[1:-1]:
            address = house.xpath('./td[1]//strong/text()')[0]
            region = house.xpath('./td[2]/a/text()')[0]
            room_type = house.xpath('./td[3]/a/text()')[0]
            house_type = house.xpath('./td[4]/a/text()')[0]
            area = house.xpath('./td[5]/text()')[0]
            price = house.xpath('./td[6]//text()')[0]
            registration_time = house.xpath('./td[7]//text()')[0]
            # 数据预处理
            area = re.search(r'\d+', area).group(0)
            try:
                price = re.search(r'\d+', price).group(0)
            except:
                price = '面议'
            registration_time = registration_time.replace('[', '').replace(']', '')
            print(f'{address}   {region}   {room_type}   {house_type}   {area}   {price}   {registration_time}')
            data['详细地址'].append(address)
            data['区域'].append(region)
            data['房型'].append(room_type)
            data['户型'].append(house_type)
            data['面积(㎡)'].append(area)
            data['出售价格(万)'].append(price)
            data['登记时间'].append(registration_time)
    # 转成pandas形式，并存入csv
    df = pd.DataFrame(data)
    df.to_csv('龙港房地产.csv', encoding='utf-8-sig', index=False)
