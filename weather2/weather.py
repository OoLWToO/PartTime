import csv

import mysql
import requests
from lxml import etree

# 设置请求头
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'Hm_lvt_e9daa3d2d6076d2d8ec79d05f050c0d5=1716811706,1716825458; Hm_lvt_029c70397ba7bba8caeb29017c83b8d8=1716811706,1716825458; Hm_lpvt_029c70397ba7bba8caeb29017c83b8d8=1716825462; Hm_lpvt_e9daa3d2d6076d2d8ec79d05f050c0d5=1716825462',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

# 连接到 MySQL 数据库
mydb = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="123456",
    database="dangdang"
)

# 创建一个指向数据库的游标
mycursor = mydb.cursor()


def write_to_mysql(date, weather, low_temperature, max_temperature):
    sql = "INSERT INTO book (date, weather, low_temperature, max_temperature) VALUES (%s, %s, %s, %s)"
    val = (date, weather, low_temperature, max_temperature)
    # 执行 SQL 查询
    mycursor.execute(sql, val)
    # 提交更改到数据库
    mydb.commit()


if __name__ == '__main__':
    # 发送请求，用etree转成html
    url = f'https://www.tianqi.com/jiangsu-xinbeiqu/16276/15'
    r = requests.get(url, headers=headers)
    html = etree.HTML(r.text)
    # 先存入标签行
    with open('suzhou.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['日期', '天气', '最低温度', '最高温度'])
    # 根据xpath获取天气列表
    weather_list = html.xpath('//*[@class="box_day"]/div')
    for ele in weather_list:
        # 日期xpath可能会变
        try:
            date = f'{ele.xpath(".//h3/b/text()")[0]} {ele.xpath(".//h3/em/text()")[0]}'
        except:
            date = f'{ele.xpath(".//h3/b/text()")[0]} {ele.xpath(".//h3/text()")[0].replace(" ", "")}'
        weather = ele.xpath('.//li[@class="temp"]/text()')[0]
        low_temperature = ele.xpath('.//li[@class="temp"]/text()')[1].replace('~', '')
        max_temperature = ele.xpath('.//li[@class="temp"]/b/text()')[0]
        print(f'{date}   {weather}   {low_temperature}   {max_temperature}')
        with open('suzhou.csv', 'a', encoding='utf-8-sig', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([date, weather, low_temperature, max_temperature])
        write_to_mysql(date, weather, low_temperature, max_temperature)
    # 关闭游标和数据库连接
    mycursor.close()
    mydb.close()
