import random
import time

import pandas
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

data = {
    '标题': [],
    '作者': [],
    '阅读数': [],
    '评论数': [],
    '更新时间': [],
}

# 第一条数据的年份
year = 2025

if __name__ == '__main__':
    last_date = ''
    # 爬取1-600页
    for page in range(1, 601):
        print(f'正在爬取第{page}页')
        url = f'https://guba.eastmoney.com/o/list_futures,fczcecf103_{page}.html'
        r = requests.get(url, headers=headers)
        # time.sleep一下，防止被封ip
        time.sleep(round(random.uniform(5, 12), 2))
        html = etree.HTML(r.text)
        comment_list = html.xpath('//*[@id="articlelistnew"]/div[contains(@class,"articleh")]')
        for comment in comment_list:
            title = comment.xpath('./span[3]/a/text()')[0]
            author = comment.xpath('./span[4]/a//text()')[0]
            read_num = comment.xpath('./span[1]/text()')[0]
            comment_num = comment.xpath('./span[2]/text()')[0]
            update_time = comment.xpath('./span[5]/text()')[0]
            if not last_date:
                last_date = update_time
            if update_time[:2] > last_date[:2]:
                year -= 1
            last_date = update_time
            update_time = f'{str(year)}-{update_time}'
            print(f'{title}   {author}   {read_num}   {comment_num}   {update_time}')
            data['标题'].append(title)
            data['作者'].append(author)
            data['阅读数'].append(read_num)
            data['评论数'].append(comment_num)
            data['更新时间'].append(update_time)
        df = pandas.DataFrame(data)
        df.to_excel(f'期货吧评论数据.xlsx', index=False)
