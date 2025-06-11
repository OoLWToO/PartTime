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

username = 'admin_1077@xiaoman.okki_pro'
password = 'qkd5rw'


if __name__ == "__main__":
    # 创建driver
    driver = create_driver()
    driver.get('https://crm.xiaoman.cn/')
    print()
