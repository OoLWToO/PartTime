import time
from datetime import datetime

import pandas as pd
import requests
from lxml import etree
from matplotlib import pyplot as plt
from wordcloud import WordCloud

# 设置请求头，用于模拟用户真实请求
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Cookie': '__jsluid_s=c9bf2381199315a3f9d70fab5efbea9b; __jsl_clearance_s=1718590950.375|0|BNVMH65p0N9580f3nELVxfBlj1g%3D; PHPSESSID=mnnnrrlijttt606feek3bkdvg0; mfw_uuid=666f9de7-be92-5b8a-42db-f09d461618a6; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222024-06-17+10%3A22%3A31%22%3B%7D; __mfwc=direct; __mfwa=1718590951232.55084.1.1718590951232.1718590951232; __mfwlv=1718590951; __mfwvn=1; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1718590951; uva=s%3A150%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1718590952%3Bs%3A10%3A%22last_refer%22%3Bs%3A82%3A%22https%3A%2F%2Fwww.mafengwo.cn%2Flocaldeals%2F0-0-M10132-0-0-0-0-0.html%3Ffrom%3Dlocaldeals_index%22%3Bs%3A5%3A%22rhost%22%3BN%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1718590952%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=666f9de7-be92-5b8a-42db-f09d461618a6; __mfwb=7d6d46205828.2.direct; __mfwlt=1718590972; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1718590973; bottom_ad_status=0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

data = {
    '名字': [],
    '英文名': [],
    '攻略数': [],
    '点评数': [],
    '好评率': [],
    '简介': []
}


# 生成饼图
def create_pie_chart(item, value):
    plt.pie(value, labels=item, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title('前500条评论游玩月份统计饼图')
    plt.savefig('前500条评论游玩月份统计饼图.png')


# 生成条形图
def create_line_chart(item, value):
    plt.bar(item, value)
    plt.xlabel('类别')
    plt.ylabel('数值')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title('前500条评论评分统计条形图')
    plt.savefig('前500条评论评分统计条形图.png')


# 生成词云
def create_word_chart(word):
    wc = WordCloud(font_path="simsun.ttc", width=800, height=600, mode="RGBA", background_color=None).generate(word)
    plt.imshow(wc, interpolation='bilinear')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.axis("off")
    plt.title('前500条评论统计词云')
    wc.to_file("前500条评论统计词云.png")


if __name__ == '__main__':
    # 循环爬取1-200页
    for page in range(1, 200):
        # 请求url
        url = f'https://travel.qunar.com/p-cs300079-lijiang-jingdian-3-{page}'
        # 发送请求
        r = requests.get(url, headers=headers)
        time.sleep(1)
        html = etree.HTML(r.text)
        # 获取景点列表
        ele_list = html.xpath('//*[@class="listbox"]/ul/li')
        for ele in ele_list:
            # 获取景点名字、英文名、攻略数、点评数、好评率、简介（try处理数据为空的情况）
            name = ele.xpath('.//*[@class="cn_tit"]/text()')[0]
            try:
                en_name = ele.xpath('.//*[@class="en_tit"]/text()')[0]
            except:
                en_name = '-'
            strategy_sum = ele.xpath('.//*[@class="strategy_sum"]/text()')[0]
            comment_sum = ele.xpath('.//*[@class="comment_sum"]/text()')[0]
            star = ele.xpath('.//*[@class="cur_star"]/@style')[0]
            try:
                introduce = ele.xpath('.//*[@class="desbox"]/text()')[0]
            except:
                introduce = '-'
            # 数据预处理
            name = name.replace(' ', '')
            en_name = en_name.replace(' ', '')
            strategy_sum = strategy_sum.replace(' ', '').replace('\n', '')
            comment_sum = comment_sum.replace(' ', '').replace('\n', '')
            star = star.replace('width:', '')
            introduce = introduce.replace('\n', '')
            print(f'{name}   {en_name}   {strategy_sum}   {comment_sum}   {star}   {introduce}')
            # 存入data
            data['名字'].append(name)
            data['英文名'].append(en_name)
            data['攻略数'].append(strategy_sum)
            data['点评数'].append(comment_sum)
            data['好评率'].append(star)
            data['简介'].append(introduce)
    df = pd.DataFrame(data)
    df.to_csv('丽江旅游景点统计.csv', encoding='utf-8-sig', index=False)

    # 爬取丽江古城50页评论，每页10条数据，并可视化
    time_item = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    time_value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    star_item = ['好评', '中评', '差评']
    star_value = [0, 0, 0]
    word_item = []
    word_value = []
    comment_str = ''
    for page in range(1, 51):
        url = f'https://travel.qunar.com/p-oi714422-lijianggucheng-1-{page}#lydp'
        r = requests.get(url, headers=headers)
        time.sleep(1)
        html = etree.HTML(r.text)
        ele_list = html.xpath('//*[@id="comment_box"]/li')
        for ele in ele_list:
            # 获取时间并取月份
            date = ele.xpath('.//*[@class="e_comment_add_info"]//li[1]/text()')[0][5:7]
            time_value[time_item.index(date)] += 1
            # 获取评分并统计
            star = int(ele.xpath('.//*[@class="total_star"]/span/@class')[0][-1:])
            if star == 5:
                star_value[0] += 1
            if star == 3 or star == 4:
                star_value[1] += 1
            if star == 1 or star == 2:
                star_value[2] += 1
            # 获取评论并加入总文本
            try:
                comment_title = ele.xpath('.//*[@class="e_comment_title"]/a/text()')[0]
            except:
                comment_title = ''
            comment_str += comment_title
            comment_content = ele.xpath('.//*[@class="e_comment_content"]/p/text()')
            for content in comment_content:
                comment_str += content
    create_pie_chart(time_item, time_value)
    create_line_chart(star_item, star_value)
    create_word_chart(comment_str)
