import re
import time
import pandas as pd
import requests
from lxml import etree

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
    '页面网址': [],
    '标题': [],
    '作者': [],
    '发表时间': [],
    '游玩时间': [],
    '天数': [],
    '人均': [],
    '和谁': [],
    '标签': [],
    '途经': [],
    '行程': [],
    '目录': [],
    '正文': [],
}

scenery_list = {
    '平潭县': 'https://travel.qunar.com/travelbook/list/4-pingtandao-714512/hot_heat/{}.htm',
    '东山县': 'https://travel.qunar.com/travelbook/list/%25E4%25B8%259C%25E5%25B1%25B1%25E5%25B2%259B/hot_heat/{}.htm'
}


if __name__ == '__main__':
    for scenery_name, base_url in scenery_list.items():
        for page in range(1, 101):
            print(f'正在爬取第{page}页评论')
            # 请求url
            url = base_url.format(page)
            # 发送请求
            r = requests.get(url, headers=headers)
            time.sleep(1)
            html = etree.HTML(r.text)
            youji_eles = html.xpath('//*[@class="b_strategy_list "]/li')
            if not youji_eles:
                break
            for youji_ele in youji_eles:
                title = ''.join(youji_ele.xpath('.//h2/a//text()'))
                try:
                    author = youji_ele.xpath('.//*[@class="user_name"]/a/text()')[0]
                except:
                    author = ''
                try:
                    play_time = youji_ele.xpath('.//*[@class="date"]/text()')[0].replace(' ', '').replace('出发', '')
                except:
                    play_time = ''
                try:
                    days_num = youji_ele.xpath('.//*[@class="days"]/text()')[0].replace(' ', '').replace('共', '').replace('天', '')
                except:
                    days_num = youji_ele.xpath('.//*[@class="days"]/text()')[0].replace(' ', '').replace('共', '').replace('天', '')
                try:
                    per_capita = youji_ele.xpath('.//*[@class="fee"]/text()')[0].replace(' ', '').replace('人均', '').replace('元', '')
                except:
                    per_capita = ''
                try:
                    with_whom = youji_ele.xpath('.//*[@class="people"]/text()')[0].replace(' ', '')
                except:
                    with_whom = ''
                try:
                    trip = youji_ele.xpath('.//*[@class="trip"]/text()')[0].replace(' ', '')
                except:
                    trip = ''
                try:
                    via_scenery = youji_ele.xpath('.//*[@class="places" and contains(text(),"途经")]/span/text()')[0]
                except:
                    via_scenery = ''
                try:
                    stroke = ''.join(youji_ele.xpath('.//*[@class="places" and contains(text(),"行程")]//text()')).replace('行程：', '')
                except:
                    stroke = ''
                try:
                    youji_id = re.search(r'\d+', youji_ele.xpath('.//*[@class="pic"][1]/a[last()]/@href')[0]).group(0)
                except:
                    youji_id = ''
                if youji_id:
                    youji_url = f'https://travel.qunar.com/travelbook/note/{youji_id}'
                    r = requests.get(youji_url, headers=headers)
                    time.sleep(1)
                    html = etree.HTML(r.text)
                    try:
                        publish_time = html.xpath('//*[@class="date"]/span[1]/text()')[0].replace('/', '-')
                        directory = ' | '.join(html.xpath('//*[@class="clrfix"]/div[@class="text"]/text()'))
                        main_text = ''.join(html.xpath('//*[@class="e_main"]//text()')).replace(' \n', '')
                    except:
                        publish_time = ''
                        directory = ''
                        main_text = ''
                else:
                    youji_url = ''
                    publish_time = ''
                    directory = ''
                    main_text = ''
                print(f'{youji_url}   {title}   {author}   {publish_time}   {play_time}   {days_num}   {per_capita}   '
                      f'{with_whom}   {trip}   {via_scenery}   {stroke}   {directory}   {main_text[:10]}')
                data['页面网址'].append(youji_url)
                data['标题'].append(title)
                data['作者'].append(author)
                data['发表时间'].append(publish_time)
                data['游玩时间'].append(play_time)
                data['天数'].append(days_num)
                data['人均'].append(per_capita)
                data['和谁'].append(with_whom)
                data['标签'].append(trip)
                data['途经'].append(via_scenery)
                data['行程'].append(stroke)
                data['目录'].append(directory)
                data['正文'].append(main_text)
            df = pd.DataFrame(data)
            df.to_excel(f'{scenery_name}游记1.xlsx', index=False)