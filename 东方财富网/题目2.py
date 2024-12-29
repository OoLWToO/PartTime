from datetime import datetime, timedelta

import pandas as pd
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import ttk


def get_ranking_data():
    date = combo1.get()
    df = pd.read_excel(f'{date}东方财富网榜单数据.xlsx')
    print(df)


def get_shareholders_data():
    # 获取两个日期之间的所有日期
    start_date = combo1.get()
    end_date = combo2.get()
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    date_list = []
    current_date = start
    while current_date <= end:
        date_list.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    df = pd.read_excel('东方财富网股东户数数据.xlsx')
    up_values = [0 for _ in date_list]
    fall_values = [0 for _ in date_list]
    for index, row in df.iterrows():
        if row['公告日期'] in date_list:
            if row['涨幅大于10%'] == '是':
                up_values[date_list.index(row['公告日期'])] += 1

            if row['跌幅大于10%'] == '是':
                fall_values[date_list.index(row['公告日期'])] += 1
    plt.figure(figsize=(12, 6))
    plt.plot(date_list, up_values, marker='o')
    plt.plot(date_list, fall_values, marker='o')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title(f'{start_date}年-{end_date}年股东数据涨跌数量折线统计图')
    plt.xlabel('年份')
    plt.ylabel('数量')
    plt.grid(True)
    plt.show()
    print(date_list)
    print(df)


if __name__ == '__main__':
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    root = tk.Tk()
    root.title("可视化界面")
    # 设置窗口大小（可选）
    root.geometry("320x150")
    # 创建一个Frame用于放置下拉框
    frame = tk.Frame(root)
    frame.pack(pady=20)  # 将frame放置在窗口中，并在垂直方向上留出20像素的边距
    # 定义下拉框的选项
    date_options = ['2024-12-26', '2024-12-27', '2024-12-28', '2024-12-29', '2024-12-30',
                    '2024-12-31', '2025-01-01', '2025-01-02', '2025-01-03']
    # 创建日期选择
    label1 = tk.Label(root, text="爬取日期：")
    label1.place(x=10, y=40)
    label2 = tk.Label(root, text="-")
    label2.place(x=180, y=40)
    combo1 = ttk.Combobox(root, values=date_options, width=11)
    combo1.place(x=80, y=40)
    combo2 = ttk.Combobox(root, values=date_options, width=11)
    combo2.place(x=190, y=40)
    # 创建按钮
    button1 = tk.Button(root, text="获取榜单数据", command=get_ranking_data)
    button1.place(x=50, y=80, width=100)
    button2 = tk.Button(root, text="获取股东户数数据", command=get_shareholders_data)
    button2.place(x=170, y=80, width=100)
    # 运行主循环
    root.mainloop()