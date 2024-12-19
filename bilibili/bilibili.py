import re
import time

import pandas as pd
from matplotlib import pyplot as plt
from openpyxl import Workbook

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wordcloud import WordCloud

data = {
    '用户名': [],
    '等级': [],
    '评论内容': [],
    '时间': [],
    '点赞数': [],
}


def create_driver():
    chrome_driver_path = '../driver/chromedriver_119.exe'
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=option)
    driver.implicitly_wait(5)
    driver.maximize_window()
    return driver


def login(driver):
    username = '18665448472'
    password = 'ABC18665448472'
    driver.find_element_by_xpath('//*[@class="header-login-entry"]').click()
    driver.find_element_by_xpath('//*[@placeholder="请输入账号"]').send_keys(username)
    driver.find_element_by_xpath('//*[@placeholder="请输入密码"]').send_keys(password)
    driver.find_element_by_xpath('//*[@class="btn_primary "]').click()
    input('处理验证码，处理完成后在控制台按下回车键！')


if __name__ == "__main__":
    driver = create_driver()
    driver.get(
        'https://m.bilibili.com/video/BV1gi421v7hK?buvid=ZA409CA936A143974123A07F7D02B06672BD&is_story_h5=false&mid=Z42Dw56LTeGiKKOpMIeLCQ%3D%3D&p=1&plat_id=114&share_from=ugc&share_medium=ipad&share_plat=ios&')
    login(driver)
    try:
        driver.find_element_by_xpath('//*[@class="time-sort"]').click()
    except:
        input('B站加载方式变了，关闭程序重跑一次')
    while True:
        comment_list = driver.find_elements_by_xpath('//*[@class="reply-item"]')
        print(f'评论数量：{len(comment_list)}')
        if len(comment_list) >= 200:
            break
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print('等待数据加载')
        time.sleep(1)
    driver.implicitly_wait(0)
    for comment in comment_list:
        name = comment.find_element_by_xpath('.//*[@class="user-name"]').text
        try:
            level = re.search(r'\d+', comment.find_element_by_xpath('.//*[@class="user-info"]//*[contains(@class,"user-level")]').get_attribute('class')).group()
        except:
            level = '6'
        content = comment.find_element_by_xpath('.//*[@class="root-reply"]//*[@class="reply-content"]').text
        time = comment.find_element_by_xpath('.//*[@class="root-reply"]//*[@class="reply-time"]').text
        try:
            like = comment.find_element_by_xpath('.//*[@class="root-reply"]//*[@class="reply-like"]/span').text
        except:
            like = 0
        print(f'{name}   {level}   {content}   {time}   {like}')
        data['用户名'].append(name)
        data['等级'].append(level)
        data['评论内容'].append(content)
        data['时间'].append(time)
        data['点赞数'].append(like)
    df = pd.DataFrame(data)
    df.to_csv('bilibili评论数据.csv', encoding='utf-8-sig', index=False)
    driver.quit()
