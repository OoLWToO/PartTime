import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains

comment_data = {
    '评论用户': [],
    '评论时间': [],
    '评论标题': [],
    '评论内容': []
}

username = '18665448472'
password = 'ABC18665448472'


def create_driver():
    chrome_driver_path = '../driver/chromedriver_137.exe'
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=option)
    driver.implicitly_wait(.5)
    driver.maximize_window()
    return driver


if __name__ == "__main__":
    # 创建driver
    driver = create_driver()
    driver.get('https://user.qunar.com/passport/login.jsp')
    time.sleep(2)
    driver.find_element_by_xpath('//*[@class="passwordTab"]').click()
    driver.find_element_by_xpath('//*[@id="username"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="agreement"]').click()
    driver.find_element_by_xpath('//span[text()="登录"]').click()
    # 处理滑块验证码
    slider_belt = driver.find_element_by_xpath('//*[@class="NrgjHeg7YBdiFd3U9T_j_"]')
    slider_bar = driver.find_element_by_xpath('//*[@class="OQphwVk_QrhLuedI5-Jme"]')
    slider_distance = slider_belt.size['width'] - slider_bar.size['width'] + 10
    ActionChains(driver).click_and_hold(slider_bar).move_by_offset(slider_distance, 0).release().perform()
    time.sleep(2)
    # 获取上海迪士尼的评论
    driver.get('https://travel.qunar.com/p-oi7564992-shanghaidishinidujiaqu')
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="detail-nav"]//a[text()="驴友点评"]').click()
    comment_list = driver.find_elements_by_xpath('//*[@id="comment_box"]/li')
    for comment in comment_list:
        user = comment.find_element_by_xpath('.//*[@class="e_comment_usr_name"]/a').text
        title = comment.find_element_by_xpath('.//*[@class="e_comment_title"]/a').text
        date = comment.find_element_by_xpath('.//*[@class="e_comment_add_info"]//li[1]').text
        content = comment.find_element_by_xpath('.//*[@class="e_comment_content"]').text.replace('\n', '')
        print(f'{user}   {title}   {date}   {content}')
        comment_data['评论用户'].append(user)
        comment_data['评论标题'].append(title)
        comment_data['评论时间'].append(date)
        comment_data['评论内容'].append(content)
    df = pd.DataFrame(comment_data)
    df.to_excel('上海迪士尼评论数据.xlsx', index=False)
    print('爬取完成')
    driver.quit()
