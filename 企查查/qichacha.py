import time

from selenium import webdriver

data = {

}


def create_driver():
    chrome_driver_path = '../driver/chromedriver_131.exe'
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=option)
    driver.implicitly_wait(.5)
    driver.maximize_window()
    return driver

key_words = ['智慧农业', '农业大数据', '植保无人机', '生态农业', '循环农业', '农产品电商', '休闲农业']


if __name__ == "__main__":
    # 创建driver
    driver = create_driver()
    driver.get('https://www.qcc.com/')
    print()
    driver.find_element_by_xpath('//*[contains(@class,"modal-close")]').click()
    for key_word in key_words:
        for year in range(2010, 2024):
            driver.get(f'https://www.qcc.com/web/search?key={key_word}&filter=%7B%22d%22%3A%5B%7B%22value%22%3A%22{str(year)}1231-{str(year)}0101%22,%22x%22%3Atrue%7D%5D%7D')
            time.sleep(3)