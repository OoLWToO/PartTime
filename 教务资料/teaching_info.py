import os

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
    # 创建driver
    driver = create_driver()
    driver.get('https://jiaowu.ijidi.cn/')
    main_eles = driver.find_elements_by_xpath('//*[@class="container"]//li[@class="menu-item menu-item-has-children"]')
    for main_ele in main_eles:
        main_item = main_ele.text
        sub_item = main_ele.find_elements_by_xpath('./ul/li/a')[0].get_attribute('text')
        sub_item_url = main_ele.find_elements_by_xpath('./ul/li/a')[0].get_attribute('href')
        if not os.path.exists(main_item):
            os.makedirs(main_item)
    print()
