import requests
from matplotlib import pyplot as plt

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

if __name__ == '__main__':
    url = 'https://www.wurank.net/api/product/detail?action=Buildjson&id=23880&type=1&parentUniversityId=25&compareId=23881&year=2025'
    r = requests.get(url, headers=headers).json()
    rank_list = r['universityHistoryList']
    item = []
    value = []
    for rank in reversed(rank_list):
        item.append(rank['parentName'])
        value.append(rank['value'])
    plt.figure(figsize=(12, 6))
    plt.plot(item, value)  # 画折线
    plt.xlabel('年份')  # 添加X轴名称
    plt.ylabel('排名')  # 添加Y轴名称
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title('上海交通大学排名变化统计折线图')
    plt.savefig('上海交通大学排名变化统计折线图.png')
