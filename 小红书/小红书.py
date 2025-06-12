import time

from selenium import webdriver

data = {

}


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
    driver.get('https://www.xiaohongshu.com/explore')
    time.sleep(2)
    # 登录账号
    driver.find_element_by_xpath('//*[@placeholder="输入手机号"]').send_keys('18665448472')
    driver.find_element_by_xpath('//*[@class="icon-wrapper"]').click()
    driver.find_element_by_xpath('//*[text()="获取验证码"]').click()
    input('手动输入验证码登录一下账号')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@placeholder="搜索小红书"]').send_keys('寺庙文创')
    driver.find_element_by_xpath('//*[@class="search-icon"]').click()
    time.sleep(2)
    while True:
        article_list = driver.find_elements_by_xpath('//*[@class="feeds-container"]/section')
        for article in article_list:
            article.click()
            detail_ele = driver.find_element_by_xpath('//*[@class="interaction-container"]')
            title = detail_ele.find_element_by_xpath('.//*[@class="title"]').text
