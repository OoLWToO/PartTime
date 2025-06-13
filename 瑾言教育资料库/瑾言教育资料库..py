from selenium import webdriver

data = {

}


def create_driver():
    chrome_driver_path = '../driver/chromedriver_135.exe'
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=option)
    driver.implicitly_wait(.5)
    driver.maximize_window()
    return driver


if __name__ == "__main__":
    # 创建driver
    driver = create_driver()
    driver.get('https://appt0hp9gsj7446.xet.citv.cn/p/decorate/homepage')
    print()
