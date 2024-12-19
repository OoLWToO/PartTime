from datetime import datetime

import pandas as pd
from openpyxl import Workbook

from selenium import webdriver

data = {
    '园区名称': [],
    '省份': [],
    '城市': [],
    '地区': [],
    '详细地址': [],
    '大约面积(亩)': [],
    '企业数': [],
}


def create_driver():
    chrome_driver_path = '../driver/chromedriver_119.exe'
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=option)
    driver.implicitly_wait(.5)
    driver.maximize_window()
    driver.get('https://f.qianzhan.com/')
    return driver


if __name__ == "__main__":
    # 创建driver
    driver = create_driver()
    driver.get('https://f.qianzhan.com/yuanqu/diqu/36/?pg=1')
    city_list = driver.find_elements_by_xpath('//*[@class="f-cb"][1]/div/a[span]')
    for i in range(len(city_list)):
        city = driver.find_element_by_xpath(f'//*[@class="f-cb"][1]/div/a[span][{i + 1}]')
        if city.text[city.text.find('(') + 1:city.text.find(')')] == '1':
            continue
        city.click()
        towns_list = driver.find_elements_by_xpath('//*[@class="f-cb"][2]/div/a[span]')
        for j in range(len(towns_list)):
            towns = driver.find_element_by_xpath(f'//*[@class="f-cb"][2]/div/a[span][{j + 1}]')
            if towns.text[towns.text.find('(') + 1:towns.text.find(')')] == '1':
                continue
            towns.click()
            try:
                page_size = len(driver.find_elements_by_xpath('//*[@id="divpager"]/a')) - 2
            except:
                page_size = 1
            for page in range(page_size):
                park_list = driver.find_elements_by_xpath('//*[@class="company-table"]/tbody/tr')
                for park in park_list:
                    park_name = park.find_element_by_xpath('./td[2]/a').text
                    province = park.find_element_by_xpath('./td[3]').text
                    city = park.find_element_by_xpath('./td[4]').text
                    district = park.find_element_by_xpath('./td[5]').text
                    address = park.find_element_by_xpath('./td[6]').text
                    area = park.find_element_by_xpath('./td[7]').text
                    company_num = park.find_element_by_xpath('./td[8]').text
                    print(f'{park_name}   {province}   {city}   {district}   {address}   {area}   {company_num}')
                    data['园区名称'].append(park_name)
                    data['省份'].append(province)
                    data['城市'].append(city)
                    data['地区'].append(district)
                    data['详细地址'].append(address)
                    data['大约面积(亩)'].append(area)
                    data['企业数'].append(company_num)
                if page != page_size - 1:
                    driver.find_element_by_xpath('//*[@id="divpager"]/a[text()="下一页"]').click()
            df = pd.DataFrame(data)
            df.to_csv('江西产业园数据.csv', encoding='utf-8-sig', index=False)
    print('爬取完毕')
    driver.quit()