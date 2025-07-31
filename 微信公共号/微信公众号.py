import json
import time
from lxml import etree
import datetime
import pandas as pd
import requests

headers = {
    'Host': 'mp.weixin.qq.com',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf2540615) XWEB/16133',
    'Cookie': 'noticeLoginFlag=1; ua_id=ryT9XRB6gz8ZDuBtAAAAAHBDRiuZ2WxViH-Uy1etQnY=; wxuin=53930307910309; _clck=we7yzi|1|fy2|0; cert=NqiTANbDLa3f4lXaU8SIwVFGEHVhmzGC; openid=oWDr45DHynaPorM0x8ARE_DfplNs; noticeLoginFlag=1; remember_acct=18665448472%40sina.cn; xid=81307b826d7821baa870a2cb363f6c52; openid2ticket_oWDr45Fz1qgS2IcKzfNGFXS__LXU=NzTpPs97oaygTBx6H8POkwZcnipRVlRUF1DdtNLsCmQ=; mm_lang=zh_CN; uuid=e7346546910490763f97adb4fd735ab5; _qpsvr_localtk=0.5541045109407787; RK=jH25Y7hebW; ptcz=fb7da7b36632887e9904868543e2161d05f1335ea660d6d0cbc233888f220b56; data_bizuin=3198700521; bizuin=3198700521; master_user=gh_b40dc5016ec3; master_sid=ZnJMdHNmM0ptbW1EZGM2b3BVVGkzOWl5WTVtS3p2VFZQQzdVaWNTY25qOTF2WE4zWWVyc1R6VHk3ZDRHbUI1Y3dGN1RjVVE4QTI2UkZwRktXTGtzamtnNjRtU3lXaHJRNzl1TkhBQmJ1V0JNdVV0MHI5VXZlSlNwQk1oaE1VTEFtempJSDBibWdDaUI3ajVj; master_ticket=cd12c56598db975aabbedbfa78aa7694; data_ticket=LNCrhCqz+4vEi+ltmEkTlErj49E2ZCENl6UBUO94+qqOSQUZyk/4eOiXKdE6FP+p; rand_info=CAESINbI5orkLy2uvOp7biwn0WGGaMKlNzkpBlrL6yG4trY3; slave_bizuin=3198700521; slave_user=gh_b40dc5016ec3; slave_sid=dWVuR0dyNWNmQkVlTDd1OGloV2pVNjFNSXJaVjVGMHQzREJjQ2doOG5jck1YYkh6UUtNU0dsMlc5SUpZZFNDV0lzcHlXQ1loM0V2UDBmZ0h6RG5KY1pLMWcyUTIwaE5VYzVFcU56cHRya0lOMEIzVlp3RndVZFljbVRMdWgyT1Q1dnZkVVVIcGQ2Q21nb3hm; _clsk=1ddnjhy|1753931055881|9|1|mp.weixin.qq.com/weheat-agent/payload/record',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Dest': 'empty',
}

data = {
    '标题': [],
    '发布时间': [],
    '文章链接': [],
}

if __name__ == '__main__':
    base_url = 'https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin={}&count=1000000&query=&fakeid=Mzg4NTc3MjQ4MA%3D%3D&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=82f31b34f6ff61dc67ed6c92b687637b&token=399439404&lang=zh_CN&f=json&ajax=1'
    page = 0
    while True:
        print(f'正在爬取第{page // 5 + 1}页')
        url = base_url.format(page)
        response = requests.get(url=url, headers=headers)
        time.sleep(3)
        publish_list = json.loads(response.json()['publish_page'])['publish_list']
        if len(publish_list) == 0:
            break
        for publish in publish_list:
            article_list = json.loads(publish['publish_info'])['appmsgex']
            for article in article_list:
                title = article['title']
                publish_time = datetime.datetime.fromtimestamp(article['create_time']).strftime("%Y-%m-%d")
                link = article['link']
                print(f'{title}   {publish_time}   {link}')
                data['标题'].append(title)
                data['发布时间'].append(publish_time)
                data['文章链接'].append(link)
        page += 5
    print(f'共爬取{len(data["文章链接"])}条数据')
    df = pd.DataFrame(data)
    df.to_excel(f'公众号文章.xlsx', index=False)
