import re
import time

import pandas as pd
from openpyxl.utils.escape import escape

from selenium import webdriver

data = {
    '股票代码': [],
    '股票简称': [],
    '路演标题': [],
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
    # 设置链接、股票代码、股票简称、路演名称、年份
    url_list = ['https://rs.p5w.net/html/135971.shtml']
    for url in url_list:
        print(url)
        driver.get(url)
        time.sleep(2)
        ask_num = 1
        code = driver.find_element_by_xpath('//*[@class="colTop"]//i[2]').text
        company_name = driver.find_element_by_xpath('//*[@class="colTop"]//i[1]').text
        show_title = driver.find_element_by_xpath('//*[@class="colTop"]/h1').text
        year = driver.find_element_by_xpath('//*[@id="roadshowSupport"]//*[text()="举办时间"]//following-sibling::div/i').text[:4]
        try:
            driver.find_element_by_xpath('//*[@class="roadTab minTab"]//a[text()="问答"]').click()
            time.sleep(.5)
        except:
            break
        # 加载问答数据
        while True:
            ask_list = driver.find_elements_by_xpath('//*[@class="conList questBox scrollbar"][2]//*[@class="queList"]/li')
            # 滚动内嵌滚动条，如果新获取的列表长度等于原理的列表长度，证明加载完毕退出循环
            scroll_bar = driver.find_element_by_xpath('//*[@class="conList questBox scrollbar"][2]')
            driver.execute_script("arguments[0].scrollTo(0, 0);", scroll_bar)
            time.sleep(1)
            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scroll_bar)
            time.sleep(1)
            driver.execute_script("arguments[0].scrollTo(0, 0);", scroll_bar)
            time.sleep(1)
            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scroll_bar)
            time.sleep(1)
            driver.execute_script("arguments[0].scrollIntoView(true);", scroll_bar)
            if len(driver.find_elements_by_xpath('//*[@class="conList questBox scrollbar"][2]//*[@class="queList"]/li')) == len(ask_list):
                break
        for ask in ask_list:
            quest_name = ask.find_element_by_xpath('.//*[@class="quest"]//*[@class="tBar"]/i[1]').text
            quest_time = ask.find_element_by_xpath('.//*[@class="quest"]//*[@class="tBar"]/i[@class="date"]').text
            quest_content = ask.find_element_by_xpath('.//*[@class="quest"]//*[@class="content"]').text
            answer_name = ask.find_element_by_xpath('.//*[@class="answer"]//*[@class="tBar"]/i[last()]').text
            answer_time = ask.find_element_by_xpath('.//*[@class="answer"]//*[@class="tBar"]/i[@class="date"]').text
            answer_content = ask.find_element_by_xpath('.//*[@class="answer"]//*[@class="content"]').text
            print(f'{code}   {company_name}   {show_title}   {ask_num}   {year}   {quest_name}   {quest_time}   {quest_content}   {answer_name}   {answer_time}   {answer_content}')
            quest_content = escape(quest_content)
            answer_content = escape(answer_content)
            data['股票代码'].append(code)
            data['股票简称'].append(company_name)
            data['路演标题'].append(show_title)
            data['提问问题序号'].append(ask_num)
            data['会计年度'].append(year)
            data['提问人'].append(quest_name)
            data['提问时间'].append(quest_time)
            data['提问内容'].append(quest_content)
            data['回答人'].append(answer_name)
            data['回答时间'].append(answer_time)
            data['回答内容'].append(answer_content)
            ask_num += 1
        # 转成DataFrame格式存入Excel
        try:
            df = pd.DataFrame(data)
            df.to_excel(f'答复数据.xlsx', index=False)
        except:
            pass
