import random
import time

import requests
from lxml import etree

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": "aQQ_ajkguid=9BAF3AF9-2564-17C1-076D-177C21915728; id58=Cr4A2Wd0w7dpT88KFHRTAg==; 58tj_uuid=9b9846cf-e483-409d-9715-ccbcbdce2a27; new_uv=1; _ga=GA1.2.1750036582.1735705535; _gid=GA1.2.43598502.1735705535; _ga_DYBJHZFBX2=GS1.2.1735705535.1.0.1735705535.0.0.0; als=0; ajk-appVersion=; fzq_h=8be96db5c1ed8954d2e7af46884052a8_1735705528786_e1ad2009b506496d9e656cafc8fa9942_1996682534; xxzlclientid=702f9546-005c-4d8a-ac56-1735705538074; xxzlxxid=pfmxwN4IMJwEhsqtaOtsk7Ep14jXZfeE0ywZdUkiOY/x1vIlG91N0A5sLttxDeAQHCha; ctid=48; sessid=0F449804-00D8-4E80-33C6-3D4CEF7ED312; twe=2; seo_source_type=0; ajk_member_verify=vyBaYYPow8YSNkub425%2BnjsMXItxYer3b0hZRvssols%3D; ajk_member_verify2=MjgxMzA2MzIxfHNrVXlGUkV8MQ%3D%3D; fzq_js_anjuke_ershoufang_pc=69a101c92a3a72eb9c78a066b8dae4e9_1735708538066_25; obtain_by=1; ajkAuthTicket=TT=c66709046c03e07f50c26c7ff4b390fb&TS=1735708530429&PBODY=Cwqefp0BVLLvqdhXm_tUcZruBcbsI9pUR09wctu_DhTToPH3sHRd1Cml9H57flNosCF_V8pq2c3O2oapatvLNRNhsDMkFGmS7kKYhwUBga5fFKdLT2uN6eGkoaRYAJyCLQ7W6qyObDgzzBgDSRcDb-ZO_W2yoxbNVEowblDwRu8&VER=2&CUID=ffixV21Kx-RQlOZ0s8aG3hFWXp57TMBP; xxzlbbid=pfmbM3wxMDM0NnwxLjEwLjF8MTczNTcwODUzODU1MDc2OTA3MHxITDIvYkRHcHBWODZsZ2g3Y2NJN3dHMXVRV0xhZ292RXNjVTk3Mk83bnZzPXwxMDU4ZTA1NjMyOWU4ZDE0N2FjMWZlMzc2ZTZiMTU1NF8xNzM1NzA4NTMwMjgyX2FhNTk0MzAxMWNjMTRhODQ4MDQ5OGNlMDc2MGJlZTM3XzE5OTY2ODI1MzR8NGRjZTA3ZGM5Nzk1NzU2MDE1YzIyYjhlZDhhMDA5OWJfMTczNTcwODUzODMyOF8yNTQ=",
    "priority": "u=0, i",
    "referer": "https://heb.anjuke.com/sale/daoli/p3/",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


if __name__ == '__main__':
    base_url = 'https://heb.zu.anjuke.com/fangyuan/'
    r = requests.get(base_url, headers=headers)
    html = etree.HTML(r.text)
    region_urls = html.xpath('//*[@class="sub-items sub-level1"]/a/@href')[1:-1]
    for region_url in region_urls:
        for page in range(10):
            # 发送请求
            page_url = f'{region_url}pg{page + 1}/'
            r = requests.get(page_url, headers=headers)
            print(page_url)
            # time.sleep一下，防止被封ip
            time.sleep(round(random.uniform(3, 10), 2))
            # 转化成HTML格式
            html = etree.HTML(r.text)
            detail_urls = html.xpath('//*[@class="zu-itemmod clearfix"]/@link')
            for detail_url in detail_urls:
                r = requests.get(detail_url, headers=headers)
                time.sleep(round(random.uniform(3, 5), 2))
                html = etree.HTML(r.text)
                try:
                    price = html.xpath('//*[@class="price"]//text()')[0].replace('元/月', '')
                    area = html.xpath('//*[@class="type" and contains(text(),"面积")]/following-sibling::span/b/text()')[0].replace('平方米', '')
                    floor = html.xpath('//*[@class="type" and contains(text(),"楼层")]/following-sibling::span/text()')[0]
                    info = ''.join(html.xpath('//div[./h2[@class="title" and text()="房源概况"]]/following-sibling::div[1]//text()')).replace('\n', '')
                except:
                    print(detail_url)
                print(f'{price}   {area}   {floor}   {info}')
