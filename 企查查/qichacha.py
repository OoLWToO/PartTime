import re
import time

import pandas as pd
from selenium import webdriver

data = {
    '企业名称': [],
    '省': [],
    '市': [],
    '区': [],
    '注册地址': [],
    '注册资本': [],
    '成立时间': [],
}

username = '18665448472'
password = 'ABC18665448472'
key_words = ['智慧农业', '农业大数据', '植保无人机', '生态农业', '循环农业', '农产品电商', '休闲农业']


def create_driver():
    chrome_driver_path = '../driver/chromedriver_131.exe'
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=option)
    driver.implicitly_wait(.5)
    driver.maximize_window()
    return driver


if __name__ == "__main__":
    # 创建driver
    driver = create_driver()
    driver.get('https://www.qcc.com/')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@class="qcc-login-type-change"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//a[text()="密码登录"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[contains(@placeholder,"手机号码/用户名")]').send_keys(username)
    driver.find_element_by_xpath('//*[contains(@placeholder,"密码")]').send_keys(password)
    print()
    for key_word in key_words:
        for year in range(2010, 2024):
            driver.get(f'https://www.qcc.com/web/search?key={key_word}&p=1&filter=%7B%22d%22%3A%5B%7B%22value%22%3A%22{str(year)}1231-{str(year)}0101%22,%22x%22%3Atrue%7D%5D%7D')
            time.sleep(2)
            result_num = int(driver.find_element_by_xpath('//*[@class="left-panel"]//*[@class="text-danger"]').text.replace(',', ''))
            # for page in range(result_num//20+1):
            for page in range(2):
                driver.get(f'https://www.qcc.com/web/search?key={key_word}&p={page+1}&filter=%7B%22d%22%3A%5B%7B%22value%22%3A%22{str(year)}1231-{str(year)}0101%22,%22x%22%3Atrue%7D%5D%7D')
                company_list = driver.find_elements_by_xpath('//*[@class="search-cell"]//tr[@class]')
                for company in company_list:
                    name = company.find_element_by_xpath('.//*[@class="copy-title"]/a/span').text
                    register_address = company.find_element_by_xpath('.//*[@class="f" and contains(text(),"地址")]/span').text
                    try:
                        register_capital = company.find_element_by_xpath('.//*[@class="f" and contains(text(),"注册资本")]/span').text
                    except:
                        register_capital = ''
                    found_time = company.find_element_by_xpath('.//*[@class="f" and contains(text(),"成立日期")]/span').text
                    match = re.match(r'(?P<province>[^省]+省)?(?P<city>[^市]+市)?(?P<district>[^区]+区)?', register_address)
                    if match:
                        province = match.group('province')
                        city = match.group('city')
                        district = match.group('district')
                    else:
                        province = ''
                        city = ''
                        district = ''
                    print(f'{name}   {province}   {city}   {district}   {register_address}   {register_capital}   {found_time}')
                    data['企业名称'].append(name)
                    data['省'].append(province)
                    data['市'].append(city)
                    data['区'].append(district)
                    data['注册地址'].append(register_address)
                    data['注册资本'].append(register_capital)
                    data['成立时间'].append(found_time)
        df = pd.DataFrame(data)
        df.to_excel(f'《{key_word}》关键字企查查数据.xlsx', index=False)