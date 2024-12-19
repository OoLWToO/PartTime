import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from wordcloud import WordCloud

# 设置请求头，用于模拟用户真实请求
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
    'accept-language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Cookie': 'HttpOnly; HttpOnly; wdcid=45144998a67f15c1; wdses=1ef46467e7098135; Hm_lvt_28a3153dcfb00d257d29dbb127cafeba=1718936207; bg4=3|ARbUF; wdlast=1718936943; Hm_lpvt_28a3153dcfb00d257d29dbb127cafeba=1718936943',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}


# 生成词云函数
def create_word_chart(year, content):
    wc = WordCloud(font_path="simsun.ttc", width=800, height=600, mode="RGBA", background_color=None).generate(content)
    plt.imshow(wc, interpolation='bilinear')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.axis("off")
    wc.to_file(f"{year}年词云统计.png")

if __name__ == '__main__':
    # 今年
    year = 2024
    url = 'http://hprc.cssn.cn/wxzl/wxysl/lczf/'
    r = requests.get(url, headers=headers)
    # 设置编码格式，不然会乱码
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.content, 'html.parser')
    # 查找所有class为"bl"的元素下的a标签
    url_list = soup.select('.bl a')
    # 只取前四个，也就是近四年，循环请求文章
    for url in url_list[:4]:
        # 因为获取到的href前面会有个‘.’，如'./shisijbg/202404/t20240429_5748667.html'，url["href"][1:]不取前面那个‘.’
        r = requests.get(f'http://hprc.cssn.cn/wxzl/wxysl/lczf{url["href"][1:]}')
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.content, 'html.parser')
        # 使用soup的CSS选择器来查找具有class为"TRS_Editor"的元素，取第一个获取到的元素获取text
        content = soup.select('.TRS_Editor')[0].text
        # 打开一个文本文件来存储元素内容
        with open(f'{year}.txt', 'w', encoding='utf-8') as file:
            file.write(str(content))
        # 生成词云
        create_word_chart(year, content)
        year -= 1
