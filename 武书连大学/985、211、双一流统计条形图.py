import pandas as pd
from matplotlib import pyplot as plt

if __name__ == '__main__':
    df = pd.read_csv("武书连大学数据.csv")
    item = ['985', '211', '双一流']
    value = [0, 0, 0]
    for index, row in df.iterrows():
        if row['985'] == '是':
            value[0] += 1
        if row['211'] == '是':
            value[1] += 1
        if row['双一流'] == '是':
            value[2] += 1
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(6, 6))
    plt.bar(item, value)
    plt.title('985、211、双一流统计条形图')
    plt.xlabel('类型')
    plt.ylabel('数量')
    plt.savefig('985、211、双一流统计条形图.png')