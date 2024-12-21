import re
import time
from datetime import datetime

import pandas as pd
import requests
from lxml import etree
from matplotlib import pyplot as plt
from wordcloud import WordCloud

# 设置请求头，用于模拟用户真实请求
headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": 'QN1=00014780306c68df610808e8; QN300=s=baidu; QN99=3448; QN269=D563A601BECF11EF86526E207D55223B; _i=DFiEuMNDb2fDNWq6_9glXRx2qcAw; fid=7c7a9c41-5ae8-4be9-9273-913ccfe15fd7; QN205=s=baidu; QN277=s=baidu; QN601=97e121b5db0a23b9ccfd26b829b08fca; QN48=00013a802f1068df6168782d; quinn=f1bf42e54301d5c83cd6db24110edf29e4880dd5d1dd492e5be8635f4c6e2c10f852a48e1128126d06944844436cb259; QunarGlobal=10.80.148.213_-310e495_193d79474b2_-60d6|1734698549912; activityClose=1; ariaDefaultTheme=null; QN243=3; qunar-assist={"version":"20211215173359.925","show":false,"audio":false,"speed":"middle","zomm":1,"cursor":false,"pointer":false,"bigtext":false,"overead":false,"readscreen":false,"theme":"default"}; csrfToken=zecYQVBSkFcwXhLDrtHgSlKwtLFto9rE; Hm_lvt_c56a2b5278263aa647778d304009eafc=1734698570,1734700596; HMACCOUNT=F2E6A3827135F422; viewdist=300021-14; viewpoi=719780|5741150|707622|707449|712636; uld=1-300021-22-1734704269; JSESSIONID=9189EC998729FCA367046B756118A22F; QN267=0487590136a614d724; _vi=ICuVoesKd-nU2ShDhqqcQc3L-7ZmrGmKWfLK-dH37ooA8TlesKDy598Da4AThMEe6QPIotCNdNENqM9WA5lheQmz9UQohURvqdd_nj4RcZJvljk7oIBqSqoj4Nam0M9jB6QgQwLrax3RMaN1UAdY6hi2nk-09FD89ulU4cvTCeuu; Hm_lpvt_c56a2b5278263aa647778d304009eafc=1734704287; QN271=b0e9c5b1-d318-4f5a-b07c-c6b0d6c643b9; SECKEY_ABVK=9xfvEiUOO00T91zeM6Io0BiHMaIu0m1wolo+mXXbY6I=; BMAP_SECKEY=MhT_QqWPn7ObIoJuGQms5zWZuZnrh2tQR6qZ95Gy5Fk5LCwML5sYbbdloGJbahzkTJQP-mLFcAoi_MEtUCu_MguS8HBfe3DRFkI1IZKmRhR3wDDfCM2lFyjCfyikXQRtkveyqKZEAwJL4njf61zGDDAq8pIELdYsVy2-rvg91sebAkAtHuBZZ3b41dultMcU',
    "referer": "https://travel.qunar.com/p-oi712636-bayiqiyijinianguan",
    "sec-ch-ua": '";Not A Brand";v="99", "Chromium";v="94"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 SE 2.X MetaSr 1.0",
    "x-requested-with": "XMLHttpRequest"
}

data = {
    '景点名': [],
    '评论时间': [],
    '评论标题': [],
    '评论内容': []
}

# 生成词云
def create_word_chart(scenery, word):
    wc = WordCloud(font_path="simsun.ttc", width=800, height=600, mode="RGBA", background_color=None).generate(word)
    plt.imshow(wc, interpolation='bilinear')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.axis("off")
    plt.title(f'{scenery}评论统计词云')
    wc.to_file(f'{scenery}评论统计词云.png')

if __name__ == '__main__':
    scenery_name = ['八一起义纪念馆', '八一南昌起义纪念塔', '朱德旧居', '八一广场']
    # 八一起义纪念馆/八一南昌起义纪念塔/朱德旧居/八一广场
    bash_urls = ['https://travel.qunar.com/p-oi712636-bayiqiyijinianguan',
                    'https://travel.qunar.com/p-oi707622-bayinanchangqiyijinian',
                    'https://travel.qunar.com/p-oi707449-zhudejiuju',
                    'https://travel.qunar.com/p-oi5741150-bayiguangchang']
    for bash_url in bash_urls:
        # 获取景点id和景点评论数
        response = requests.get(bash_url, headers=headers)
        html = etree.HTML(response.text)
        scenery_id = re.findall(r'\d+', bash_url)[0]
        comment_num = int(re.findall(r'\d+', html.xpath('//*[@data-beacon="total_comments"]/text()')[0])[0])
        # 用于统计词云
        comment_str = ''
        # 每页十条数据
        for page in range(comment_num // 10 + 1):
            comment_url = f'https://travel.qunar.com/place/api/html/comments/poi/{scenery_id}?poiList=true&sortField=1&rank=0&pageSize=10&page={page+1}'
            try:
                r = requests.get(comment_url, headers=headers)
                time.sleep(3)
                html = etree.HTML(r.json()['data'])
            except:
                try:
                    # 请求出错重试
                    r = requests.get(comment_url, headers=headers)
                    time.sleep(3)
                    html = etree.HTML(r.json()['data'])
                except:
                    # 请求出错重试
                    r = requests.get(comment_url, headers=headers)
                    time.sleep(3)
                    html = etree.HTML(r.json()['data'])
            ele_list = html.xpath('//*[@id="comment_box"]/li')
            for ele in ele_list:
                try:
                    comment_title = ele.xpath('.//*[@class="e_comment_title"]/a/text()')[0]
                except:
                    comment_title = ''
                comment_date = ele.xpath('.//*[@class="e_comment_add_info"]//li[1]/text()')[0]
                year, month, day = comment_date.split('-')
                new_year = str(int(year) + 3)
                comment_date = f'{new_year}-{month}-{day}'
                comment_content = ''.join(ele.xpath('.//*[@class="e_comment_content"]/p/text()'))
                comment_str += comment_title
                comment_str += comment_content
                print(f'{scenery_name[bash_urls.index(bash_url)]}   {comment_title[:20]}   {comment_date}   {comment_content[:20]}')
                # 存入data
                data['景点名'].append(scenery_name[bash_urls.index(bash_url)])
                data['评论时间'].append(comment_date)
                data['评论标题'].append(comment_title)
                data['评论内容'].append(comment_content)
        create_word_chart(scenery_name[bash_urls.index(bash_url)], comment_str)
        df = pd.DataFrame(data)
        df.to_excel('南昌红色景点评论统计.xlsx', index=False)