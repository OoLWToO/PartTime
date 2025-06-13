import time

import pandas as pd
from selenium import webdriver

def create_driver():
    chrome_driver_path = '../driver/chromedriver_137.exe'
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=option)
    driver.implicitly_wait(.5)
    driver.maximize_window()
    return driver

data = {
    '名称': [],
    '申请/专利权人': [],
    '发明/设计人': [],
    '代理人': [],
    '地址': [],
    '申请日': [],
    '公开（公告）日': [],
    '公开（公告）号': [],
    '主分类号': [],
    '摘要': [],
}

if __name__ == "__main__":
    username = '18665448472'
    password = 'aABC18665448472'
    # 创建driver
    driver = create_driver()
    driver.get('https://iptop.lotut.com/')
    # 登录操作
    driver.find_element_by_xpath('//a[@onclick="triggerLogin()"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//li[text()="账号密码登录"]').click()
    driver.find_element_by_xpath('//input[@class="login-username"]').send_keys(username)
    driver.find_element_by_xpath('//*[@class="password"]').send_keys(password)
    driver.find_element_by_xpath('//*[@class="bottom-botton login-button_captcha"]').click()
    input('处理图形验证码后按下回车')
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="searchInput"]').send_keys('机械')
    driver.find_element_by_xpath('//*[@class="form-button"]').click()
    time.sleep(2)
    patent_list = driver.find_elements_by_xpath('//*[@id="right-scroll"]//li')
    for patent in patent_list:
        # 滚动到当前所在元素
        driver.execute_script("arguments[0].scrollIntoView();", patent)
        # 爬取数据
        name = patent.find_element_by_xpath('.//*[@class="d_patentName"]').text
        patentee = '/'.join([element.text for element in patent.find_elements_by_xpath('.//*[@class="apply_people_box"]//a') if element.text]).replace('', '').replace('\n', '')
        designer = '/'.join([element.get_attribute('title') for element in patent.find_elements_by_xpath('.//*[@class="hoverCopyText"]') if element.get_attribute('title')]).replace('', '').replace('\n', '')
        agent = '/'.join([element.text for element in patent.find_elements_by_xpath('.//*[@name="proxyPerson"]') if element.text]).replace('', '').replace('\n', '')
        address = patent.find_element_by_xpath('.//*[@class="getaddress"]').text
        application_date = patent.find_element_by_xpath('.//*[@name="appDate"]').text
        public_date = patent.find_element_by_xpath('.//*[@name="publishDate"]').text
        public_number = patent.find_element_by_xpath('.//*[@class="alink_default hoverCopyText"]').text
        classification = patent.find_element_by_xpath('.//*[@class="ipc hoverCopyText"]').text
        abstract = patent.find_element_by_xpath('.//*[@class="span-content"]').text
        print(f'{name}   {patentee}   {designer}   {agent}   {address}   {application_date}   {public_date}   {public_number}   {classification}   {abstract}')
        data['名称'].append(name)
        data['申请/专利权人'].append(patentee)
        data['发明/设计人'].append(designer)
        data['代理人'].append(agent)
        data['地址'].append(address)
        data['申请日'].append(application_date)
        data['公开（公告）日'].append(public_date)
        data['公开（公告）号'].append(public_number)
        data['主分类号'].append(classification)
        data['摘要'].append(abstract)
    df = pd.DataFrame(data)
    df.to_csv('“机械”专利数据.csv', encoding='utf-8-sig', index=False)
    print('爬取完成')
    driver.quit()