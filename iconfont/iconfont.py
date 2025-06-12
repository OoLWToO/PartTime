import time

from selenium import webdriver
from selenium.webdriver import ActionChains

username = '18665448472'
password = 'ABC1419710910'


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
    driver.get('https://www.iconfont.cn/')
    time.sleep(2)
    driver.find_element_by_xpath('//*[@href="/login"]').click()
    driver.find_element_by_xpath('//*[@autocomplete="username"]').send_keys(username)
    driver.find_element_by_xpath('//*[@autocomplete="current-password"]').send_keys(password)
    driver.find_element_by_xpath('//button[text()="登录"]').click()
    time.sleep(2)
    # 点击一下使input框出现
    driver.find_element_by_xpath('//*[@class="search-input-cover"]').click()
    driver.find_element_by_xpath('//*[@class="search-input show"]').send_keys('管理')
    driver.find_element_by_xpath('//*[@class="iconfont icon-sousuo"]').click()
    time.sleep(3)
    # 下载前10个
    icon_list = driver.find_elements_by_xpath('//*[@class="page-search-container"]//li')
    for icon in icon_list[:10]:
        print(f'将第{icon_list.index(icon) + 1}个图标添加到购物车')
        ActionChains(driver).move_to_element(icon).perform()
        icon.find_element_by_xpath('.//*[@title="添加入库"]').click()
        time.sleep(.5)
    driver.find_element_by_xpath('//*[@class="icon-car"]').click()
    time.sleep(.5)
    driver.find_element_by_xpath('//span[text()="下载素材"]').click()
    driver.find_element_by_xpath('//span[text()="PNG"]').click()
    print('下载完成')
