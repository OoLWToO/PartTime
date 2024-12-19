from datetime import datetime

import pandas as pd
from openpyxl import Workbook

from selenium import webdriver


def create_driver():
    chrome_driver_path = '../driver/chromedriver_119.exe'
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=option)
    driver.implicitly_wait(.5)
    driver.maximize_window()
    return driver


if __name__ == "__main__":
    # 创建driver
    # driver = create_driver()
    # driver.get('https://data.eastmoney.com/gdfx/')
    # print('')
    # driver.quit()
    df = pd.read_excel('开发区合伙企业.xlsx')
    for status in df['纳税人名称']:
        data = {
            '股东名称': [],
            '股东类型': [],
            '持股变动': [],
            '统计次数': [],
            '平均涨幅（10日）': [],
            '最大涨幅（10日）': [],
            '最小涨幅（10日）': [],
            '平均涨幅（30日）': [],
            '最大涨幅（30日）': [],
            '最小涨幅（30日）': [],
            '平均涨幅（60日）': [],
            '最大涨幅（60日）': [],
            '最小涨幅（60日）': [],
            '持有个股': [],
        }
