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
    "Cookie": "QN1=0000ee8034fc692554e0bbc3; QN205=organic; QN277=organic; _i=DFiEuqNX_ISD8Xk6_LI962Uf_mLw; QN269=11871CD0C40611EF9FD1C6DB5E348FCC; fid=88a354a5-376c-4a7a-b827-5bf1f16b62fd; QN48=tc_693498e620e8968b_1941bfb7b58_ad39; viewbook=6130591|6836373|6802914|6130591; viewdist=299826-4|369313-2|297222-1|299878-3; _vi=HfyXB3eHiag71lhQqXMBDpr_BeZMDAGfFmLyfT88gyVoGtidIAZc2laEohYJ-87adzhxQi49oQSSZYuGgLvIHwcDJEcjV5btAQhZu-66m2DqLOWPT6Q6Ft4XTW6qAIR2to6ggf7hx4tQHNT6hK8tKoqQuIo6tPEqFdAcGPWakEbO; viewpoi=7469386|701880|713884|708156|7564992|709621; uld=1-299861-2-1735788100|1-299878-4-1735787531|1-297222-1-1735636283|1-369313-2-1735636270|1-299826-18-1735289547|1-297220-2-1735286009; SECKEY_ABVK=PNG2QB2CO18LI2SPUmyn8U0sOgQnKCaZ0DqO7GW0rjI%3D; BMAP_SECKEY=xSteYl7H5Uc_i2vAQl-7sO3HUzOY7ftKrWH9MkCbTdyoiUzVG-1MB2Xs-uKR2yxfnOslpcgeXB1APvNfgX3tw_o-Omc5IHORht95xa-02m0juqQMRXCTyJzWoo86g1Gw_LqjBxOkP-pexdXLPTXjGnIQELRze-TzByF7FISKNl5Dv00AJWqXOBdUhNXUjbVp; qunar-assist={%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}; QN267=0263297418564e3c0a; csrfToken=BvuVHz6syu6TcS1j88GTjKlVxoNYpn1W; ariaDefaultTheme=undefined; Hm_lvt_c56a2b5278263aa647778d304009eafc=1735638067,1735786209,1735788327,1735788434; Hm_lpvt_c56a2b5278263aa647778d304009eafc=1735788434; HMACCOUNT=CD82991D93936EF5; QN271=be4191b1-0314-44d9-86d6-3280b8b54bb0; JSESSIONID=D4CBCB6B4BC6729922369F310EE6A795",
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
    '景点名称': [],
    '用户名': [],
    '评分': [],
    '评论': [],
}


info_data = {
    '景点名称': [],
    '概述': [],
    '地址': [],
}


if __name__ == '__main__':
    # 获取所有景点列表，循环爬取1-15页
    for page in range(1, 16):
        print(f'景点第{page}页')
        # 请求url
        url = f'https://travel.qunar.com/p-cs299861-nanjing-jingdian-3-{page}'
        # 发送请求
        r = requests.get(url, headers=headers)
        time.sleep(1)
        html = etree.HTML(r.text)
        # 获取景点列表
        ele_list = html.xpath('//*[@class="listbox"]/ul/li')
        for ele in ele_list:
            # 获取景点名字以及链接
            scenery_name = ele.xpath('.//*[@class="cn_tit"]/text()')[0].replace(' ', '')
            detail_url = ele.xpath('.//a[@class="titlink"]/@href')[0]
            scenery_id = re.findall(r'\d+', detail_url)[0]
            image_url = ele.xpath('.//a[@class="imglink"]/img/@src')[0]
            r = requests.get(image_url, headers=headers)
            with open(f'图片/{scenery_name}.png', 'wb') as news_image:
                news_image.write(r.content)
            r = requests.get(detail_url, headers=headers)
            html = etree.HTML(r.text)
            try:
                intro = ''.join(html.xpath('//*[@class="e_db_content_box"]//p//text()')).replace('\n', '')
            except:
                intro = ''
            try:
                address = html.xpath('//dt[text()="地址:"]/following-sibling::dd/span/text()')[0]
            except:
                address = ''
            # 每页50条数据
            for c_page in range(20):
                print(f'正在爬取{scenery_name}, 第{c_page + 1}页评论')
                comment_url = f'https://travel.qunar.com/place/api/html/comments/poi/{scenery_id}?poiList=true&sortField=0&rank=0&pageSize=50&page={c_page + 1}'
                try:
                    r = requests.get(comment_url, headers=headers)
                    time.sleep(1)
                    html = etree.HTML(r.json()['data'])
                except:
                    try:
                        # 请求出错重试
                        time.sleep(3)
                        r = requests.get(comment_url, headers=headers)
                        html = etree.HTML(r.json()['data'])
                    except:
                        # 请求出错重试
                        time.sleep(5)
                        r = requests.get(comment_url, headers=headers)
                        html = etree.HTML(r.json()['data'])
                comment_list = html.xpath('//*[@id="comment_box"]/li')
                if len(comment_list) == 0:
                    break
                for comment in comment_list:
                    # user_name获取不到的为游客
                    try:
                        user_name = comment.xpath('.//*[@class="e_comment_usr_name"]/a/text()')[0]
                    except:
                        user_name = '游客'
                    score = re.search(r'\d+', comment.xpath('.//*[@class="total_star"]/span/@class')[0]).group(0)
                    content = ''.join(comment.xpath('.//*[@class="e_comment_content"]/p/text()'))
                    print(f'{scenery_name}   {user_name}   {score}   {content[:20]}')
                    # 存入data
                    data['景点名称'].append(scenery_name)
                    data['用户名'].append(user_name)
                    data['评分'].append(score)
                    data['评论'].append(content)
            info_data['景点名称'].append(scenery_name)
            info_data['概述'].append(intro)
            info_data['地址'].append(address)
            df = pd.DataFrame(data)
            df.to_excel(f'南京景点评论统计.xlsx', index=False)
            df = pd.DataFrame(info_data)
            df.to_excel(f'南京景点信息统计.xlsx', index=False)
