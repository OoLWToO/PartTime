import random
import time

import pandas as pd
import re
import requests
from lxml import etree

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Cookie': 'bid=ZOdoakk_RV8; _pk_id.100001.8cb4=3dd96165e59d538e.1735457531.; __utmz=30149280.1735457531.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __yadk_uid=q71ZAYpoeRWFUwMCm88LvhdkWGaEm8yF; douban-fav-remind=1; __utmc=30149280; ct=y; _pk_ses.100001.8cb4=1; ap_v=0,6.0; __utma=30149280.395365431.1735457531.1735463551.1735469519.4; __utmt=1; dbcl2="280430415:GYyZpqcWPqE"; ck=xq3l; push_noty_num=0; push_doumail_num=0; __utmv=30149280.28043; __utmb=30149280.37.5.1735469569636'
}

main_data = {
    '标题': [],
    '发帖人': [],
    '时间': [],
    '帖子内容': [],
    '点赞数': [],
    '收藏数': [],
    '转发数': [],
    '回复数': [],
}

reply_data = {
    '主帖链接': [],
    '发帖人': [],
    '时间': [],
    '内容': [],
    '点赞数': [],
}

post_ids = ['667045', '682040', '653998', 'sociological', '722717', 'ustv', '629680', '265038', '689953', '703618',
            'postgraduates', '146203', '714776', 'english', 'guilv', '707919', '679221', '279640']

if __name__ == '__main__':
    post_id = '679221'
    base_url = f'https://www.douban.com/group/{post_id}/discussion?start=0&type=new'
    # 发送请求
    response = requests.get(base_url, headers=headers)
    # time.sleep一下，防止被封ip
    time.sleep(round(random.uniform(3, 5), 2))
    # 通过etree转成html
    html = etree.HTML(response.text)
    post_title = html.xpath('//*[@class="info"]//*[@class="title"]/a/text()')[0]
    post_page = int(html.xpath('//*[@class="paginator"]/a[last()]/text()')[0])
    if post_page > 100:
        post_page = 100
    for page in range(post_page):
        print(f'正在爬取{post_title}第{page+1}页主帖, 共{post_page}页')
        main_url = f'https://www.douban.com/group/{post_id}/discussion?start={page*25}&type=new'
        response = requests.get(main_url, headers=headers)
        time.sleep(round(random.uniform(3, 5), 2))
        html = etree.HTML(response.text)
        # 获取并遍历主帖列表，跳过第一条表头
        articel_list = html.xpath('//*[@class="article"]//tr')
        for articel in articel_list[1:]:
            detail_url = articel.xpath('./td[1]/a/@href')[0]
            response = requests.get(detail_url, headers=headers)
            time.sleep(round(random.uniform(3, 5), 2))
            html = etree.HTML(response.text)
            title = html.xpath('//h1/text()')[0]
            poster = html.xpath('//*[@class="from"]/a/text()')[0]
            post_time = html.xpath('//*[contains(@class,"create-time")]/text()')[0]
            content = ''.join(html.xpath('//*[@class="topic-content"]//p//text()')).replace('\n', '')
            try:
                like_num = html.xpath('//*[@class="react-text" and text()="赞"]/following-sibling::span/text()')[0]
            except:
                like_num = 0
            try:
                collect_num = html.xpath('//*[@class="react-text" and text()="收藏"]/following-sibling::span/text()')[0]
            except:
                collect_num = 0
            try:
                forward_num = html.xpath('//*[@class="react-text" and text()="转发"]/following-sibling::span/text()')[0]
            except:
                forward_num = 0
            try:
                comment_page = int(html.xpath('//*[@class="paginator"]/a[last()]/text()')[0])
            except:
                comment_page = 1
            # 数据预处理
            title = title.replace(' ', '').replace('\n', '')
            reply_num = 0
            for c_page in range(comment_page):
                print(f'正在爬取{detail_url}第{c_page + 1}页回复帖, 共{comment_page}页')
                comment_url = f'{detail_url}?start={c_page*100}'
                response = requests.get(detail_url, headers=headers)
                time.sleep(round(random.uniform(3, 5), 2))
                html = etree.HTML(response.text)
                comment_list = html.xpath('//*[@id="comments"]/li')
                reply_num += len(comment_list)
                for comment in comment_list:
                    comment_poster = comment.xpath('.//h4/a/text()')[0]
                    comment_time = comment.xpath('.//h4/span/text()')[0]
                    comment_content = ''.join(comment.xpath('.//*[@class="reply-content"]//p//text()'))
                    try:
                        comment_like_num = re.search(r'\d+', comment.xpath('.//*[contains(text(),"赞")]/text()')[0]).group(0)
                    except:
                        comment_like_num = 0
                    reply_data['主帖链接'].append(detail_url)
                    reply_data['发帖人'].append(comment_poster)
                    reply_data['时间'].append(comment_time)
                    reply_data['内容'].append(comment_content)
                    reply_data['点赞数'].append(comment_like_num)
            main_data['标题'].append(title)
            main_data['发帖人'].append(poster)
            main_data['时间'].append(post_time)
            main_data['帖子内容'].append(content)
            main_data['点赞数'].append(like_num)
            main_data['收藏数'].append(collect_num)
            main_data['转发数'].append(forward_num)
            main_data['回复数'].append(reply_num)
        # 转成DataFrame格式存入csv
        df = pd.DataFrame(main_data)
        df.to_csv(f'{post_title}主帖数据.csv', encoding='utf-8-sig', index=False)
        df = pd.DataFrame(reply_data)
        df.to_csv(f'{post_title}回复贴数据.csv', encoding='utf-8-sig', index=False)
