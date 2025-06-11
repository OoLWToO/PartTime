import pandas as pd
from matplotlib import pyplot as plt
from wordcloud import WordCloud

if __name__ == '__main__':
    df = pd.read_csv("武书连大学数据.csv")
    word_str = ''
    for index, row in df.iterrows():
        word_str += f'{row["学校类型"]} '
    wc = WordCloud(
        font_path="simsun.ttc",  # 或指定绝对路径
        width=800,
        height=600,
        background_color="white",
        mode="RGB"
    ).generate(word_str)

    # 显示并保存
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.title('学校类型统计词云')
    wc.to_file('学校类型统计词云.png')

