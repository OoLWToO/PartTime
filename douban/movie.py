import pandas as pd
import requests
from lxml import etree

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Cookie': 'bid=JMweL-P6C-k; douban-fav-remind=1; _pk_id.100001.8cb4=81eca70ccbd53f6b.1730477798.; __utmz=30149280.1730477798.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __yadk_uid=fV9X0td9qlvPTnrd1q7xWCztzvD66YBK; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1734610854%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DfDOgugQOrGKrPy75Nn7_BCtHjS_V5jRivB9_-ggiq1CQIT1ofo1eJR70ks0sVvv8pdXEFK4mghEzEJAE9DIUeq%26wd%3D%26eqid%3D8032f2be000057d8000000036724fe9a%22%5D; _pk_ses.100001.8cb4=1; ap_v=0,6.0; __utma=30149280.1445238079.1730477798.1730477798.1734610855.2; __utmc=30149280; ll="108306"; dbcl2="280430415:GYyZpqcWPqE"; ck=xq3l; push_noty_num=0; push_doumail_num=0; __utmt=1; __utmv=30149280.28043; __utmb=30149280.11.10.1734610855',
}

data = {
    '电影名': [],
    '导演': [],
    '编剧': [],
    '主演': [],
    '类型': [],
    '上映日期': [],
    '片长': [],
}

if __name__ == '__main__':
    # 爬取豆瓣电影: 周星驰
    base_url = 'https://www.douban.com/personage/27253787/'
    # 发送请求
    response = requests.get(base_url, headers=headers)
    # 通过etree转成html
    html = etree.HTML(response.text)
    # 根据xpath获取人物基本信息
    introduce = ''
    base_info_list = html.xpath('//*[@class="subject-target"]//div[@class="right"]//text()')
    for base_info in base_info_list:
        if base_info.replace('\n', '').replace(' ', ''):
            introduce += base_info.replace(' ', '')
    # 获取人物简介
    introduce += ''.join(html.xpath('//*[contains(@class,"subject-intro")]//text()'))
    # 设置获奖情况链接
    awards_url = f'{base_url}awards'
    response = requests.get(awards_url, headers=headers)
    html = etree.HTML(response.text)
    # 获取获奖情况
    awards_text = ''.join(html.xpath('//*[@id="content"]//text()'))
    # 写入txt
    with open('周星驰.txt', 'w', encoding='utf-8') as file:
        file.write(introduce + '\n' + awards_text)

    # 循环获取所有作品链接，共13页
    for page in range(0, 121, 10):
        creation_url = f'{base_url}creations?type=filmmaker&start={page}&sortby=collection&role=&format=pic'
        response = requests.get(creation_url, headers=headers)
        html = etree.HTML(response.text)
        movie_urls = html.xpath('//*[@class="creations"]/li/a/@href')
        for movie_url in movie_urls:
            # 请求电影详细页信息
            response = requests.get(movie_url, headers=headers)
            html = etree.HTML(response.text)
            # 根据xpath获取: 电影名、导演、编剧、主演、类型、上映日期、片长
            m_name = ''.join(html.xpath('//h1//text()')).replace('\n', '').replace(' ', '')
            director = '/'.join(html.xpath('//*[@id="info"]/span[./span[text()="导演"]]/span[@class="attrs"]/a/text()'))
            writers = '/'.join(html.xpath('//*[@id="info"]/span[./span[text()="编剧"]]/span[@class="attrs"]/a/text()'))
            starring = '/'.join(html.xpath('//*[@id="info"]/span[./span[text()="主演"]]/span[@class="attrs"]/a//text()'))
            m_type = '/'.join(html.xpath('//*[@property="v:genre"]/text()'))
            release_date = '/'.join(html.xpath('//*[@property="v:initialReleaseDate"]/text()'))
            length = '/'.join(html.xpath('//*[@property="v:runtime"]/text()'))
            print(f'{m_name}   {director}   {writers}   {starring}   {m_type}   {release_date}   {length}')
            # 存入data字典
            data['电影名'].append(m_name)
            data['导演'].append(director)
            data['编剧'].append(writers)
            data['主演'].append(starring)
            data['类型'].append(m_type)
            data['上映日期'].append(release_date)
            data['片长'].append(length)
    # 转成DataFrame格式存入csv
    df = pd.DataFrame(data)
    df.to_csv('周星驰作品.csv', encoding='utf-8-sig', index=False)






