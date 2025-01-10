import json
import os
import re
import shutil
import time

import pandas as pd
from selenium import webdriver

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
    "orders": [
        {
            "asc": 'false',
            "column": "order_num"
        }
    ],
    "size": 500,
    "tags": [
        {
            "tagNo": "A07",
            "tagName": "SU模型",
            "parentNo": "root",
            "tagLevel": 1,
            "specialShow": 0,
            "searchStatus": 1
        }
    ]
}

info_data = {
    '标题': [],
    '类型': [],
    'SU渲染器': [],
    '格式': [],
    '贴图材质': [],
    '软件版本': [],
    'C4D渲染器': [],
    '文件大小': [],
    '上传时间': [],
    '编号': [],
}


def create_driver():
    chrome_driver_path = '../driver/chromedriver_119.exe'
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=option)
    driver.implicitly_wait(.5)
    driver.maximize_window()
    return driver


if __name__ == '__main__':
    page = 3
    driver = create_driver()
    # 检查路径是否存在
    # if not os.path.exists(f'C4D{page}'):
    #     os.makedirs(f'C4D{page}')
    # for item in os.listdir(f'C4D{page}'):
    #     item_path = os.path.join(f'C4D{page}', item)
    #     if os.path.isfile(item_path) or os.path.islink(item_path):
    #         os.unlink(item_path)
    #     elif os.path.isdir(item_path):
    #         shutil.rmtree(item_path)
    url = 'http://suby.cn/api/anon/subyMaterial/getPageList'
    print(f'正在爬取第{page}页')
    data['current'] = page
    data = json.dumps(data)
    response = requests.post(url=url, data=data, headers=headers)
    records = response.json()['data']['records']
    for record in records:
        print(f'正在爬取第{records.index(record) + 1}条，共{len(records)}条')
        m_id = record['id']
        g_id = record['guid']
        title = record['title'].replace(':', '').replace(' ', '')
        print(title)
        # if not os.path.exists(f'C4D{page}/{title}'):
        #     os.makedirs(f'C4D{page}/{title}')

        # 保存标题图片
        # base_image_url = record['thumbnailUrl']
        # try:
        #     response = requests.get(base_image_url, stream=True)
        # except:
        #     continue
        # with open(f'C4D{page}/{title}/标题图片.jpg', 'wb') as news_image:
        #     news_image.write(response.content)

        # 保存信息
        driver.get(f'http://suby.cn/vip/vipdetail?id={m_id}')
        while True:
            try:
                driver.find_element_by_xpath('//span[text()="VIP登录免费下载"]').text
                break
            except:
                pass
        try:
            ty = driver.find_element_by_xpath('//span[text()="类型:"]/following-sibling::span').text
        except:
            ty = ''
        try:
            su_renderer = driver.find_element_by_xpath('//span[text()="SU渲染器:"]/following-sibling::span').text
        except:
            su_renderer = ''
        try:
            m_format = driver.find_element_by_xpath('//span[text()="格式:"]/following-sibling::span').text
        except:
            m_format = ''
        try:
            texture = driver.find_element_by_xpath('//span[text()="贴图材质:"]/following-sibling::span').text
        except:
            texture = ''
        try:
            soft_version = driver.find_element_by_xpath('//span[text()="贴图材质:"]/following-sibling::span').text
        except:
            soft_version = ''
        try:
            C4D_renderer = driver.find_element_by_xpath('//span[text()="C4D渲染器:"]/following-sibling::span').text
        except:
            C4D_renderer = ''
        file_size = record['materialFilesize']
        upload_time = record['createTime']
        number = record['materialNo']
        print(f'{ty}   {su_renderer}   {m_format}   {texture}   {soft_version}   {C4D_renderer}   {file_size}   {upload_time}   {number}')
        info_data['标题'].append(title)
        info_data['类型'].append(ty)
        info_data['SU渲染器'].append(su_renderer)
        info_data['格式'].append(m_format)
        info_data['贴图材质'].append(texture)
        info_data['软件版本'].append(soft_version)
        info_data['C4D渲染器'].append(C4D_renderer)
        info_data['文件大小'].append(file_size)
        info_data['上传时间'].append(upload_time)
        info_data['编号'].append(number)

        # 保存详细页图片
        # image_list_url = f'http://suby.cn/api/anon/subyMaterial/info/{m_id}'
        # response = requests.get(url=image_list_url, headers=detail_headers)
        # image_urls = re.findall(r'http://[^"\s&]+\.jpg', response.json()['data']['content'])
        # for index, image_url in enumerate(image_urls):
        #     for _ in range(3):
        #         try:
        #             response = requests.get(image_url, stream=True)
        #             break
        #         except:
        #             pass
        #     with open(f'C4D{page}/{title}/图片{index + 1}.jpg', 'wb') as news_image:
        #         news_image.write(response.content)
        if (records.index(record) + 1) % 100 == 0:
            df = pd.DataFrame(info_data)
            df.to_excel(f'素白C4D{page}.xlsx', index=False)
    df = pd.DataFrame(info_data)
    df.to_excel(f'素白C4D{page}.xlsx', index=False)
