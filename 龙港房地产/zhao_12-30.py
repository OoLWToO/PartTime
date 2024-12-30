import pandas
from matplotlib import pyplot as plt

if __name__ == '__main__':
    df = pandas.read_csv('龙港房地产.csv')
    item = ['50万-', '50-59万', '60-69万', '70-79万', '80-89万', '90-99万', '100-109万', '110-119万',
            '120-129万', '130-139万', '140-149万', '150万+']
    value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for index, row in df.iterrows():
        try:
            if float(row['出售价格(万)']) <= 50:
                value[0] += 1
            elif 50 <= float(row['出售价格(万)']) <= 59:
                value[1] += 1
            elif 60 <= float(row['出售价格(万)']) <= 69:
                value[2] += 1
            elif 70 <= float(row['出售价格(万)']) <= 79:
                value[3] += 1
            elif 80 <= float(row['出售价格(万)']) <= 89:
                value[4] += 1
            elif 90 <= float(row['出售价格(万)']) <= 99:
                value[5] += 1
            elif 100 <= float(row['出售价格(万)']) <= 109:
                value[6] += 1
            elif 110 <= float(row['出售价格(万)']) <= 119:
                value[7] += 1
            elif 120 <= float(row['出售价格(万)']) <= 129:
                value[8] += 1
            elif 130 <= float(row['出售价格(万)']) <= 139:
                value[9] += 1
            elif 140 <= float(row['出售价格(万)']) <= 149:
                value[10] += 1
            elif float(row['出售价格(万)']) >= 150:
                value[11] += 1
        except:
            continue
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(12, 6))
    plt.bar(item, value)
    plt.title('龙港房地产总价统计条形图')
    plt.xlabel('总价')
    plt.ylabel('数量')
    plt.savefig('龙港房地产总价统计条形图.png')
