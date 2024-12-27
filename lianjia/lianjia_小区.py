import random
import re
import time

import pandas as pd
import requests
from lxml import etree
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import ttk


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "qd.lianjia.com",
    "Referer": "https://qd.lianjia.com/chengjiao/pg3c1511063874668/",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "Cookie": "lianjia_uuid=62b46ef9-c80b-4d23-b1c3-e6cffb316b19; _ga=GA1.2.2048597721.1734934324; crosSdkDT2019DeviceId=u8qwx3--ics2qa-2do2pvnnl6yw43t-1othxnu9w; ftkrc_=3a4595dc-6ef2-434f-8363-f74f1e1b15c0; lfrc_=8ca2b90e-a545-4bbc-9750-dc975b9deffd; _ga_PV625F3L95=GS1.2.1734934814.1.1.1734936373.0.0.0; _jzqx=1.1734943662.1734943662.1.jzqsr=xa%2Elianjia%2Ecom|jzqct=/ershoufang/xixianxinquxian/.-; login_ucid=2000000038985323; lianjia_token=2.00137153e46bb8e06302dc7ad5327905c9; lianjia_token_secure=2.00137153e46bb8e06302dc7ad5327905c9; security_ticket=jEE/ouguLzUAjSXtqtxqxga3wGNuiyhZ6oqeyOnExUrdNxqANJ/kQ62yjqeik8CwinpUuyH7AGowjfTyb8Zivvj7eWZcsu4jQkvdMgNpjMFcDYp7HZoFeFdTs+/d/w3PfWlJO+QeL0L1gGUNgo245uEdg+QRwhlHm69gPzZ9J6U=; _ga_N51MBR7HR4=GS1.2.1735091273.1.1.1735091309.0.0.0; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22193f224b89719ca-029068245990a3-26031051-1327104-193f224b89821fd%22%2C%22%24device_id%22%3A%22193f224b89719ca-029068245990a3-26031051-1327104-193f224b89821fd%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wyzh%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoxau%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; _ga_WGKDF6B591=GS1.2.1735095100.3.1.1735095219.0.0.0; select_city=370200; lianjia_ssid=047c504e-cce9-466c-95c6-7821b34f3e9d; Hm_lvt_46bf127ac9b856df503ec2dbf942b67e=1734943662,1735091262,1735095088,1735183050; HMACCOUNT=CD82991D93936EF5; _qzjc=1; _jzqa=1.80855173081169230.1734934313.1734943662.1735183050.3; _jzqc=1; _jzqckmp=1; _gid=GA1.2.2000266407.1735183062; Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e=1735183092; _qzja=1.425118837.1735183050293.1735183050293.1735183050293.1735183070738.1735183092121.0.0.0.3.1; _qzjb=1.1735183050293.3.0.0.0; _qzjto=3.1.0; _jzqb=1.3.10.1735183050.1; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiZWQwMTAxNjgwNGRmM2YwMTQzODUyNmQwNmE4Y2Q0NDY4MTM5ZmI4NmQyNTk5ZTg0OWQ3Y2ViYzcxNzlkNmVjNmZmNzYxMTk3N2U0NGRjOThkNWI4Yjg2ZTM3NzcxYWJhZWRkY2E5YzU0OTI5ZGY1N2IyYTBjODAyMDM5MDcwNWRhMmZiY2QwNTI1MWE3ODQ4ZGI4MDNiZjBmNGRiNTg1MjJlOTY2ZDQyMTY4Nzk5Y2NjYmM0MDlmMWZiODM0NThkMWRmMmJjNDE5OGVhM2MwOGYwZWFjOWExNzNlZDVmM2YzZjE4MjhiZGRjYjA4NTk0ZmUzYjBiOWRjODNhZDBjOFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCIxMGI0NjA1YlwifSIsInIiOiJodHRwczovL3FkLmxpYW5qaWEuY29tL2NoZW5namlhby9wZzEwYzE1MTEwNjM4NzQ2NjgvIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0=; _ga_EYZV9X59TQ=GS1.2.1735183062.2.1.1735183105.0.0.0; _ga_DX18CJBZRT=GS1.2.1735183062.2.1.1735183105.0.0.0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

data = {
    '标题': [],
    '总价(万)': [],
    '单价(元/平)': [],
    '户型': [],
    '面积': [],
    '售出时间': [],
    '朝向': [],
    '装修情况': [],
    '楼层': [],
    '建筑类型': [],
    '标签': [],
    '挂牌价': [],
    '成交周期(天)': [],
    '经纪人': [],
}


def create_plot_chart():
    chart_type = combo1.get()
    start = int(combo2.get())
    end = int(combo3.get())
    # count用于计算总数, value用于计算价格
    count = []
    value = []
    item = []
    for year in range(start, end + 1):
        value.append(0)
        item.append(str(year))
        count.append(0)
    df = pd.read_csv('青岛万科城多伦多街区小区销售数据.csv')
    for index, row in df.iterrows():
        if row['售出时间'][:4] in item:
            if chart_type != '销量':
                value[item.index(row['售出时间'][:4])] += row[chart_type]
            count[item.index(row['售出时间'][:4])] += 1
    for index, v in enumerate(value):
        if count[index] != 0:
            value[index] = v / count[index]
    # 创建折线图
    if chart_type != '销量':
        plt.plot(item, value, marker='o')
    else:
        plt.plot(item, count, marker='o')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    if chart_type == '销量':
        plt.title(f'{start}年-{end}年青岛万科城多伦多街区小区{chart_type}折线图')
    else:
        plt.title(f'{start}年-{end}年青岛万科城多伦多街区小区平均{chart_type}折线图')
    plt.xlabel('年份')
    plt.ylabel(chart_type)
    plt.grid(True)
    plt.legend([chart_type])
    plt.show()


