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
    'scenery_name': [],
    'user_name': [],
    'score': [],
    'content': [],
}



if __name__ == '__main__':
    # 获取所有景点列表，循环爬取1-15页
    for page in range(5, 16):
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
            # 每页十条数据
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
                    data['scenery_name'].append(scenery_name)
                    data['user_name'].append(user_name)
                    data['score'].append(score)
                    data['content'].append(content)
            df = pd.DataFrame(data)
            df.to_excel(f'南京景点评论统计.xlsx', index=False)
