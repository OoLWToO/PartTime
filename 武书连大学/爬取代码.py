import json
import time

import pandas as pd
import requests

from selenium import webdriver

data = {
    '综合实力': [],
    '学校名称': [],
    '英文名': [],
    '综合实力等级': [],
    '省份': [],
    '学校类型': [],
    '学校参考类型': [],
    '985': [],
    '211': [],
    '双一流': [],
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
    driver.get('https://www.wurank.net/university-ranking')
    driver.find_element_by_xpath('//*[@class="show pg-select"]').click()
    driver.find_element_by_xpath('//*[text()="50条/页"]').click()
    time.sleep(3)
    for _ in range(17):
        universities = driver.find_elements_by_xpath('//*[@class="mc-table"]/div')
        for universitiy in universities:
            # 第一、第二、第三名为图片
            strength_rank = universitiy.find_element_by_xpath('./div[1]/div').text
            if not strength_rank:
                strength_rank = universitiy.find_element_by_xpath('./div[1]/div/img').get_attribute('src')[-5:-4]
            name = universitiy.find_element_by_xpath('.//*[@class="mc-name s18"]').text
            e_name = universitiy.find_element_by_xpath('.//*[@class="mc-name s18"]').text
            strength_level = universitiy.find_element_by_xpath('./div[3]/div').text
            province = universitiy.find_element_by_xpath('./div[4]/div').text
            universitiy_type = universitiy.find_element_by_xpath('./div[5]/div').text
            universitiy_reference_type = universitiy.find_element_by_xpath('./div[6]/div').text
            introduce = universitiy.find_element_by_xpath('.//*[@class="mc-des s14"]').text
            is_985 = '是' if '985' in introduce else '否'
            is_211 = '是' if '211' in introduce else '否'
            is_double = '是' if '双一流' in introduce else '否'
            print(f'{strength_rank}   {name}   {e_name}   {strength_level}   {province}   {universitiy_type}   {universitiy_reference_type}   {is_985}   {is_211}   {is_double}')
            # 存入data
            data['综合实力'].append(strength_rank)
            data['学校名称'].append(name)
            data['英文名'].append(e_name)
            data['综合实力等级'].append(strength_level)
            data['省份'].append(province)
            data['学校类型'].append(universitiy_type)
            data['学校参考类型'].append(universitiy_reference_type)
            data['985'].append(is_985)
            data['211'].append(is_211)
            data['双一流'].append(is_double)
        driver.find_element_by_xpath('//*[@class="pg-next s16"]').click()
        time.sleep(2)
        df = pd.DataFrame(data)
        df.to_csv('武书连大学数据.csv', encoding='utf-8-sig', index=False)
    print('爬取完毕')
    driver.quit()
