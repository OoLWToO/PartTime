import pandas as pd
import requests
from lxml import etree

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    "cookie": "x-web-secsdk-uid=7c92b141-0e12-4bb7-b894-68aa041bc29f; Hm_lvt_2667d29c8e792e6fa9182c20a3013175=1734759314; Hm_lpvt_2667d29c8e792e6fa9182c20a3013175=1734759314; HMACCOUNT=B052F3C9997EBC2C; csrf_session_id=340dc36c40ce27326db9dbf604be637f; s_v_web_id=verify_m4xqwlpt_Xzi5Ci3r_jvsG_4uPa_95vg_LV2P6kX1V5xU; ttwid=1%7CMuOj8HDPXZZj4kqu_g7ak7PuitCc0s9dsswnhya3nns%7C1734759295%7Ca56430b94f3db1244c7c31ba0a8318ded17afa7eee0c2b2fdc36e3098e4c9dc4; novel_web_id=7450734329674499636",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

data = {
    '小说链接': [],
    '图片链接': [],
    '小说题目': [],
    '阅读人数': [],
    '相关信息': [],
}

def getData():
    # 榜单id, 爬取科幻末世、都市日常
    category_id = ['8', '261']
    for category in category_id:
        # 每个offset十条数据
        url = f'https://fanqienovel.com/api/rank/category/list?app_id=1967&rank_list_type=3&offset=0&limit=30&category_id={category}&rank_version=&gender=1&rankMold=2&msToken=e3nRNiGt_GPwqhNkj3hn0s45NdIfyZtavf-TKg-m144pYTDhUYyq1djEjGhi1leiG5Ac0U-FX8-3O5TEox97io6mn5o8VnoruO0O3sBY1l1Rox_G6llH_xA86wBiK7A-&a_bogus=Y6-YkcheMsm1kjv3Yhkz9bkm0RD0YW5IgZEFB4oXGzwu'
        r = requests.get(url, headers=headers)
        book_list = r.json()['data']['book_list']
        for book in book_list:
            book_url = f'https://fanqienovel.com/page/{book["bookId"]}'
            image_url = book['thumbUri']
            read_num = book['read_count']
            # 标题和相关信息会乱码, 请求书籍详细页获取
            r = requests.get(book_url, headers=headers)
            html = etree.HTML(r.text)
            title = html.xpath('//*[@class="info-name"]//text()')[0]
            info = html.xpath('//*[@class="page-abstract-content"]//text()')[0].replace('\u3000', '')
            saveData(book_url, image_url, title, read_num, info)
    df = pd.DataFrame(data)
    df.to_excel('番茄小说榜单统计.xlsx', index=False)

def saveData(book_url, image_url, title, read_num, info):
    print(f'{book_url}   {image_url}   {title}   {read_num}   {info}')
    data['小说链接'].append(book_url)
    data['图片链接'].append(image_url)
    data['小说题目'].append(title)
    data['阅读人数'].append(read_num)
    data['相关信息'].append(info)

if __name__ == '__main__':
    getData()