def get_data():
    for page in range(10):
        # 发送请求
        url = f'https://qd.lianjia.com/chengjiao/pg{page + 1}c1511063874668/'
        r = requests.get(url, headers=headers)
        print(url)
        # time.sleep一下，防止被封ip
        time.sleep(round(random.uniform(5, 20), 2))
        html = etree.HTML(r.text)
        house_list = html.xpath('//*[@class="listContent"]/li')
        for house in house_list:
            title = house.xpath('.//*[@class="title"]/a/text()')[0]
            total_price = house.xpath('.//*[@class="totalPrice"]/span/text()')[0]
            unit_price = house.xpath('.//*[@class="unitPrice"]/span/text()')[0]
            sold_time = house.xpath('.//*[@class="dealDate"]/text()')[0]
            house_info = house.xpath('.//*[@class="houseInfo"]/text()')[0]
            position_info = house.xpath('.//*[@class="positionInfo"]/text()')[0]
            deal_house_info = ''.join(house.xpath('.//*[@class="dealHouseTxt"]//text()'))
            deal_cyclee_info = ''.join(house.xpath('.//*[@class="dealCycleTxt"]//text()'))
            agent = house.xpath('.//*[@class="agentInfoList"]/a/text()')[0]
            # 数据预处理
            house_type = re.search(r'(\d+)室(\d+)厅', title).group(0)
            house_area = re.search(r'(\d+\.?\d*)平米', title).group(1)
            towards = re.search(r'(\w+)\s*\|\s*(\w+)', house_info).group(1)
            decoration_situation = re.search(r'(\w+)\s*\|\s*(\w+)', house_info).group(2)
            floor = position_info[:position_info.find(' ')]
            building_type = position_info[position_info.find(' ') + 1:]
            listing_price = re.search(r'挂牌(\d+\.?\d*)万', deal_cyclee_info).group(1)
            cycle_match = re.search(r'成交周期(\d+)天', deal_cyclee_info)
            if cycle_match:
                transaction_cycle = cycle_match.group(1)
            else:
                transaction_cycle = ''
            print(f'{title}   {total_price}   {unit_price}   {house_type}   {house_area}   {sold_time}   {towards}   '
                  f'{decoration_situation}   {floor}   {building_type}   {deal_house_info}   {listing_price}   '
                  f'{transaction_cycle}   {agent}')
            # 数据存入data
            data['标题'].append(title)
            data['总价(万)'].append(total_price)
            data['单价(元/平)'].append(unit_price)
            data['户型'].append(house_type)
            data['面积'].append(house_area)
            data['售出时间'].append(sold_time)
            data['朝向'].append(towards)
            data['装修情况'].append(decoration_situation)
            data['楼层'].append(floor)
            data['建筑类型'].append(building_type)
            data['标签'].append(deal_house_info)
            data['挂牌价'].append(listing_price)
            data['成交周期(天)'].append(transaction_cycle)
            data['经纪人'].append(agent)
    df = pd.DataFrame(data)
    df.to_csv('青岛万科城多伦多街区小区销售数据.csv', encoding='utf-8-sig', index=False)


if __name__ == '__main__':
    # get_data()
    root = tk.Tk()
    root.title("可视化界面")

    # 设置窗口大小（可选）
    root.geometry("320x200")

    # 创建一个Frame用于放置下拉框
    frame = tk.Frame(root)
    frame.pack(pady=20)  # 将frame放置在窗口中，并在垂直方向上留出20像素的边距

    # 定义下拉框的选项
    visualization_options = ['总价(万)', '单价(元/平)', '销量']
    date_options = [str(year) for year in range(2010, 2025)]

    # 创建第一个下拉框：可视化数据
    label1 = tk.Label(root, text="可视化数据：")
    label1.place(x=10, y=30)  # 将标签放置在窗口中，x=10, y=10的位置
    combo1 = ttk.Combobox(root, values=visualization_options)
    combo1.place(x=120, y=30)  # 将下拉框放置在窗口中，x=120, y=10的位置

    # 创建第二个下拉框：爬取日期
    label2 = tk.Label(root, text="爬取日期：")
    label2.place(x=10, y=80)
    label3 = tk.Label(root, text="-")
    label3.place(x=195, y=80)
    # 将标签放置在窗口中，x=10, y=50的位置
    combo2 = ttk.Combobox(root, values=date_options, width=7)
    combo2.place(x=120, y=80)  # 将下拉框放置在窗口中，x=120, y=50的位置
    combo3 = ttk.Combobox(root, values=date_options, width=7)
    combo3.place(x=210, y=80)  # 将下拉框放置在窗口中，x=120, y=50的位置

    # 创建按钮：生成
    button_generate = tk.Button(root, text="生成", command=create_plot_chart)
    button_generate.place(x=120, y=120, width=100)  # 将按钮放置在窗口中，x=160, y=100的位置

    # 运行主循环
    root.mainloop()