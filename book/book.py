import pandas as pd
import requests
from lxml import etree
from matplotlib import pyplot as plt

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Cookie': '__jsluid_s=c9bf2381199315a3f9d70fab5efbea9b; __jsl_clearance_s=1718590950.375|0|BNVMH65p0N9580f3nELVxfBlj1g%3D; PHPSESSID=mnnnrrlijttt606feek3bkdvg0; mfw_uuid=666f9de7-be92-5b8a-42db-f09d461618a6; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222024-06-17+10%3A22%3A31%22%3B%7D; __mfwc=direct; __mfwa=1718590951232.55084.1.1718590951232.1718590951232; __mfwlv=1718590951; __mfwvn=1; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1718590951; uva=s%3A150%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1718590952%3Bs%3A10%3A%22last_refer%22%3Bs%3A82%3A%22https%3A%2F%2Fwww.mafengwo.cn%2Flocaldeals%2F0-0-M10132-0-0-0-0-0.html%3Ffrom%3Dlocaldeals_index%22%3Bs%3A5%3A%22rhost%22%3BN%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1718590952%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=666f9de7-be92-5b8a-42db-f09d461618a6; __mfwb=7d6d46205828.2.direct; __mfwlt=1718590972; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1718590973; bottom_ad_status=0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

bookTag = {
    '电子': '2a8f1030-fa2f-403a-9f38-76cfe875c184',
    '数学': '34858549-baec-4292-b5f0-23064a7ccb6f',
    '通讯': '923f77a9-018e-4872-9326-cf9c255a2a32',
}

orderStr = {
    '最新': 'publish',
    '最热': 'hot',
    '价格升序': 'price-low',
    '价格降序': 'price-up',
}

data = {
    '类别': [],
    '排序方式': [],
    '图书名称': [],
    '图书作者': [],
    '作者简介': [],
    '原价': [],
    '折扣价': [],
    '图书简介': [],
}


def create_price_chart(price_list, book_type, book_order):
    item = ['19元-', '20-29元', '30-39元', '40-49元', '50-59元', '60-69元', '70-79元', '80-89元', '90-99元', '100元+']
    value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for d in price_list:
        try:
            if float(d) <= 19:
                value[0] += 1
            elif 20 <= float(d) <= 29:
                value[1] += 1
            elif 30 <= float(d) <= 39:
                value[2] += 1
            elif 40 <= float(d) <= 49:
                value[3] += 1
            elif 50 <= float(d) <= 59:
                value[4] += 1
            elif 60 <= float(d) <= 69:
                value[5] += 1
            elif 70 <= float(d) <= 79:
                value[6] += 1
            elif 80 <= float(d) <= 89:
                value[7] += 1
            elif 90 <= float(d) <= 99:
                value[8] += 1
            elif float(d) >= 100:
                value[9] += 1
        except:
            continue
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(12, 6))
    plt.bar(item, value)
    plt.title(f'{book_type}图书{book_order}排序价格统计条形图')
    plt.xlabel('价格')
    plt.ylabel('数量')
    plt.savefig(f'{book_type}图书{book_order}排序价格统计条形图.png')


if __name__ == '__main__':
    url = 'https://www.ptpress.com.cn/bookinfo/getBookListForEBTag'
    for tag in bookTag:
        price_data = []
        for order in orderStr:
            parameter = {'page': '1', 'rows': '20', 'bookTagId': bookTag[f'{tag}'], 'orderStr': orderStr[f'{order}']}
            r = requests.post(url, headers=headers, data=parameter)
            book_list = r.json()['data']['data']
            for b in book_list:
                r = requests.post(f'https://www.ptpress.com.cn/bookinfo/getBookDetailsById', headers=headers,
                                  data={'bookId': b['bookId']})
                book = r.json()['data']
                # 排序方式、类别、图书名称、图书作者、作者简介、原价、折扣价、图书简介等
                book_name = book["bookName"]
                try:
                    author = book["author"]
                except:
                    author = ''
                try:
                    author_info = book["authorIntro"]["data"].replace('<p>', '').replace('</p>', '')
                except:
                    author_info = ''
                price = book['price']
                discount_price = book["discountPrice"]
                try:
                    book_info = book["resume"]["data"].replace('<p>', '').replace('</p>', '')
                except:
                    book_info = ''
                print(
                    f'{tag}   {order}   {book_name}   {author}   {author_info}   {price}   {discount_price}   {book_info}')
                data['类别'].append(tag)
                data['排序方式'].append(order)
                data['图书名称'].append(book_name)
                data['图书作者'].append(author)
                data['作者简介'].append(author_info)
                data['原价'].append(price)
                data['折扣价'].append(discount_price)
                data['图书简介'].append(book_info)
                price_data.append(discount_price)
            create_price_chart(price_data, tag, order)
        df = pd.DataFrame(data)
        df.to_csv('人民邮电出版社图书数据.csv', encoding='utf-8-sig', index=False)
