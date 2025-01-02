import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_driver():
    chrome_driver_path = '../driver/chromedriver_131.exe'
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=option)
    driver.implicitly_wait(.5)
    driver.maximize_window()
    return driver

data = {
    '红书号': []
}

page = 3


if __name__ == '__main__':
    driver = create_driver()
    url = 'https://tonggao.huitun.com/#/xhs/square'
    driver.get(url)
    scrollable_element = driver.find_element_by_xpath('//*[@class="global-content ant-layout-content"]')
    input('等待登录后，按下回车！！！')
    for _ in range(page):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_element)
        while True:
            try:
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[contains(text(),"拼命加载中")]')))
            except:
                break
    user_list = driver.find_elements_by_xpath('//*[@class="model-list-wrapper"]/div')
    for user in user_list:
        driver.execute_script("arguments[0].scrollIntoView();", user)
        try:
            user_header = user.find_element_by_xpath('.//*[@class="avatar-wrapper"]')
        except:
            continue
        user_header.click()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[-1])
        red_num = driver.find_element_by_xpath('//*[@class="red_id"]').text.replace('红书号:', '')
        print(f'{red_num}')
        data['红书号'].append(red_num)
        # 关闭除了第一个窗口以外的窗口
        for handle in driver.window_handles:
            if handle != driver.window_handles[0]:
                driver.switch_to.window(handle)
                driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
        df = pd.DataFrame(data)
        df.to_excel('小红书账号.xlsx', index=False)

