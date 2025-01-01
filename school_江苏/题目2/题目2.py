import os
import pandas as pd
from matplotlib import pyplot as plt

def generate_bar_chart(classification, subject, score_data):
    chart_title = f'{classification}学校{subject}专业分数线分布条形图'
    score_items = []
    score_counts = []
    for score in score_data:
        if str(score) in score_items:
            index = score_items.index(str(score))
            score_counts[index] += 1
        else:
            score_items.append(str(score))
            score_counts.append(1)
    if len(score_items) < 2 or len(score_counts) < 2:
        return
    sorted_pairs = sorted(zip(score_items, score_counts), key=lambda pair: pair[0])
    sorted_items, sorted_counts = zip(*sorted_pairs)
    plt.close('all')
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(6, 6))
    plt.xticks(rotation=45)
    plt.bar(sorted_items, sorted_counts)
    plt.title(f'{chart_title}')
    plt.xlabel('分数')
    plt.ylabel('数量')
    plt.savefig(f'图片/{chart_title}')

if __name__ == '__main__':
    if not os.path.exists('./图片'):
        os.makedirs('./图片')
    data_frame = pd.read_csv('../题目1/分数线统计(数学、计算机).csv')
    hebei_scores = {}
    beijing_scores = {}
    guangdong_scores = {}
    scores_985 = {}
    scores_211 = {}
    for index, row in data_frame.iterrows():
        if row['所在地区'] == '河北':
            if not hebei_scores.get(row['专业名称']):
                hebei_scores[row['专业名称']] = []
            hebei_scores[row['专业名称']].append(row['总分'])
        if row['所在地区'] == '北京':
            if not beijing_scores.get(row['专业名称']):
                beijing_scores[row['专业名称']] = []
            beijing_scores[row['专业名称']].append(row['总分'])
        if row['所在地区'] == '广东':
            if not guangdong_scores.get(row['专业名称']):
                guangdong_scores[row['专业名称']] = []
            guangdong_scores[row['专业名称']].append(row['总分'])
        if row['是否为985'] == '是':
            if not scores_985.get(row['专业名称']):
                scores_985[row['专业名称']] = []
            scores_985[row['专业名称']].append(row['总分'])
        if row['是否为211'] == '是':
            if not scores_211.get(row['专业名称']):
                scores_211[row['专业名称']] = []
            scores_211[row['专业名称']].append(row['总分'])
    for subject_name, scores in hebei_scores.items():
        generate_bar_chart('河北', subject_name, scores)
    for subject_name, scores in beijing_scores.items():
        generate_bar_chart('北京', subject_name, scores)
    for subject_name, scores in guangdong_scores.items():
        generate_bar_chart('广东', subject_name, scores)
    for subject_name, scores in scores_985.items():
        generate_bar_chart('985', subject_name, scores)
    for subject_name, scores in scores_211.items():
        generate_bar_chart('211', subject_name, scores)