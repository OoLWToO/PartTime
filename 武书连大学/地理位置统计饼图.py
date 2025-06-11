import pandas as pd
from matplotlib import pyplot as plt

if __name__ == '__main__':
    df = pd.read_csv("武书连大学数据.csv")
    item = []
    value = []
    for index, row in df.iterrows():
        if row['省份'] in item:
            index = item.index(row['省份'])
            value[index] += 1
        else:
            item.append(row['省份'])
            value.append(1)
    combined = list(zip(item, value))
    sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)
    sorted_item, sorted_value = zip(*sorted_combined)
    # 将第九个以后整合成'其他'
    sorted_item = tuple(list(sorted_item[:22]) + ['其他'])
    sorted_value = tuple(list(sorted_value[:22]) + [sum(sorted_value[22:])])
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(12, 12))
    plt.pie(sorted_value, labels=sorted_item, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('地理位置统计饼图')
    plt.savefig('地理位置统计饼图.png')