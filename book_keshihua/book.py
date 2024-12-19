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


def create_number_chart(df):
    item = ['电子', '数学与统计学', '通信']
    value = [0, 0, 0]
    value[0] = df[df['类别'] == item[0]].shape[0]
    value[1] = df[df['类别'] == item[1]].shape[0]
    value[2] = df[df['类别'] == item[2]].shape[0]
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(8, 6))
    plt.bar(item, value)
    plt.title(f'各图书数量统计条形图')
    plt.xlabel('类型')
    plt.ylabel('数量')
    plt.savefig(f'各图书数量统计条形图.png')


def create_price_chart(price_list, book_type):
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
    plt.title(f'{book_type}图书价格统计条形图')
    plt.xlabel('价格')
    plt.ylabel('数量')
    plt.savefig(f'{book_type}图书价格统计条形图.png')


def create_pie_chart(data, chart_name):
    item = []
    value = []
    for d in data:
        if d in item:
            index = item.index(d)
            value[index] += 1
        else:
            item.append(d)
            value.append(1)
    combined = list(zip(item, value))
    sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)
    sorted_item, sorted_value = zip(*sorted_combined)
    sorted_item = tuple(list(sorted_item[:5]) + ['其他'])
    sorted_value = tuple(list(sorted_value[:5]) + [sum(sorted_value[8:])])
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.pie(sorted_value, labels=sorted_item, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title(f'书籍{chart_name}统计饼图')
    plt.savefig(f'书籍{chart_name}统计饼图.png')


if __name__ == '__main__':
    df = pd.read_csv('人邮图书.csv')
    create_number_chart(df)
    create_price_chart(df[df['类别'] == '电子']['价格'], '电子')
    create_price_chart(df[df['类别'] == '数学与统计学']['价格'], '数学与统计学')
    create_price_chart(df[df['类别'] == '通信']['价格'], '通信')
    create_pie_chart(df['包装'], '包装')
    create_pie_chart(df['开本'], '开本')
