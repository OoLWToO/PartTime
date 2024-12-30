import requests
import pandas as pd
import matplotlib.pyplot as plt

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    'Cookie': '__permanent_id=20241216144216388783570476774906337; dangdang.com=email=MTg2NjU0NDg0NzI4MDg5MEBkZG1vYmlscGhvbmVfX3VzZXIuY29t&nickname=&display_id=4766850823709&customerid=pHb+Fh5jzxhaYY5fEB+3EA==&viptype=ayHYXk7x4cc=&show_name=186****8472; __visit_id=20241220163438756375720133582533937; __out_refer=; secret_key=22f3133e23d4f3adee29f838b4af8e2a; MDD_channelId=70000; MDD_fromPlatform=307; producthistoryid=1901349244; ddscreen=2; dest_area=country_id%3D9000%26province_id%3D111%26city_id%3D0%26district_id%3D0%26town_id%3D0; pos_9_end=1734683971912; pos_0_end=1734683972071; ad_ids=3618801%7C%231; pos_0_start=1734683981904; sessionID=pc_9acc76d9a2892b72577dbf62dcd3b8023636c5f0cbc251e6d0a8f5bbce01dd3e; USERNUM=31L5l/h0tGSDYvFwilByaQ==; login.dangdang.com=.ASPXAUTH=fIDHc6OZ19F19nnaQ93AvozkhkvUjGacGaHuev/d2xvcUHPGfN2NHw==; ddoy=email=1866544847280890@ddmobilphone__user.com&nickname=&validatedflag=0&uname=&utype=1&.ALFG=off&.ALTM=1734684008570; LOGIN_TIME=1734684009378; pos_6_end=1734684057238; pos_6_start=1734684057354; __trace_id=20241220164059903172719220825530478; __rpm=%7Cp_21055821.comment_long_body..1734684065159',
}

data = {
    '一级分类': [],
    '二级分类': [],
    '品名': [],
    '最低价': [],
    '平均价': [],
    '最高价': [],
    '规格': [],
    '产地': [],
    '单位': [],
    '发布日期': [],
}

post_data = {
    'limit': '20000',
    'current': '1',
    'pubDateStartTime': '2023/01/01',
    'pubDateEndTime': '2024/12/31',
    'prodPcatid': '1190',
    'prodCatid': '1210',
    'prodName': '黄花鱼',
}


def create_250g_price_chart():
    table_name = f'2023-2024-250g黄花鱼平均价统计条形图'
    item = []
    value = []
    for index, d in df.iterrows():
        # 排除其他规格
        if '250' not in d['规格']:
            continue
        if d['平均价'] in item:
            index = item.index(d['平均价'])
            value[index] += 1
        else:
            item.append(d['平均价'])
            value.append(1)
    sorted_pairs = sorted(zip(item, value), key=lambda pair: pair[0])
    sorted_items, sorted_values = zip(*sorted_pairs)
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(12, 6))
    plt.bar(sorted_items, sorted_values)
    plt.title(table_name)
    plt.xlabel('价格（元）')
    plt.ylabel('数量')
    plt.xticks(rotation=45)
    plt.savefig(table_name)


def create_500g_price_chart():
    table_name = f'2023-2024-500g黄花鱼平均价统计条形图'
    item = []
    value = []
    for index, d in df.iterrows():
        # 排除其他规格
        if '500' not in d['规格']:
            continue
        if d['平均价'] in item:
            index = item.index(d['平均价'])
            value[index] += 1
        else:
            item.append(d['平均价'])
            value.append(1)
    sorted_pairs = sorted(zip(item, value), key=lambda pair: pair[0])
    sorted_items, sorted_values = zip(*sorted_pairs)
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(12, 6))
    plt.bar(sorted_items, sorted_values)
    plt.title(table_name)
    plt.xlabel('价格（元）')
    plt.ylabel('数量')
    plt.xticks(rotation=45)
    plt.savefig(table_name)


def create_750g_price_chart():
    table_name = f'2023-2024-750g黄花鱼平均价统计条形图'
    item = []
    value = []
    for index, d in df.iterrows():
        # 排除其他规格
        if '750' not in d['规格']:
            continue
        if d['平均价'] in item:
            try:
                index = item.index(d['平均价'])
            except:
                print()
            value[index] += 1
        else:
            item.append(d['平均价'])
            value.append(1)
    sorted_pairs = sorted(zip(item, value), key=lambda pair: pair[0])
    sorted_items, sorted_values = zip(*sorted_pairs)
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(12, 6))
    plt.bar(sorted_items, sorted_values)
    plt.title(table_name)
    plt.xlabel('价格（元）')
    plt.ylabel('数量')
    plt.xticks(rotation=45)
    plt.savefig(table_name)


def create_scatter_chart():
    table_name = f'2023-2024-黄花鱼规格与平均价格散点图'
    df = pd.DataFrame(data)
    # 将规格转换为数值型，方便计算和比较
    spec_to_value = {
        '250g左右/鲜': 250,
        '500g左右/鲜': 500,
        '750g左右/鲜': 750
    }
    # 将规格转换为数值
    df['规格数值'] = df['规格'].map(spec_to_value)
    # 确保平均价格列为数值类型
    df['平均价'] = pd.to_numeric(df['平均价'], errors='coerce')
    # 去除平均价格中的NaN值
    df = df.dropna(subset=['平均价'])
    # 创建散点图
    plt.figure(figsize=(12, 8))
    colors = {'250g左右/鲜': 'red', '500g左右/鲜': 'green', '750g左右/鲜': 'blue'}
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 绘制每个规格的散点图
    for spec, color in colors.items():
        spec_df = df[df['规格'] == spec]
        plt.scatter(spec_df['规格数值'], spec_df['平均价'], color=color, label=spec)
    # 添加图例
    plt.legend()
    # 添加标题和坐标轴标签
    plt.title(table_name)
    plt.xlabel('规格（克）')
    plt.ylabel('平均价格（元/斤）')
    plt.grid(True)
    # 保存图表
    plt.savefig(table_name)


if __name__ == '__main__':
    url = 'http://www.xinfadi.com.cn/getPriceData.html'
    response = requests.post(url=url, data=post_data, headers=headers).json()
    products = response['list']
    for product in products:
        classification_one = product['prodCat']
        classification_two = product['prodPcat']
        name = product['prodName']
        lowest_price = product['lowPrice']
        average_price = product['avgPrice']
        highest_price = product['highPrice']
        size = product['specInfo']
        origin = product['place']
        unit = product['unitInfo']
        release_date = product['pubDate'][:10]
        # 排除'小黄花鱼', 去除掉价格小于10的错误项
        if '小' in name or float(lowest_price) < 10 or float(average_price) < 10 or float(highest_price) < 10:
            continue
        print(f'{classification_one}   {classification_two}   {name}   {lowest_price}   {average_price}   '
              f'{highest_price}   {size}   {origin}   {unit}   {release_date}')
        data['一级分类'].append(classification_one)
        data['二级分类'].append(classification_two)
        data['品名'].append(name)
        data['最低价'].append(lowest_price)
        data['平均价'].append(average_price)
        data['最高价'].append(highest_price)
        data['规格'].append(size)
        data['产地'].append(origin)
        data['单位'].append(unit)
        data['发布日期'].append(release_date)
    df = pd.DataFrame(data)
    df.to_csv('2023-2024国产黄花鱼数据统计.csv', encoding='utf-8-sig', index=False)
    create_250g_price_chart()
    create_500g_price_chart()
    create_750g_price_chart()
    create_scatter_chart()
