import random
import re
import time
import pandas as pd
import requests
from lxml import etree

# 设置请求头，用于模拟用户真实请求
headers = {
  "accept": "application/json, text/javascript, */*; q=0.01",
  "accept_language": "zh-CN,zh;q=0.9",
  "cookie": "QN1=0000f380306c6930eea00f05; QN300=s%3Dbaidu; QN99=7505; QN48=0789146f-7bf8-4b36-9efe-b318a19eb641; QN668=51%2C57%2C53%2C55%2C53%2C56%2C56%2C56%2C51%2C59%2C54%2C55%2C58; ctt_june=1683616182042##iK3waKgsVuPwawPwa%3D3%3DX2ERaS0RWPjnXSgwXKgnEKaNX23NaRTDVKiIEPPOiK3siK3saKgsWKaOWSjwaKv%2BWhPwaUvt; ctf_june=1683616182042##iK3wWStAaUPwawPwasXmEKXnaKtsaKDma%3DWRXPawVK2nas3AVPWTEP3%2BaKGIiK3siK3saKgsWKaOWSjwaKa%2BaUPwaUvt; cs_june=c8d615b10725571c19a318c9a0c8e1c16efbfa668eaa8771a57495dd89a1e31a420495129a4621b763b0ad19a0a76a3f928ed69f8dc87a0d2aac3f32c97f23c8b17c80df7eee7c02a9c1a6a5b97c11799ecb0af0e312e990309499ff2b518b685a737ae180251ef5be23400b098dd8ca; QN601=43ef70d0cf2410dd843b6098a7debc7f; quinn=29c9f798233894088e52429c6073d84ee91d71b83eb3d0ba71e6508381ebe5b6283d72adc23dfa1b432ddd7c7fbf174a; QN277=organic; QN269=5C2DA410C4E311EF9B8912E1EDE33B5B; _i=ueHd8LougHAucBJAdyscGbOfN1oX; fid=4a6141c8-b941-427f-8ccd-f763e5792e72; QN205=s%3Dbaidu; viewpoi=713884|707373|706824|705581|703792|707188; BMAP_SECKEY=gSTJrNTncfna43I_4E2xierXvXyftnBFpCpAzELjXEjel9KGao1jY4aOZDs9XMtyPQd8WaQI371ea098FBISSbKQTjYUSSNgCT4U3II0KjQNHFWQA6bq5WbHzmD7od4ObKPoaLgFXjUH8wXDcrI5CytAARWoQqu0CzSDLEUzYjgjo26bXzbFDTLFSBkTbTjZ; SECKEY_ABVK=qjqwVFjTQAzYjjbZKQQxFtMld0dJobwYZqZBv03b4Uw%3D; qunar-assist={%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}; csrfToken=PkiFlWNf7Dlll1rxTDD9l2zdGBkzlLbq; Hm_lvt_c56a2b5278263aa647778d304009eafc=1735705207,1735711299,1735723191,1735821371; HMACCOUNT=53BEF1F68DC70C31; viewbook=6814930|7441092; _vi=lwnbmwOFwvKFowPVMTEGyjU6ULkdh6yUPiRYyGuEdO_5szQkdmI5cBlqQHkydsp3nNCjbsOx0TcWGRv93KBKc0go00JWMtDGMFGzTUYHne1IOTUw_6j18yLvXgtWYa_TEyNZFuPhU33ecwiAJWrt4o_OkNq_5dC38r-5oJwbSUVV; viewdist=299826-13|299861-84|297215-1|369313-17|297222-3; uld=1-369313-17-1735822519|1-297222-3-1735821518|1-297215-1-1735821358|1-299861-97-1735723182|1-299826-15-1735367424; JSESSIONID=F3A8E14601BC5D40D1B8CD0890074299; QN267=0191308557508daccdf; ariaDefaultTheme=undefined; Hm_lpvt_c56a2b5278263aa647778d304009eafc=1735822532; QN271=f172a886-c1f1-4b98-8add-6e8dc4713081",
  "priority": "u=1, i",
  "referer": "https://travel.qunar.com/p-cs369313-gulangyu",
  "sec_ch_ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
  "sec_ch_ua_mobile": "?0",
  "sec_ch_ua_platform": "\"Windows\"",
  "sec_fetch_dest": "empty",
  "sec_fetch_mode": "cors",
  "sec_fetch_site": "same-origin",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
  "x_requested_with": "XMLHttpRequest"
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

scenery_list = ['连江', '福建东山', '南澳',
                '长海县', '大长山岛', '长岛',
                '烟台+长岛', '上海崇明', '浙江岱山',
                '岱山', '岱山岛', '浙江嵊泗列岛',
                '嵊泗列岛', '嵊泗', '洞头',
                '洞头+温州', '温州+洞头', '浙江+玉环']
search_url = 'https://travel.qunar.com/search/gonglue/{}/hot_heat/{}.htm'

if __name__ == '__main__':
    i = 17
    for page in range(1, 21):
        print(f'正在爬取第{page}页攻略')
        url = search_url.format(scenery_list[i], page)
        for j in range(3):
            r = requests.get(url, headers=headers)
            time.sleep(round(random.uniform(3, 5), 2))
            html = etree.HTML(r.text)
            gonglue_eles = html.xpath('//*[@class="b_strategy_list "]/li')
            if len(gonglue_eles) == 0 and '操作过于频繁' in r.text:
                raise print('操作过于频繁')
            break
        for gonglue_ele in gonglue_eles:
            title = ''.join(gonglue_ele.xpath('.//h2/a//text()'))
            try:
                author = gonglue_ele.xpath('.//*[@class="user_name"]/a/text()')[0]
            except:
                author = ''
            try:
                play_time = gonglue_ele.xpath('.//*[@class="date"]/text()')[0].replace(' ', '').replace('出发', '')
            except:
                play_time = ''
            try:
                days_num = gonglue_ele.xpath('.//*[@class="days"]/text()')[0].replace(' ', '').replace('共', '').replace('天', '')
            except:
                days_num = gonglue_ele.xpath('.//*[@class="days"]/text()')[0].replace(' ', '').replace('共', '').replace('天', '')
            try:
                per_capita = gonglue_ele.xpath('.//*[@class="fee"]/text()')[0].replace(' ', '').replace('人均', '').replace('元', '')
            except:
                per_capita = ''
            try:
                with_whom = gonglue_ele.xpath('.//*[@class="people"]/text()')[0].replace(' ', '')
            except:
                with_whom = ''
            try:
                trip = gonglue_ele.xpath('.//*[@class="trip"]/text()')[0].replace(' ', '')
            except:
                trip = ''
            try:
                via_scenery = gonglue_ele.xpath('.//*[@class="places" and contains(text(),"途经")]/span/text()')[0]
            except:
                via_scenery = ''
            try:
                stroke = ''.join(gonglue_ele.xpath('.//*[@class="places" and contains(text(),"行程")]//text()')).replace('行程：', '')
            except:
                stroke = ''
            try:
                youji_id = re.search(r'\d+', gonglue_ele.xpath('.//*[@class="pic"][1]/a[last()]/@href')[0]).group(0)
            except:
                youji_id = ''
            if youji_id:
                youji_url = f'https://travel.qunar.com/travelbook/note/{youji_id}'
                r = requests.get(youji_url, headers=headers)
                time.sleep(round(random.uniform(3, 5), 2))
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
        df.to_excel(f'{scenery_list[i]}攻略2.xlsx', index=False)
