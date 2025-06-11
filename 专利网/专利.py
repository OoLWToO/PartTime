import time

from selenium import webdriver

data = {

}


def create_driver():
    chrome_driver_path = '../driver/chromedriver_119.exe'
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=option)
    driver.implicitly_wait(.5)
    driver.maximize_window()
    return driver


if __name__ == "__main__":
    username = '15675710186'
    password = 'As15675710186'
    # 创建driver
    driver = create_driver()
    driver.get('https://iptop.lotut.com/')
    # 登录操作
    driver.find_element_by_xpath('//a[@onclick="triggerLogin()"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//li[text()="账号密码登录"]').click()