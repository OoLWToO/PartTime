import time
from datetime import datetime

import pandas as pd
from openpyxl import Workbook

from selenium import webdriver


data = {
    '股东名称': [],
    '股东类型': [],
    '股东排名': [],
    '股票代码': [],
    '股票简称': [],
    '报告期': [],
    '数量(股)': [],
    '持股占流通股比(%)': [],
    '数量变化比例(股)': [],
    '数量变化比例(%)': [],
    '持股变动': [],
    '流通市值(元)': [],
    '公告日': [],
}


def create_driver():
    chrome_driver_path = '../driver/chromedriver_119.exe'
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=option)
    driver.implicitly_wait(1)
    driver.maximize_window()
    return driver


if __name__ == "__main__":
    # 创建driver
    driver = create_driver()
    driver.get('https://data.eastmoney.com/gdfx/')
    # 读取文件
    df = pd.read_excel('全市合伙企业.xlsx')
    for company in df['纳税人名称']:
        # 表格偏移量
        offset = 1
        # 搜索操作
        driver.find_element_by_xpath('//*[@id="txt_name"]').clear()
        driver.find_element_by_xpath('//*[@id="txt_name"]').send_keys(company)
        driver.find_element_by_xpath('//input[@value="查总股"]').click()
        driver.switch_to.window(driver.window_handles[1])
        # 这是两种情况
        try:
            # 第一种情况
            driver.find_element_by_xpath('//*[@class="chart_type"]/li[text()="十大股东"]').click()
        except:
            # 第一种情况报错就执行第二种情况
            driver.find_element_by_xpath('//*[contains(text(),"持股统计")]/../following-sibling::*[1]//li/a[text()="十大股东"]').click()
            driver.switch_to.window(driver.window_handles[2])
        try:
            # 有的公司点十大股东没反应，这里报错了，下面会捕获异常直接跳过
            driver.find_element_by_xpath('//*[@id="shareTab"]//a[text()="持股明细"]').click()
            time.sleep(2)
            driver.find_element_by_xpath('//*[@class="chart_type"]/li[text()="十大股东"]').click()
            time.sleep(1)
            try:
                driver.find_element_by_xpath('//*[contains(text(),"暂无数据")]')
                print(f'{company}，没有数据！！！')
            except:
                # 有数据获取数据
                shareholder_list = driver.find_elements_by_xpath('//*[@class="dataview-body"]//tbody//tr')
                for shareholder in shareholder_list:
                    name = shareholder.find_element_by_xpath(f'./td[{offset + 1}]/a').text
                    types = shareholder.find_element_by_xpath(f'./td[{offset + 2}]').text
                    rank = shareholder.find_element_by_xpath(f'./td[{offset + 3}]').text
                    code = shareholder.find_element_by_xpath(f'./td[{offset + 4}]/a').text
                    short_name = shareholder.find_element_by_xpath(f'./td[{offset + 5}]/a').text
                    report_time = shareholder.find_element_by_xpath(f'./td[{offset + 7}]').text
                    quantity = shareholder.find_element_by_xpath(f'./td[{offset + 8}]').text
                    outstanding_shares = shareholder.find_element_by_xpath(f'./td[{offset + 9}]').text
                    quantity_change_ratio = shareholder.find_element_by_xpath(f'./td[{offset + 10}]').text
                    quantity_change_percent = shareholder.find_element_by_xpath(f'./td[{offset + 11}]').text
                    shareholding_change = shareholder.find_element_by_xpath(f'./td[{offset + 12}]').text
                    market_value = shareholder.find_element_by_xpath(f'./td[{offset + 13}]').text
                    publish_time = shareholder.find_element_by_xpath(f'./td[{offset + 14}]').text
                    print(
                        f'{company}   {name}   {types}   {rank}   {code}   {short_name}   {report_time}   {quantity}   {outstanding_shares}   {quantity_change_ratio}   {quantity_change_percent}   {shareholding_change}   {market_value}   {publish_time}')
                    data['股东名称'].append(name)
                    data['股东类型'].append(types)
                    data['股东排名'].append(rank)
                    data['股票代码'].append(code)
                    data['股票简称'].append(short_name)
                    data['报告期'].append(report_time)
                    data['数量(股)'].append(quantity)
                    data['持股占流通股比(%)'].append(outstanding_shares)
                    data['数量变化比例(股)'].append(quantity_change_ratio)
                    data['数量变化比例(%)'].append(quantity_change_percent)
                    data['持股变动'].append(shareholding_change)
                    data['流通市值(元)'].append(market_value)
                    data['公告日'].append(publish_time)
                # 转成pandas存入csv
                df = pd.DataFrame(data)
                df.to_csv(f'开发区合伙企业股东持股明细数据.csv', encoding='utf-8-sig', index=False)
        except:
            print(f'{company}，没有数据！！！')
            pass
        # 关闭除了第一个窗口以外的窗口
        for handle in driver.window_handles:
            if handle != driver.window_handles[0]:
                driver.switch_to.window(handle)
                driver.close()
        driver.switch_to.window(driver.window_handles[0])
    print('爬取完毕')
    driver.quit()
