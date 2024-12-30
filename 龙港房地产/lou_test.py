import pandas
from matplotlib import pyplot as plt

if __name__ == '__main__':
    df = pandas.read_csv('龙港房地产.csv')
    item = []
    value = []
    house_type = []
    for index, row in df.iterrows():
        house_type.append(row['户型'][:4])
    for d in house_type:
        if d in item:
            index = item.index(d)
            value[index] += 1
        else:
            item.append(d)
            value.append(1)
    combined = list(zip(item, value))
    sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)
    sorted_item, sorted_value = zip(*sorted_combined)
    # 将第七个以后整合成'其他'
    sorted_item = tuple(list(sorted_item[:7]) + ['其他'])
    sorted_value = tuple(list(sorted_value[:7]) + [sum(sorted_value[7:])])
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.pie(sorted_value, labels=sorted_item, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('龙港房地产房型统计饼图')
    plt.savefig('龙港房地产房型统计饼图.png')
