import re
import pandas as pd
import requests
from pyecharts.charts import Map, Pie, Line, Bar
from pyecharts import options as opts

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "wzws_sessionid=oGduWqWCZmM1ZWUxgDIyMS40LjIxMC4xNjWBZjUyOWEz; JSESSIONID=QyAHESDrr33IzLjmg0Dw8zfW6cGBaoEMwRSYejeMgHWoiz6h9m_I!1186126168; u=6",
    "Host": "data.stats.gov.cn",
    "Referer": "https://data.stats.gov.cn/easyquery.htm?cn=E0103",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


# 地区代码对照表
region_dict = {
    '110000': "北京市",
    '120000': "天津市",
    '130000': "河北省",
    '140000': "山西省",
    '150000': "内蒙古自治区",
    '210000': "辽宁省",
    '220000': "吉林省",
    '230000': "黑龙江省",
    '310000': "上海市",
    '320000': "江苏省",
    '330000': "浙江省",
    '340000': "安徽省",
    '350000': "福建省",
    '360000': "江西省",
    '370000': "山东省",
    '410000': "河南省",
    '420000': "湖北省",
    '430000': "湖南省",
    '440000': "广东省",
    '450000': "广西壮族自治区",
    '460000': "海南省",
    '500000': "重庆市",
    '510000': "四川省",
    '520000': "贵州省",
    '530000': "云南省",
    '540000': "西藏自治区",
    '610000': "陕西省",
    '620000': "甘肃省",
    '630000': "青海省",
    '640000': "宁夏回族自治区",
    '650000': "新疆维吾尔自治区"
}

data = {
    '地区': [],
    '2014': [],
    '2015': [],
    '2016': [],
    '2017': [],
    '2018': [],
    '2019': [],
    '2020': [],
    '2021': [],
    '2022': [],
    '2023': [],
}


def create_map_chart(year):
    province_list = []
    # 遍历data，得出[地区, GDP]列表
    df = pd.DataFrame(data)
    for index, row in df.iterrows():
        province_list.append([row['地区'], row[year]])
    # 创建地图Map实例，设置宽高
    map = Map(init_opts=opts.InitOpts(width='1800px', height='1200px'))
    # 设置标题和最大值
    map.set_global_opts(
        title_opts=opts.TitleOpts(title=f"{year}年"),
        visualmap_opts=opts.VisualMapOpts(max_=60000))
    map.add(f"{year}年我国各地区生产总值数据", data_pair=province_list, maptype='china', is_roam=True)
    map.render(path=f"{year}年我国各地区生产总值数据.html")


def create_pie_chart(year):
    province_list = []
    # 遍历data，得出[地区, GDP]列表
    df = pd.DataFrame(data)
    for index, row in df.iterrows():
        province_list.append((row['地区'], row[year]))
    # 创建饼图Pie图实例，设置宽高
    pie = Pie(init_opts=opts.InitOpts(width='1800px', height='1200px'))
    pie.set_global_opts(
        title_opts=opts.TitleOpts(title=f"{year}年各地区生产总值占比", pos_left="center", pos_top="50px"),  # 设置标题
        legend_opts=opts.LegendOpts(is_show=True),  # 显示图例
    )
    # 设置标签格式
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    pie.add("", province_list)
    pie.render(f"{year}年各地区生产总值占比.html")


def create_line_chart():
    items = []
    for year in range(2014, 2024):
        items.append(f'{year}')
    # 创建折线图Line图实例，设置宽高
    line = Line(init_opts=opts.InitOpts(width='1800px', height='1200px'))
    # 设置x轴
    line.add_xaxis(items)
    # 遍历data，将该地区每年的GDP加入y轴列表
    df = pd.DataFrame(data)
    for index, row in df.iterrows():
        year_values = []
        for year in range(2014, 2024):
            year_values.append(row[f'{year}'])
        line.add_yaxis(row['地区'], year_values, is_smooth=True)
    line.set_global_opts(title_opts=opts.TitleOpts(title="2014-2023年我国各地区生产总值变化", pos_left="center", pos_top="50px"))
    line.render("2014-2023年我国各地区生产总值变化.html")


def create_custom_bar_chart(year):
    province_list = []
    # 遍历data，提取[地区, GDP]列表
    df = pd.DataFrame(data)
    for index, row in df.iterrows():
        province_list.append((row['地区'], row[year]))
    # 根据GDP排序
    sorted_data = sorted(province_list, key=lambda x: x[1], reverse=True)
    sorted_items, sorted_values = zip(*sorted_data)

    # 创建条形图Bar实例，设置宽高
    bar = Bar(init_opts=opts.InitOpts(width='1800px', height='1200px'))
    # 添加x轴和y轴
    bar.add_xaxis(list(sorted_items))
    bar.add_yaxis(f"{year}年GDP", list(sorted_values))

    # 设置标题，显示提示信息，类目型x轴，数值型y轴
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title=f"{year}年我国各地区生产总值条形图", pos_left="center", pos_top="50px"),
        tooltip_opts=opts.TooltipOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category", axislabel_opts={"rotate": 45}),  # X轴标签旋转以防重叠
        yaxis_opts=opts.AxisOpts(type_="value"),
    )
    bar.render(f"{year}年我国各地区生产总值条形图.html")


def create_bar_chart():
    items = []
    values = []
    # 遍历data，计算出该地区2014-2023年GDP总额
    df = pd.DataFrame(data)
    for index, row in df.iterrows():
        total_GDP = 0
        for year in range(2014, 2024):
            total_GDP += row[f'{year}']
        items.append(row['地区'])
        values.append(round(total_GDP, 2))
    # 根据y轴GDP总额打包排序
    combined = list(zip(items, values))
    sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)
    sorted_item, sorted_value = zip(*sorted_combined)
    # 创建条形图Bar实例，设置宽高
    bar = Bar(init_opts=opts.InitOpts(width='1800px', height='1200px'))
    # 添加x轴和y轴，只取前十个地区
    bar.add_xaxis(sorted_item[:10])
    bar.add_yaxis("GDP", sorted_value[:10])
    # 设置标题，显示提示信息，类目型x轴，数值型y轴
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="2014-2023年我国各地区GDP前十"),
        tooltip_opts=opts.TooltipOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category"),
        yaxis_opts=opts.AxisOpts(type_="value"),
    )
    bar.render("2014-2023年我国各地区GDP前十.html")


if __name__ == '__main__':
    url = 'https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A020101%22%7D%5D&dfwds=%5B%5D&k1=1735177846238&h=1'
    r = requests.get(url, headers=headers)
    GDP_datas = r.json()['returndata']['datanodes']
    for GDP_data in GDP_datas:
        code_data = GDP_data['code']
        # 根据地区代码映射表匹配数据对应的地区和年份
        # 例：code_data='zb.A020101_reg.110000_sj.2023'
        region = region_dict[re.search(r"_reg\.(\d{6})_sj", code_data).group(1)]
        year = re.search(r"_sj\.(\d{4})", code_data).group(1)
        GDP = GDP_data['data']['data']
        if region not in data['地区']:
            data['地区'].append(region)
        data[year].append(GDP)
        print(f'{region}   {year}   {GDP}')
    df = pd.DataFrame(data)
    df.to_excel(f'2014-2023年我国各地区生产总值数据.xlsx', index=False)
    # 创建['2014', '2017', '2020', '2023']年的地图表和饼图
    for year in ['2014', '2023']:
        create_map_chart(year)
        create_pie_chart(year)
        create_custom_bar_chart(year)
    create_line_chart()
    create_bar_chart()
