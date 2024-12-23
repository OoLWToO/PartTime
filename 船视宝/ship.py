import time

import pandas as pd
from selenium import webdriver
from datetime import datetime

data = {
    '船舶英文名称': [],
    'MMSI': [],
    'IMO': [],
    '载重吨': [],
    'TEU': [],
    '设计吃水(m)': [],
    '建造年月': [],
    '目的港': [],
    '船舶动态': [],
    '预抵/动态时间': [],
    '到港时间': [],
    '空/满': [],
    '启运港挂靠次数(近1年)': [],
    '目的港挂靠次数(近1年)': [],
    '对地航速(kn)': [],
    '当前吃水(m)': [],
    'AIS航行状态': [],
}

# 配置信息
grouped_list = ['装']  # 分组列表
phone = '17615291380'  # 手机号码


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
    driver.get('https://www.myvessel.cn/auth/login')
    driver.find_element_by_xpath('//*[@class="anticon"]').click()
    driver.find_element_by_xpath('//*[@placeholder="手机号"]').send_keys(phone)
    driver.find_element_by_xpath('//*[@class="sm-ico"]').click()
    driver.find_element_by_xpath('//a[text()="获取验证码"]').click()
    while (True):
        print('等待输入验证码...')
        time.sleep(2)
        if 'position' in driver.current_url:
            break
    # 等待3s后刷新，页面弹窗消失
    time.sleep(3)
    driver.refresh()
    print('登录成功！！！')
    time.sleep(3)
    # 点击'船队功能', 循环分组列表选择分组
    driver.find_element_by_xpath('//button[contains(text(),"船队功能")]').click()
    time.sleep(2)
    for grouped in grouped_list:
        driver.find_element_by_xpath(f'//*[@class="my-fleet-box"]/button[./span[text()="{grouped}"]]').click()
        time.sleep(.5)
    driver.find_element_by_xpath('//*[contains(@class,"category-item") and ./p[contains(text(),"列表")]]').click()
    # 切换到新打开的窗口，即最后一个窗口
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    # 选择'列表设置'
    driver.find_element_by_xpath('//button[./span[text()="列表设置"]]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[name()="svg" and @title="全选"]').click()
    time.sleep(1)
    for key, value in data.items():
        driver.find_element_by_xpath(f'//*[@class="n-checkbox__label" and text()="{key}"]').click()
    driver.find_element_by_xpath('//*[@class="n-button__content" and text()="确定"]').click()
    time.sleep(5)
    page_num = int(driver.find_element_by_xpath('(//*[@rel="nofollow"])[last()]').text)
    ship_list = driver.find_elements_by_xpath('//*[@class="ant-table-body"]//tr[contains(@class,"table-row")]')
    for page in range(page_num-1):
        for ship in ship_list:
            en_name = ship.find_element_by_xpath('./td[2]').text
            MMSI = ship.find_element_by_xpath('./td[3]').text
            IMO = ship.find_element_by_xpath('./td[4]').text
            DWT = ship.find_element_by_xpath('./td[5]').text
            TEU = ship.find_element_by_xpath('./td[6]').text
            design_draft = ship.find_element_by_xpath('./td[7]').text
            build_time = ship.find_element_by_xpath('./td[8]').text
            end_port = ship.find_element_by_xpath('./td[9]').text
            ship_dynamics = ship.find_element_by_xpath('./td[10]').text
            expected_arrival_time = ship.find_element_by_xpath('./td[11]').text
            arrival_time = ship.find_element_by_xpath('./td[12]').text
            empty_or_full = ship.find_element_by_xpath('./td[13]').text
            start_port_anchored_num = ship.find_element_by_xpath('./td[14]').text
            end_port_anchored_num = ship.find_element_by_xpath('./td[15]').text
            ground_speed = ship.find_element_by_xpath('./td[16]').text
            current_draft = ship.find_element_by_xpath('./td[17]').text
            AIS_state = ship.find_element_by_xpath('./td[18]').text
            print(f'{en_name}   {MMSI}   {IMO}   {DWT}   {TEU}   {design_draft}   {build_time}   {end_port}   '
                  f'{ship_dynamics}   {expected_arrival_time}   {arrival_time}   {empty_or_full}   {start_port_anchored_num}   '
                  f'{end_port_anchored_num}   {ground_speed}   {current_draft}   {AIS_state}')
            data['船舶英文名称'].append(en_name)
            data['MMSI'].append(MMSI)
            data['IMO'].append(IMO)
            data['载重吨'].append(DWT)
            data['TEU'].append(TEU)
            data['设计吃水(m)'].append(design_draft)
            data['建造年月'].append(build_time)
            data['目的港'].append(end_port)
            data['船舶动态'].append(ship_dynamics)
            data['预抵/动态时间'].append(expected_arrival_time)
            data['到港时间'].append(arrival_time)
            data['空/满'].append(empty_or_full)
            data['启运港挂靠次数(近1年)'].append(start_port_anchored_num)
            data['目的港挂靠次数(近1年)'].append(end_port_anchored_num)
            data['对地航速(kn)'].append(ground_speed)
            data['当前吃水(m)'].append(current_draft)
            data['AIS航行状态'].append(AIS_state)
        driver.find_element_by_xpath('//li[@title="下一页"]').click()
        time.sleep(2)
    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日")
    df = pd.DataFrame(data)
    df.to_excel(f'{date_str}_船舶信息.xlsx', index=False)
