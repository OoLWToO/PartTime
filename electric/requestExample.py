import pandas as pd
import requests
from lxml import etree
import re
import pandas as pd
import matplotlib.pyplot as plt

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

data = {
    '省份': [],
    '总发电量': [],
    '总发电量(同比增长)': [],
    '火电发电量': [],
    '火电发电量(同比增长)': [],
    '水电发电量': [],
    '水电发电量(同比增长)': [],
    '风力发电量': [],
    '风力发电量(同比增长)': [],
    '太阳能发电量': [],
    '太阳能发电量(同比增长)': [],
    '核电发电量': [],
    '核电发电量(同比增长)': [],
}

def create_chart():
    # 读取Excel文件
    df = pd.read_excel('31省份2024年1-3月发电量数据.xlsx')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 绘制各省发电总量柱状图
    plt.figure(figsize=(10, 8))
    plt.bar(df['省份'], df['总发电量'], color='skyblue')
    plt.xlabel('省份')
    plt.ylabel('总发电量 (亿千瓦时)')
    plt.title('各省发电总量柱状图')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('各省发电总量柱状图.png')

    # 绘制各省水力发电量柱状图
    plt.figure(figsize=(10, 8))
    plt.bar(df['省份'], df['水电发电量'], color='lightgreen')
    plt.xlabel('省份')
    plt.ylabel('水力发电量 (亿千瓦时)')
    plt.title('各省水力发电量柱状图')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('各省水力发电量柱状图.png')

    # 绘制各省火力发电量柱状图
    plt.figure(figsize=(10, 8))
    plt.bar(df['省份'], df['火电发电量'], color='orange')
    plt.xlabel('省份')
    plt.ylabel('火力发电量 (亿千瓦时)')
    plt.title('各省火力发电量柱状图')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('各省火力发电量柱状图.png')

    # 绘制各省发电总量饼图
    plt.figure(figsize=(10, 8))
    plt.pie(df['总发电量'], labels=df['省份'], autopct='%1.1f%%', startangle=140)
    plt.title('各省发电总量饼图')
    plt.savefig('各省发电总量饼图.png')

    # 绘制各省水力发电和火力发电饼图
    plt.figure(figsize=(10, 8))
    df['水电发电量'] = pd.to_numeric(df['水电发电量'], errors='coerce')
    df['火电发电量'] = pd.to_numeric(df['火电发电量'], errors='coerce')
    plt.pie([df['水电发电量'].sum(), df['火电发电量'].sum()], labels=['水力发电', '火力发电'], autopct='%1.1f%%',
            startangle=140)
    plt.title('各省水力发电和火力发电饼图')
    plt.savefig('各省水力发电和火力发电饼图.png')


if __name__ == '__main__':
    url = 'https://www.hxny.com/nd-102461-0-17.html'
    r = requests.get(url, headers=headers)
    html = etree.HTML(r.text)
    content_list = html.xpath('//*[@class="newsdtl03"]/p[contains(text(),"2024年1-3月")]/text()')
    for content in content_list:
        # 初始化变量
        provinces = ""
        total_generation = ""
        total_generation_growth = ""
        thermal_power_generation = ""
        thermal_power_generation_growth = ""
        water_power_generation = ""
        water_power_generation_growth = ""
        wind_power_generation = ""
        wind_power_generation_growth = ""
        solar_power_generation = ""
        solar_power_generation_growth = ""
        nuclear_power_generation = ""
        nuclear_power_generation_growth = ""
        # 匹配省份
        province_pattern = r'2024年1-3月，(?P<province>.+?)总发电量'
        province_match = re.search(province_pattern, content)
        if province_match:
            provinces = province_match.group('province').rstrip('总发电量')
        # 匹配总发电量和同比增长
        total_pattern = r'总发电量(?P<total_generation>-?\d+\.?\d*)亿千瓦时，同比增长(?P<total_growth>-?\d+\.?\d*%)'
        total_match = re.search(total_pattern, content)
        if total_match:
            total_generation = total_match.group('total_generation')
            total_generation_growth = total_match.group('total_growth')
        # 匹配火电发电量和同比增长
        thermal_pattern = r'火电发电量(?P<thermal_power>-?\d+\.?\d*)亿千瓦时，同比增长(?P<thermal_growth>-?\d+\.?\d*%)'
        thermal_match = re.search(thermal_pattern, content)
        if thermal_match:
            thermal_power_generation = thermal_match.group('thermal_power')
            thermal_power_generation_growth = thermal_match.group('thermal_growth')
        # 匹配水电发电量和同比增长
        water_pattern = r'水力发电量(?P<water_power>-?\d+\.?\d*)亿千瓦时，同比增长(?P<water_growth>-?\d+\.?\d*%)'
        water_match = re.search(water_pattern, content)
        if water_match:
            water_power_generation = water_match.group('water_power')
            water_power_generation_growth = water_match.group('water_growth')
        # 匹配风力发电量和同比增长
        wind_pattern = r'风力发电量(?P<wind_power>-?\d+\.?\d*)亿千瓦时，同比增长(?P<wind_growth>-?\d+\.?\d*%)'
        wind_match = re.search(wind_pattern, content)
        if wind_match:
            wind_power_generation = wind_match.group('wind_power')
            wind_power_generation_growth = wind_match.group('wind_growth')
        # 匹配太阳能发电量和同比增长
        solar_pattern = r'太阳能发电量(?P<solar_power>-?\d+\.?\d*)亿千瓦时，同比增长(?P<solar_growth>-?\d+\.?\d*%)'
        solar_match = re.search(solar_pattern, content)
        if solar_match:
            solar_power_generation = solar_match.group('solar_power')
            solar_power_generation_growth = solar_match.group('solar_growth')
        # 匹配核电发电量和同比增长
        nuclear_pattern = r'核电发电量(?P<nuclear_power>-?\d+\.?\d*)亿千瓦时，同比增长(?P<nuclear_growth>-?\d+\.?\d*%)'
        nuclear_match = re.search(nuclear_pattern, content)
        if nuclear_match:
            nuclear_power_generation = nuclear_match.group('nuclear_power')
            nuclear_power_generation_growth = nuclear_match.group('nuclear_growth')
        print(f'{provinces}   {total_generation}   {total_generation_growth}   {thermal_power_generation}   '
              f'{thermal_power_generation_growth}   {water_power_generation}   {water_power_generation_growth}   '
              f'{wind_power_generation}   {wind_power_generation_growth}   {solar_power_generation}   '
              f'{solar_power_generation_growth}   {nuclear_power_generation}   {nuclear_power_generation_growth}   ')
        # 存入data
        data['省份'].append(provinces)
        data['总发电量'].append(total_generation)
        data['总发电量(同比增长)'].append(total_generation_growth)
        data['火电发电量'].append(thermal_power_generation)
        data['火电发电量(同比增长)'].append(thermal_power_generation_growth)
        data['水电发电量'].append(water_power_generation)
        data['水电发电量(同比增长)'].append(water_power_generation_growth)
        data['风力发电量'].append(wind_power_generation)
        data['风力发电量(同比增长)'].append(wind_power_generation_growth)
        data['太阳能发电量'].append(solar_power_generation)
        data['太阳能发电量(同比增长)'].append(solar_power_generation_growth)
        data['核电发电量'].append(nuclear_power_generation)
        data['核电发电量(同比增长)'].append(nuclear_power_generation_growth)
    df = pd.DataFrame(data)
    df.to_excel('31省份2024年1-3月发电量数据.xlsx', index=False)
    create_chart()