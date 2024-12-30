import time

import requests
from datetime import datetime
from selenium import webdriver

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

data = {
    "data": {
        "page": 2,
        "page_size": 10,
        "sort": "collected",
        "keyword": "",
        "task_from": "httg",
        "htsid": "9fab78f763d2738a1464f89b0236b74c"
    },
    "timestamp": "2024-12-30 10:47:07",
    "sign": "FB1655EA47D0BBDA769D68E2718ED13E"
}


def create_driver():
    chrome_driver_path = '../driver/chromedriver_119.exe'
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=option)
    driver.implicitly_wait(.5)
    driver.maximize_window()
    return driver


def get_current_cookie():
    # 获取当前页面Cookie
    cookies_list = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    cookie = ';'.join(item for item in cookies_list)
    return cookie


if __name__ == '__main__':
    driver = create_driver()
    url = 'https://tonggao.huitun.com/#/xhs/square'
    driver.get(url)
    scrollable_element = driver.find_element_by_xpath('//*[@class="global-content ant-layout-content"]')
    last_height = driver.execute_script("return arguments[0].scrollHeight;", scrollable_element)
    while True:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_element)
        time.sleep(5)
        new_height = driver.execute_script("return arguments[0].scrollHeight;", scrollable_element)
        if new_height == last_height:
            break
        last_height = new_height
    print()