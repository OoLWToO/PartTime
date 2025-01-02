import os

import pandas as pd
from matplotlib import pyplot as plt

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}


def create_chart(classify, subject, score_list):
    table_name = f'{classify}学校{subject}专业分数线分布条形图'
    item = []
    value = []
    for d in score_list:
        if str(d) in item:
            index = item.index(str(d))
            value[index] += 1
        else:
            item.append(str(d))
            value.append(1)
    if len(item) < 2 or len(value) < 2:
        return
    sorted_pairs = sorted(zip(item, value), key=lambda pair: pair[0])
    sorted_items, sorted_values = zip(*sorted_pairs)
    plt.close('all')
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(6, 6))
    plt.xticks(rotation=45)
    plt.bar(sorted_items, sorted_values)
    plt.title(f'{table_name}')
    plt.xlabel('分数')
    plt.ylabel('数量')
    plt.savefig(f'图片/{table_name}')

if __name__ == '__main__':
    if not os.path.exists('./图片'):
        os.makedirs('./图片')
    df = pd.read_csv('../题目1/分数线统计(数学、计算机).csv')
    score_hebei = {}
    score_beijing = {}
    score_shanghai = {}
    score_985 = {}
    score_211 = {}
    for index, row in df.iterrows():
        if row['所在地区'] == '河北':
            if not score_hebei.get(row['专业名称']):
                score_hebei[row['专业名称']] = []
            score_hebei[row['专业名称']].append(row['总分'])
        if row['所在地区'] == '北京':
            if not score_beijing.get(row['专业名称']):
                score_beijing[row['专业名称']] = []
            score_beijing[row['专业名称']].append(row['总分'])
        if row['所在地区'] == '上海':
            if not score_shanghai.get(row['专业名称']):
                score_shanghai[row['专业名称']] = []
            score_shanghai[row['专业名称']].append(row['总分'])
        if row['是否为985'] == '是':
            if not score_985.get(row['专业名称']):
                score_985[row['专业名称']] = []
            score_985[row['专业名称']].append(row['总分'])
        if row['是否为211'] == '是':
            if not score_211.get(row['专业名称']):
                score_211[row['专业名称']] = []
            score_211[row['专业名称']].append(row['总分'])
    for key, value in score_hebei.items():
        create_chart('河北', key, value)
    for key, value in score_beijing.items():
        create_chart('北京', key, value)
    for key, value in score_shanghai.items():
        create_chart('上海', key, value)
    for key, value in score_985.items():
        create_chart('985', key, value)
    for key, value in score_211.items():
        create_chart('211', key, value)
