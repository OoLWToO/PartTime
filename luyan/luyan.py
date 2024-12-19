import re
import time

import pandas as pd
from openpyxl.utils.escape import escape

from selenium import webdriver

# 问答数据数量
data = {
    '股票代码': [],
    '股票简称': [],
    '提问问题序号': [],
    '会计年度': [],
    '提问人': [],
    '提问时间': [],
    '提问内容': [],
    '回答人': [],
    '回答时间': [],
    '回答内容': [],
}


def create_driver():
    # 路径设为自己的chromedriver路径
    chrome_driver_path = '../driver/chromedriver_119.exe'
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=option)
    driver.implicitly_wait(2)
    driver.maximize_window()
    return driver


if __name__ == "__main__":
    driver = create_driver()
    driver.get('https://rs.p5w.net/roadshow?roadshowType=4')
    # 先获取所有股票代码
    driver.find_element_by_xpath('//span[contains(text(),"上市仪式")]').click()
    code_list = []
    while True:
        code_ele = driver.find_elements_by_xpath('//*[@class="roadList cf"]//div[@class="top t-ovh"]//i')
        for code in code_ele:
            try:
                code_list.append(re.findall(r'\d+', code.text)[0])
            except:
                pass
        if len(code_list) >= 20:
            break
        try:
            # 点击当前页数的下一页，如果无法点击证明到结尾了，会报错然后退出循环
            driver.find_element_by_xpath('//*[@id="pagination"]//li[@class="active"]/following-sibling::li[1]').click()
        except:
            break
        time.sleep(1)
    for code in code_list:
        ask_num = 1
        # 爬取最新提问
        driver.get(f'https://ir.p5w.net/c/{code}/questionlist.shtml?query=1')
        time.sleep(.5)
        while True:
            company_name = driver.find_element_by_xpath('//p[contains(text(),"公司简称")]/span').text
            ask_list = driver.find_elements_by_xpath(
                '//*[@class="conList" and not(contains(@style, "display: none;"))]/ul//li')
            if 'noData' in ask_list[0].get_attribute('class'):
                break
            for ask in ask_list:
                ask_name = ask.find_element_by_xpath('.//span[@class="person superStar" or @class="person"]').text
                ask_time = ask.find_element_by_xpath('.//p[@class="date"]').text
                ask_content = ask.find_element_by_xpath('.//a[@class="dib f14"]').text
                year = ask_time[:4]
                print(f'{code}   {company_name}   {ask_num}   {year}   {ask_name}   {ask_time}   {ask_content}')
                ask_content = escape(ask_content)
                data['股票代码'].append(code)
                data['股票简称'].append(company_name)
                data['提问问题序号'].append(ask_num)
                data['会计年度'].append(year)
                data['提问人'].append(ask_name)
                data['提问时间'].append(ask_time)
                data['提问内容'].append(ask_content)
                data['回答人'].append('')
                data['回答时间'].append('')
                data['回答内容'].append('')
                ask_num += 1
            try:
                driver.find_element_by_xpath(
                    '//*[@id="replyPagination"]//li[@class="active"]/following-sibling::li[1]').click()
                time.sleep(.5)
            except:
                break
        # 转成DataFrame格式存入Excel
        try:
            df = pd.DataFrame(data)
            df.to_excel(f'答复数据.xlsx', index=False)
        except:
            pass
        # 爬取最新回复
        driver.get(f'https://ir.p5w.net/c/{code}/questionlist.shtml?query=0')
        time.sleep(.5)
        while True:
            ask_list = driver.find_elements_by_xpath(
                '//*[@class="conList" and not(contains(@style, "display: none;"))]/ul//li')
            if 'noData' in ask_list[0].get_attribute('class'):
                break
            for ask in ask_list:
                ask_name = ask.find_element_by_xpath(
                    './div[1]//span[@class="person superStar" or @class="person"]').text
                ask_time = ask.find_element_by_xpath('./div[1]//p[@class="date"]').text
                ask_content = ask.find_element_by_xpath('./div[1]//a[@class="dib f14"]').text
                year = ask_time[:4]
                reply_name = ask.find_element_by_xpath('./div[2]//a[@class="person"]').text
                reply_time = ask.find_element_by_xpath('./div[2]//p[@class="date"]').text
                reply_content = ask.find_element_by_xpath('./div[2]//a[@class="dib f14"]').text
                print(
                    f'{code}   {company_name}   {ask_num}   {year}   {ask_name}   {ask_time}   {ask_content}   {reply_name}   {reply_time}   {reply_content}')
                ask_content = escape(ask_content)
                reply_content = escape(reply_content)
                data['股票代码'].append(code)
                data['股票简称'].append(company_name)
                data['会计年度'].append(year)
                data['提问人'].append(ask_name)
                data['提问时间'].append(ask_time)
                data['提问内容'].append(ask_content)
                data['回答人'].append(reply_name)
                data['回答时间'].append(reply_time)
                data['回答内容'].append(reply_content)
                data['提问问题序号'].append(ask_num)
                ask_num += 1
            try:
                driver.find_element_by_xpath(
                    '//*[@id="replyPagination"]//li[@class="active"]/following-sibling::li[1]').click()
                time.sleep(.5)
            except:
                break
        try:
            df = pd.DataFrame(data)
            df.to_excel(f'答复数据.xlsx', index=False)
        except:
            pass
