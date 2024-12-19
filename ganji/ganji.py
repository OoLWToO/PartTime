import time

import pandas as pd
import requests
from lxml import etree

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
    '岗位类型': [],
    '薪资': [],
    '福利': [],
    '公司': [],
    '地址': [],
}

# 这里爬取50页，每页60条数据，共3000条，页数可调
for i in range(50):
    # 发送请求
    url = f'https://dl.ganji.com/job/pn{i+1}/?pid=702170190756085760/'
    print(url)
    r = requests.get(url, headers=headers)
    # 赶集网封ip很快，必须等待一段时间再发请求
    time.sleep(40)
    # 转化成HTML格式
    html = etree.HTML(r.text)
    job_list = html.xpath('//*[@class="dataCollectionCls"]')
    for job in job_list:
        # 获取名称、岗位类型、薪资、福利、公司、地址
        name = job.xpath('.//*[@class="ibox-title"]/text()')[0]
        job_type = job.xpath('.//*[@class="ibox-address"]/span/text()')[0]
        salary = job.xpath('.//*[@class="ibox-salary"]/text()')[0]
        welfare = job.xpath('.//*[@class="ibox-icon"]/span/span/text()')
        company = job.xpath('.//*[@class="ibox-enterprise"]//a/text()')[0]
        address = job.xpath('.//*[@class="ibox-address"]/text()')[0]

        # 数据预处理
        name = name.replace(' ', '').replace('\n', '')
        job_type = job_type.replace('｜', '')
        salary = salary.replace(' ', '').replace('\n', '')
        welfare = '/'.join(welfare)
        company = company.replace(' ', '').replace('\n', '')
        address = address.replace(' ', '').replace('\n', '')
        # 存入data
        data['名称'].append(name)
        data['岗位类型'].append(job_type)
        data['薪资'].append(salary)
        data['福利'].append(welfare)
        data['公司'].append(company)
        data['地址'].append(address)
        print(f'{name}   {job_type}   {salary}   {welfare}   {company}   {address}')
    # 转成pandas形式，并存入csv
    df = pd.DataFrame(data)
    df.to_csv('大连赶集网岗位数据.csv', encoding='utf-8-sig', index=False)
