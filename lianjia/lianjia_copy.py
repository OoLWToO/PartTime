import random
import time

import pandas as pd
import requests
from lxml import etree
from matplotlib import pyplot as plt

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
    '链接': [],
    '城市': [],
    '位置': [],
    '标题': [],
    '小区名称': [],
    '区域': [],
    '总价（万）': [],
    '单价（元/平方米）': [],
    '房屋户型': [],
    '房屋面积': [],
    '朝向': [],
    '装修情况': [],
    '楼层': [],
    '建筑类型': [],
    '关注人数': [],
    '发布时间': [],
    '标签': [],
}

position_mapping = {
    'cq': '重庆',
    'xa': '西安',
    'jiangbei': '江北',
    'yubei': '渝北',
    'nanan': '南岸',
    'banan': '巴南',
    'shapingba': '沙坪坝',
    'jiulongpo': '九龙坡',
    'yuzhong': '渝中',
    'dadukou': '大渡口',
    'jiangjing': '江津',
    'beibei': '北碚',
    'beilin': '碑林',
    'weiyang': '未央',
    'baqiao': '灞桥',
    'xinchengqu': '新城区',
    'lianhu': '莲湖',
    'changan7': '长安',
    'yanta': '雁塔',
    'xixianxinquxian': '西咸新区（西安）'
}


if __name__ == '__main__':
    # 重庆: 江北，渝北，南岸，巴南，沙坪坝，九龙坡，渝中，大渡口，江津，北碚
    # 西安: 碑林，未央，灞桥，新城区，莲湖，长安，雁塔，西咸新区（西安）
    citys = ['cq', 'xa']
    positions = {
        'cq': ['jiangbei', 'yubei', 'nanan', 'banan', 'shapingba', 'jiulongpo', 'yuzhong', 'dadukou', 'jiangjing', 'beibei'],
        'xa': ['beilin', 'weiyang', 'baqiao', 'xinchengqu', 'lianhu', 'changan7', 'yanta', 'xixianxinquxian']
    }
    for city in citys:
        for position in positions[city]:
            for page in range(25):
                city_name = position_mapping[city]
                position_name = position_mapping[position]
                # 发送请求
                url = f'https://{city}.lianjia.com/ershoufang/{position}/pg{page + 1}/'
                r = requests.get(url, headers=headers)
                print(url)
                # time.sleep一下，防止被封ip
                time.sleep(round(random.uniform(5, 20), 2))
                html = etree.HTML(r.text)
                house_list = html.xpath('//*[@class="sellListContent"]/li')
                for house in house_list:
                    # 标题、小区名称、区域、总价（万）、单价（元 / 平方米）、房屋户型、房屋面积、朝向、装修情况、楼层、建筑类型、关注人数、发布时间、标签
                    title = house.xpath('.//div[@class="title"]/a/text()')[0]
                    community_name = house.xpath('.//*[@class="positionInfo"]/a[1]/text()')[0]
                    area = house.xpath('.//*[@class="positionInfo"]/a[2]/text()')[0]
                    price = house.xpath('.//*[contains(@class,"totalPrice")]/span/text()')[0]
                    unit_price = house.xpath('.//*[@class="unitPrice"]/@data-price')[0]
                    house_info = house.xpath('.//*[@class="houseInfo"]/text()')[0]
                    follow_info = house.xpath('.//*[@class="followInfo"]/text()')[0]
                    tag = house.xpath('.//*[@class="tag"]/span/text()')
                    # 数据预处理
                    house_info = house_info.replace(' ', '').split('|')
                    house_type = house_info[0]
                    house_area = house_info[1]
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
                    print(f'{city_name}   {position_name}   {title}   {community_name}   {area}   {price}   {unit_price}   '
                          f'{house_type}   {house_area}   {towards}   {renovation_situation}   {floor}   {building_type}   '
                          f'{followers_num}   {publish_time}   {tag}')
                    # 存入data
                    data['链接'].append(url)
                    data['城市'].append(city_name)
                    data['位置'].append(position_name)
                    data['标题'].append(title)
                    data['小区名称'].append(community_name)
                    data['区域'].append(area)
                    data['总价（万）'].append(price)
                    data['单价（元/平方米）'].append(unit_price)
                    data['房屋户型'].append(house_type)
                    data['房屋面积'].append(house_area)
                    data['朝向'].append(towards)
                    data['装修情况'].append(renovation_situation)
                    data['楼层'].append(floor)
                    data['建筑类型'].append(building_type)
                    data['关注人数'].append(followers_num)
                    data['发布时间'].append(publish_time)
                    data['标签'].append(tag)
            df = pd.DataFrame(data)
            df.to_csv('链家在售二手房数据.csv', encoding='utf-8-sig', index=False)
