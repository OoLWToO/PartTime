import re
import time
import pandas as pd
import requests
from lxml import etree
from matplotlib import pyplot as plt
from wordcloud import WordCloud

# 设置请求头，用于模拟用户真实请求
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Cookie": "QN1=0000ee8034fc692554e0bbc3; QN205=organic; QN277=organic; _i=DFiEuqNX_ISD8Xk6_LI962Uf_mLw; QN269=11871CD0C40611EF9FD1C6DB5E348FCC; fid=88a354a5-376c-4a7a-b827-5bf1f16b62fd; qunar-assist={%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}; csrfToken=VJNn3CGzH8yT7Sl81VaAHgVCeKEGIoWX; _vi=KHsMwvIGDk4kZ9TbfJK0r9A7sfNEusZQEagGmpITG_osS6YODHd21mz4F-Bw52kcUwpQpw5ruH32rN7CWMLhhQKNGLwbkofFtwscLKN9lvdEJcIo9Gi5TVfM1iJk3OHJUVr0sOsGxeTJozqa20TOqhG8xdNixESY_5rOl3otZkJd; Hm_lvt_c56a2b5278263aa647778d304009eafc=1735271580,1735285692; HMACCOUNT=CD82991D93936EF5; viewdist=299826-3; viewpoi=713884|708156; QN271=319823a6-3e4e-4a59-a20f-f29688b6be40; uld=1-299826-8-1735285756; JSESSIONID=5D51E6B040297D33FB5648ABBCCEFCC1; QN267=0263297418ec7372b0; ariaDefaultTheme=undefined; Hm_lpvt_c56a2b5278263aa647778d304009eafc=1735285756; SECKEY_ABVK=SpksYxrkiZ95rjNjcpCOIfurycvQxpMavFte9FbQxVw%3D; BMAP_SECKEY=m7HCwDvpsHz7IoQPkOGrzgsw6-1d-8TTjunY1AuXLJrxHSXqN8VxEDwBEFeCtQ8el98rFNlkuWcY0X3mUXvPpLJ0rt26r0MXO4tRABVe3Af7a-UQ2hHjzmDSm_xEM8hi-Bke8vn7ztvbFVFmHoc4zq57orqhS8SzjCpAwAiwxS7kncDt5h4m1WrVXFnaX-Ec",
    "Referer": "https://travel.qunar.com/p-cs299826-fuzhou-jingdian-3-2",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
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
def create_pie_chart(scenery, item, value):
    plt.close('all')
    plt.pie(value, labels=item, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title(f'{scenery}游玩月份统计饼图')
    plt.savefig(f'{scenery}游玩月份统计饼图.png')


# 生成词云
def create_word_chart(scenery, word):
    plt.close('all')
    wc = WordCloud(font_path="simsun.ttc", width=800, height=600, mode="RGBA", background_color=None).generate(word)
    plt.imshow(wc, interpolation='bilinear')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.axis("off")
    plt.title(f'{scenery}评论统计词云')
    wc.to_file(f'{scenery}评论统计词云.png')


if __name__ == '__main__':
    # 获取所有景点列表，循环爬取1-100页
    for page in range(1, 100):
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

    # 爬取丽江古城、泸沽湖、玉龙雪山评论数据
    scenery_name = ['丽江古城', '泸沽湖', '玉龙雪山']
    bash_urls = ['https://travel.qunar.com/p-oi714422-lijianggucheng',
                 'https://travel.qunar.com/p-oi720460-luguhu',
                 'https://travel.qunar.com/p-oi714716-yulongxueshan']
    for bash_url in bash_urls:
        comment_data = {
            '景点名': [],
            '评论时间': [],
            '评论标题': [],
            '评论内容': []
        }
        # 用于统计评论月份数量
        time_item = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        time_value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # 获取景点id和景点评论数
        response = requests.get(bash_url, headers=headers)
        html = etree.HTML(response.text)
        scenery_id = re.findall(r'\d+', bash_url)[0]
        # 用于统计词云
        comment_str = ''
        # 每页十条数据
        for page in range(50):
            comment_url = f'https://travel.qunar.com/place/api/html/comments/poi/{scenery_id}?poiList=true&sortField=0&rank=0&pageSize=10&page={page + 1}'
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
                print(
                    f'{scenery_name[bash_urls.index(bash_url)]}   {comment_title[:20]}   {comment_date}   {comment_content[:20]}')
                # 存入data
                comment_data['景点名'].append(scenery_name[bash_urls.index(bash_url)])
                comment_data['评论时间'].append(comment_date)
                comment_data['评论标题'].append(comment_title)
                comment_data['评论内容'].append(comment_content)
                time_value[time_item.index(month)] += 1
        create_pie_chart(scenery_name[bash_urls.index(bash_url)], time_item, time_value)
        create_word_chart(scenery_name[bash_urls.index(bash_url)], comment_str)
        df = pd.DataFrame(comment_data)
        df.to_excel(f'{scenery_name[bash_urls.index(bash_url)]}评论统计.xlsx', index=False)
