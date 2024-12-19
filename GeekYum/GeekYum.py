import time
from functools import partial

import schedule
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import element_driver as e


# 全局配置文件
username = '18665448472'
password = 'ABC18665448472'
climb_time = ['07:00', '10:00', '14:00']
search_port = [['上海', '德国汉堡'],
               ['上海', '荷兰鹿特丹'],
               ['天津', '美西洛杉矶'],
               ['天津', '美东休斯顿']]


def create_driver():
    chrome_driver_path = "../../rpa/driver/chromedriver_119.exe"
    options = Options()
    options.add_argument("--start-maximized")
    chrome_driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
    chrome_driver.implicitly_wait(5)
    chrome_driver.get("https://www.geekyum.com/business")
    return chrome_driver


def search_mission(driver):
    e.input_by_xpath(driver, '//*[@placeholder="起运港"]', )
    e.wait_ele_visibility_by_xpath(driver, '//*[@class="el-scrollbar"]//*[@class="select-custom-content"]').click()
    e.input_by_xpath(driver, '//*[@placeholder="目的港"]', )
    print('执行了定时任务！！！')


def set_mission_time(driver):
    for c_time in climb_time:
        schedule.every().day.at(c_time).do(partial(search_mission, driver=driver))


if __name__ == "__main__":
    driver = create_driver()
    set_mission_time(driver)
    e.find_ele_and_click(driver, '//*[@class="login"]')
    e.find_ele_and_click(driver, '//*[contains(@class,"icon-mimasuo")]')
    e.input_by_xpath(driver, '//*[@name="username"]', username)
    e.input_by_xpath(driver, '//*[@name="password"]', password)
    e.find_ele_and_click(driver, '//span[text()="登录"]')
    e.find_ele_and_click(driver, '//span[text()="Geek Rate"]')
    while True:
        # schedule.run_pending()
        search_mission(driver)
        time.sleep(1)
