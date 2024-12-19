import os
import time

import pandas as pd
import requests
from lxml import etree

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

if __name__ == '__main__':
    url = f'https://www.chinabuilding.com.cn/books.html'
    r = requests.get(url, headers=headers)
    html = etree.HTML(r.text)
    directory_list = html.xpath('//*[@id="ctl00_body_ulCate"]/li/a[2]')
    for directory in directory_list[2:3]:
        book_data = {
            '标题': [],
            '简介': []
        }
        book_url = []
        directory_name = directory.xpath('./text()')[0]
        print(f'正在爬取{directory_name}栏目数据！！！')
        # 创建图片目录
        os.makedirs(f'图片/{directory_name}', exist_ok=True)
        original_url = directory.xpath("./@href")[0]
        r = requests.get(f'https://www.chinabuilding.com.cn/{original_url}', headers=headers)
        html = etree.HTML(r.text)
        try:
            page_size = html.xpath('//*[@class="pagenumber"]/li[last()-1]/a/text()')[0].replace('...', '')
        except:
            page_size = '1'
        parts = original_url.split(".")
        print(f'总共：{page_size}页，开始爬取书本链接！！！')
        # 读取书本链接
        for page in range(int(page_size)):
            print(f'第{page + 1}页')
            r = requests.get(f'https://www.chinabuilding.com.cn/{parts[0]}-{page + 1}.{parts[1]}', headers=headers)
            html = etree.HTML(r.text)
            urls = html.xpath('//*[@id="books-list"]//*[@class="title"]/a/@href')
            for url in urls:
                book_url.append(f'https://www.chinabuilding.com.cn{url}')
        print('开始爬取书籍信息！！！')
        for url in book_url:
            i = 0
            r = requests.get(url, headers=headers)
            html = etree.HTML(r.text)
            title = html.xpath('//*[@id="book-info"]/h2/text()')[0].replace('/', '').replace(' ', '').replace('（', '(').replace(
                '）', ')')
            introduce = ''
            introduce_str = html.xpath('//*[@id="book-contdesc"]//p//span/text()')
            if len(introduce_str) == 0:
                introduce_str = html.xpath('//*[@id="book-contdesc"]//p/text()')
            for text in introduce_str:
                introduce += text
            os.makedirs(f'图片/{directory_name}/{title}', exist_ok=True)
            img_url = html.xpath('//*[@id="book-info"]//img/@src')
            for img in img_url:
                i += 1
                r = requests.get(f'https://www.chinabuilding.com.cn/{img}', headers=headers)
                with open(f"图片/{directory_name}/{title}/{i}.png", "wb") as f:
                    f.write(r.content)
            book_data['标题'].append(title)
            book_data['简介'].append(introduce)
            print(f'共{len(book_url)}条数据，第{book_url.index(url) + 1}条，{title}，保存成功')
            df = pd.DataFrame(book_data)
            df.to_excel(f'{directory_name}书籍数据.xlsx', index=False)
