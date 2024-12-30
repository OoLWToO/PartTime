import pandas
from matplotlib import pyplot as plt

if __name__ == '__main__':
    df = pandas.read_csv('龙港房地产.csv')
    item = ['49平米-', '50-59平米', '60-69平米', '70-79平米', '80-89平米', '90-99平米', '100-109平米', '110-119平米',
            '120-129平米', '130-139平米', '140-149平米', '150平米+']
    value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for index, row in df.iterrows():
        try:
            if float(row['面积(㎡)']) <= 49:
                value[0] += 1
            elif 50 <= float(row['面积(㎡)']) <= 59:
                value[1] += 1
            elif 60 <= float(row['面积(㎡)']) <= 69:
                value[2] += 1
            elif 70 <= float(row['面积(㎡)']) <= 79:
                value[3] += 1
            elif 80 <= float(row['面积(㎡)']) <= 89:
                value[4] += 1
            elif 90 <= float(row['面积(㎡)']) <= 99:
                value[5] += 1
            elif 100 <= float(row['面积(㎡)']) <= 109:
                value[6] += 1
            elif 110 <= float(row['面积(㎡)']) <= 119:
                value[7] += 1
            elif 120 <= float(row['面积(㎡)']) <= 129:
                value[8] += 1
            elif 130 <= float(row['面积(㎡)']) <= 139:
                value[9] += 1
            elif 140 <= float(row['面积(㎡)']) <= 149:
                value[10] += 1
            elif float(row['面积(㎡)']) >= 150:
                value[11] += 1
        except:
            continue
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(12, 6))
    plt.bar(item, value, color='#FFCC8D')
    plt.title('龙港房地产面积统计条形图')
    plt.xlabel('总价')
    plt.ylabel('数量')
    plt.savefig('龙港房地产面积统计条形图.png')
