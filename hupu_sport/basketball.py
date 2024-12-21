import pandas as pd
import requests
from lxml import etree
import pandas as pd
import matplotlib.pyplot as plt

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

data = {
    '排名': [],
    '球员': [],
    '球队': [],
    '得分': [],
    '命中(出手)': [],
    '命中率': [],
    '命中(三分)': [],
    '三分命中率': [],
    '命中(罚球)': [],
    '罚球命中率': [],
    '场次': [],
    '上场时间': []
}


def getData():
    url = 'https://nba.hupu.com/stats/players/pts'
    r = requests.get(url, headers=headers)
    html = etree.HTML(r.text)
    players = html.xpath('//*[@class="players_table"]//tr')
    for player in players[1:]:
        ranking = player.xpath('./td[1]//text()')[0]
        name = player.xpath('./td[2]//text()')[0]
        team = player.xpath('./td[3]//text()')[0]
        score = player.xpath('./td[4]//text()')[0]
        hitShot = player.xpath('./td[5]//text()')[0]
        hitRate = player.xpath('./td[6]//text()')[0]
        hitThreePoints = player.xpath('./td[7]//text()')[0]
        hitThreePointsRate = player.xpath('./td[8]//text()')[0]
        hitFreeThrows = player.xpath('./td[9]//text()')[0]
        hitFreeThrowsRate = player.xpath('./td[10]//text()')[0]
        matches = player.xpath('./td[11]//text()')[0]
        playingTime = player.xpath('./td[12]//text()')[0]
        saveData(ranking, name, team, score, hitShot, hitRate, hitThreePoints, hitThreePointsRate, hitFreeThrows,
                 hitFreeThrowsRate, matches, playingTime)
    df = pd.DataFrame(data)
    df.to_excel('虎扑体育篮球选手数据统计.xlsx', index=False)


def saveData(ranking, name, team, score, hitShot, hitRate, hitThreePoints, hitThreePointsRate, hitFreeThrows,
             hitFreeThrowsRate, matches, playingTime):
    print(f'{ranking}   {name}   {team}   {score}   {hitShot}   {hitRate}   {hitThreePoints}   '
          f'{hitThreePointsRate}   {hitFreeThrows}   {hitFreeThrowsRate}   {matches}   {playingTime}')
    data['排名'].append(ranking)
    data['球员'].append(name)
    data['球队'].append(team)
    data['得分'].append(score)
    data['命中(出手)'].append(hitShot)
    data['命中率'].append(hitRate)
    data['命中(三分)'].append(hitThreePoints)
    data['三分命中率'].append(hitThreePointsRate)
    data['命中(罚球)'].append(hitFreeThrows)
    data['罚球命中率'].append(hitFreeThrowsRate)
    data['场次'].append(matches)
    data['上场时间'].append(playingTime)


if __name__ == '__main__':
    getData()
    # 读取Excel文件
    file_path = '虎扑体育篮球选手数据统计.xlsx'
    df = pd.read_excel(file_path)

    # 球员得分柱状图
    plt.figure(figsize=(10, 6))
    plt.bar(df['球员'], df['得分'])
    plt.xlabel('球员')
    plt.ylabel('得分')
    plt.title('球员得分柱状图')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.xticks(rotation=90)  # 旋转x轴标签，以便更好地显示
    plt.tight_layout()  # 自动调整子图参数, 使之填充整个图像区域
    plt.savefig('球员得分柱状图.png')  # 保存图表为PNG文件

    # 球员命中直方图
    plt.figure(figsize=(10, 6))
    plt.hist(df['命中率'], bins=20, color='blue', alpha=0.7)
    plt.xlabel('命中率（%）')
    plt.ylabel('球员数量')
    plt.title('球员命中率直方图')
    plt.xticks(rotation=90)  # 旋转x轴标签，以便更好地显示
    plt.savefig('球员命中直方图.png')  # 保存图表为PNG文件

    # 球员得分散点图
    plt.figure(figsize=(10, 6))
    plt.scatter(df['球员'], df['得分'])
    plt.xlabel('球员')
    plt.ylabel('得分')
    plt.title('球员得分散点图')
    plt.xticks(rotation=90)  # 旋转x轴标签，以便更好地显示
    plt.tight_layout()
    plt.savefig('球员得分散点图.png')  # 保存图表为PNG文件

    # 球员上场时间散点图
    plt.figure(figsize=(10, 6))
    plt.scatter(df['球员'], df['上场时间'])
    plt.xlabel('球员')
    plt.ylabel('上场时间（分钟）')
    plt.title('球员上场时间散点图')
    plt.xticks(rotation=90)  # 旋转x轴标签，以便更好地显示
    plt.tight_layout()
    plt.savefig('球员上场时间散点图.png')  # 保存图表为PNG文件
