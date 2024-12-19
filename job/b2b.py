from openpyxl import Workbook

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 创建driver
def create_driver():
    chrome_driver_path = '../driver/chromedriver_119.exe'
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=option)
    # 设置元素的查找时间，0.5秒没找到报错，可以调高点
    driver.implicitly_wait(.5)
    driver.maximize_window()
    return driver


def scroll_to_bottom(driver):
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            if WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="page-content"]'))):
                break
        except:
            pass


if __name__ == "__main__":
    driver = create_driver()
    # 初始化excel
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.column_dimensions['A'].width = 30
    worksheet.cell(row=1, column=1, value='职位名称')
    rows = 2
    driver.get(f'https://b2b.baidu.com/aitf/s?q=%E8%94%AC%E8%8F%9C&amp;from=search&amp;fid=487853820%2C1718246794786&amp;pi=b2b.s.search...9259451009465282')
    scroll_to_bottom(driver)
    pages = len(driver.find_elements_by_xpath('//*[@class="page-content"]/ul/li[@class="ivu-page-item"]'))
    for _ in range(pages):
        data_list = driver.find_elements_by_xpath('//*[@class="card-layout is-wide is-horizontal"]')
        for data in data_list:
            name = data.find_element_by_xpath('.//*[@class="p-card-name"]/span').get_attribute('title')
            price = data.find_element_by_xpath('.//*[@class="p-card-price"]').get_attribute('title')
            unit = data.find_element_by_xpath('.//*[@class="unit"]').text
            company = data.find_element_by_xpath('.//*[contains(@class,"shopname")]/span/span').get_attribute('title')
            setup_time = data.find_element_by_xpath('.//*[@class="qi-duration"]').text
            address = data.find_element_by_xpath('.//*[@class="p-card-bottom-address"]').text
    print('爬取完毕')
