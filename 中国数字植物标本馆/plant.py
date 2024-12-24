import os
import random
import time

import pandas as pd
import requests

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "_pk_id.1.2cf1=97efcc58122beac5.1735012618.; _pk_id.43.2cf1=00b8f7f79d47172f.1735012618.; _gid=GA1.3.358840702.1735012618; _pk_ses.1.2cf1=1; _pk_ses.43.2cf1=1; PHPSESSID=o8on9lsprnm7i6qm3iknfs91pl; _gat_gtag_UA_155049937_2=1; _ga_PM9PL6NFJ2=GS1.1.1735022774.2.1.1735028412.0.0.0; _ga=GA1.1.968447662.1735012618",
    "Host": "www.cvh.ac.cn",
    "Referer": "https://www.cvh.ac.cn/spms/list.php?&taxonName=%E6%9D%89%E6%9C%A8&offset=60",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

image_headers = {
    "Origin": "https://image.cvh.ac.cn",
    "Referer": "https://image.cvh.ac.cn/files/l/PE/02091851.jpg",
    "sec-ch-ua": '";Not A Brand";v="99", "Chromium";v="94"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 SE 2.X MetaSr 1.0"
}


data = {
    '代码': [],
    '学名': [],
    '中文名': [],
    '鉴定人': [],
    '鉴定时间': [],
    '采集人': [],
    '采集号': [],
    '采集时间': [],
    '采集地': [],
    '海拔': [],
    '生境': [],
    '习性': [],
    '物候期': [],
}


if __name__ == '__main__':
    # 检查路径是否存在, 如果路径不存, 则创建路径
    if not os.path.exists('图片'):
        os.makedirs('图片')
    # 3787条数据，每页100条，爬取38页
    for page in range(38):
        # 获取植物列表
        url = f'https://www.cvh.ac.cn/controller/spms/list.php?&taxonName=%E6%9D%89%E6%9C%A8&offset={page*100}&limit=100'
        r = requests.get(url, headers=headers)
        rows = r.json()['rows']
        for row in rows:
            collection_id = row['collectionID']
            detail_url = f'https://www.cvh.ac.cn/controller/spms/detail.php?id={collection_id}'
            r = requests.get(detail_url, headers=headers)
            time.sleep(round(random.uniform(3, 10), 2))
            detail_info = r.json()['rows']
            collection_code = detail_info['collectionCode']
            scientific_name = detail_info['formattedName'].replace('<em>', '').replace('</em>', '')
            chinese_name = detail_info['chineseName']
            identified_man = detail_info['identifiedBy']
            identified_time = detail_info['dateIdentified'] if detail_info['dateIdentified'] else ''
            record_man = detail_info['recordedBy']
            record_num = detail_info['recordNumber']
            record_time = detail_info['verbatimEventDate']
            record_position = f'{detail_info["country"]} {detail_info["stateProvince"]}'
            elevation = detail_info['elevation'] if detail_info['elevation'] else ''
            habitat = detail_info['habitat']
            propensity = detail_info['occurrenceRemarks']
            reproductive_condition = detail_info['reproductiveCondition']
            print(f'{collection_code}   {scientific_name}   {chinese_name}   {identified_man}   {identified_time}   {record_man}   '
                  f'{record_num}   {record_time}   {record_position}   {elevation}   {habitat}   {propensity}   {reproductive_condition}')
            data['代码'].append(collection_code)
            data['学名'].append(scientific_name)
            data['中文名'].append(chinese_name)
            data['鉴定人'].append(identified_man)
            data['鉴定时间'].append(identified_time)
            data['采集人'].append(record_man)
            data['采集号'].append(record_num)
            data['采集时间'].append(record_time)
            data['采集地'].append(record_position)
            data['海拔'].append(elevation)
            data['生境'].append(habitat)
            data['习性'].append(propensity)
            data['物候期'].append(reproductive_condition)
            image_url = f'https://image.cvh.ac.cn/files/l/PE/{collection_code}.jpg'
            r = requests.get(image_url, headers=image_headers)
            with open(f'图片/{collection_code}.jpg', 'wb') as news_image:
                news_image.write(r.content)
        df = pd.DataFrame(data)
        df.to_excel('中国数字植物标本馆杉木数据.xlsx', index=False)
