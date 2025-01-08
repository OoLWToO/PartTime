import json
import os
import re
import shutil

import requests

headers = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Length": "174",
    "Content-Type": "application/json;charset=UTF-8",
    "Host": "suby.cn",
    "Origin": "http://suby.cn",
    "Referer": "http://suby.cn/vip/vipshow",
    "Token": "null",
    "Tokenmode": "2",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

detail_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Host": "suby.cn",
    "Token": "null",
    "Tokenmode": "2",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

data = {
    "current": 1,
    "orders": [
        {
            "asc": 'false',
            "column": "order_num"
        }
    ],
    "size": 500,
    "tags": [
        {
            "tagNo": "A01",
            "tagName": "C4D",
            "parentNo": "root",
            "tagLevel": 1,
            "specialShow": 0,
            "searchStatus": 1
        }
    ]
}

if __name__ == '__main__':
    # 检查路径是否存在
    if not os.path.exists('图片'):
        os.makedirs('图片')
    for item in os.listdir('图片'):
        item_path = os.path.join('图片', item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
    url = 'http://suby.cn/api/anon/subyMaterial/getPageList'
    data = json.dumps(data)
    response = requests.post(url=url, data=data, headers=headers)
    records = response.json()['data']['records']
    for record in records:
        m_id = record['id']
        g_id = record['guid']
        title = record['title']
        os.makedirs(f'图片/{title}')
        # 保存标题图片
        base_image_url = record['thumbnailUrl']
        response = requests.get(base_image_url, stream=True)
        with open(f'图片/{title}/标题图片.jpg', 'wb') as news_image:
            news_image.write(response.content)
        # 保存信息
        info_url = f'http://suby.cn/api/anon/subyMaterialTag/getMaterialTags/{g_id}'
        # info_headers['Referer'] = f'http://suby.cn/vip/vipdetail?id={m_id}'
        # response = requests.get(url=info_url, headers=info_headers)
        # 保存详细页图片
        image_list_url = f'http://suby.cn/api/anon/subyMaterial/info/{m_id}'
        response = requests.get(url=image_list_url, headers=detail_headers)
        image_urls = re.findall(r'http://[^"\s&]+\.jpg', response.json()['data']['content'])
        for index, image_url in enumerate(image_urls):
            response = requests.get(image_url, stream=True)
            with open(f'图片/{title}/图片{index+1}.jpg', 'wb') as news_image:
                news_image.write(response.content)
        print()