import time

import pandas as pd
from selenium import webdriver

# 股票基础数据
stock_data = {
    'stock_name': [],
    'stock_code': [],
}

# 股东数据
shareholder_data = {
    'stock_code': [],
    'stockholder_name': [],
    'stockholder_amount': [],
    'stockholder_ratio': [],
}

# 基金持股数据
fund_shareholding_data = {
    'stock_code': [],
    'fund_name': [],
    'fund_amount': [],
    'fund_ratio': [],
}

# 公司数据
company_data = {
    'stock_code': [],
    'company_name': [],
    'business_scope': [],
    'province': [],
    'actual_controller': [],
}

# 公司高管数据
company_executive_data = {
    'company_name': [],
    'manager_name': [],
    'manager_position': [],
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
    driver = create_driver()
    driver.get('https://xueqiu.com/hq/detail?market=CN&first_name=0&second_name=0&type=sh_sz')
    print('正在爬取股票基础数据......')
    for page in range(2):
        time.sleep(1)
        stock_list = driver.find_elements_by_xpath('(//*[@class="index_table-wrapper_9HK"]//tbody)[1]/tr')
        for stock in stock_list:
            stock_code = stock.find_element_by_xpath('./td[1]').text
            stock_name = stock.find_element_by_xpath('./td[2]').text
            stock_data['stock_code'].append(stock_code)
            stock_data['stock_name'].append(stock_name)
            print(f'{stock_code}   {stock_name}')
        driver.find_element_by_xpath('//button[text()="下一页"]').click()
        time.sleep(1)
    df = pd.DataFrame(stock_data)
    df.to_csv('股票基础数据.csv', encoding='utf-8-sig', index=False)

    print('-------------------------------------------------------------------------------------------------')

    # print('正在爬取股东数据......')
    # for stock_code in stock_data['stock_code']:
    #     driver.get(f'https://xueqiu.com/snowman/S/{stock_code}/detail#/LTGD')
    #     stockholder_list = driver.find_elements_by_xpath('//*[@class="brief-info holder-table"][1]//tbody/tr')
    #     for stockholder in stockholder_list:
    #         stockholder_name = stockholder.find_element_by_xpath('./td[1]').text
    #         stockholder_amount = stockholder.find_element_by_xpath('./td[2]').text
    #         stockholder_ratio = stockholder.find_element_by_xpath('./td[3]').text
    #         shareholder_data['stock_code'].append(stock_code)
    #         shareholder_data['stockholder_name'].append(stockholder_name)
    #         shareholder_data['stockholder_amount'].append(stockholder_amount)
    #         shareholder_data['stockholder_ratio'].append(stockholder_ratio)
    #         print(f'{stock_code}   {stockholder_name}   {stockholder_amount}   {stockholder_ratio}')
    # df = pd.DataFrame(shareholder_data)
    # df.to_csv('股东数据.csv', encoding='utf-8-sig', index=False)
    #
    # print('-------------------------------------------------------------------------------------------------')
    #
    # print('正在爬取基金持股数据......')
    # for stock_code in stock_data['stock_code']:
    #     driver.get(f'https://xueqiu.com/snowman/S/{stock_code}/detail#/JJCG')
    #     try:
    #         jijin_list = driver.find_elements_by_xpath('//*[@class="brief-info"]/tbody/tr')
    #     except:
    #         continue
    #     for jijin in jijin_list:
    #         fund_name = jijin.find_element_by_xpath('./td[1]').text
    #         fund_amount = jijin.find_element_by_xpath('./td[2]').text
    #         fund_ratio = jijin.find_element_by_xpath('./td[3]').text
    #         fund_shareholding_data['stock_code'].append(stock_code)
    #         fund_shareholding_data['fund_name'].append(fund_name)
    #         fund_shareholding_data['fund_amount'].append(fund_amount)
    #         fund_shareholding_data['fund_ratio'].append(fund_ratio)
    #         print(f'{stock_code}   {fund_name}   {fund_amount}   {fund_ratio}')
    # df = pd.DataFrame(fund_shareholding_data)
    # df.to_csv('基金持股数据.csv', encoding='utf-8-sig', index=False)

    # print('-------------------------------------------------------------------------------------------------')

    print('正在爬取公司数据......')
    for stock_code in stock_data['stock_code']:
        driver.get(f'https://xueqiu.com/snowman/S/{stock_code}/detail#/GSJJ')
        try:
            company_name = driver.find_element_by_xpath('//td[text()="公司名称"]/following-sibling::td').text
            business_scope = driver.find_element_by_xpath('//td[text()="主营业务"]/following-sibling::td').text
            province = driver.find_element_by_xpath('//td[text()="所属省份"]/following-sibling::td').text
            actual_controller = driver.find_element_by_xpath('//td[text()="实际控制人"]/following-sibling::td').text
        except:
            continue
        company_data['stock_code'].append(stock_code)
        company_data['company_name'].append(company_name)
        company_data['business_scope'].append(business_scope)
        company_data['province'].append(province)
        company_data['actual_controller'].append(actual_controller)
        print(f'{stock_code}   {company_name}   {business_scope}   {province}   {actual_controller}')
    df = pd.DataFrame(company_data)
    df.to_csv('公司数据.csv', encoding='utf-8-sig', index=False)

    print('-------------------------------------------------------------------------------------------------')

    print('正在爬取公司高管数据......')
    for stock_code in stock_data['stock_code']:
        driver.get(f'https://xueqiu.com/snowman/S/{stock_code}/detail#/GSGG')
        try:
            company_name = company_data['company_name'][stock_data['stock_code'].index(stock_code)]
        except:
            continue
        manager_list = driver.find_elements_by_xpath('//*[@class="brief-info"]//tbody/tr')
        for manager in manager_list:
            manager_name = manager.find_element_by_xpath('./td[1]').text
            manager_position = manager.find_element_by_xpath('./td[2]').text
            company_executive_data['company_name'].append(company_name)
            company_executive_data['manager_name'].append(manager_name)
            company_executive_data['manager_position'].append(manager_position)
            print(f'{company_name}   {manager_name}   {manager_position}')
    df = pd.DataFrame(company_executive_data)
    df.to_csv('公司高管数据.csv', encoding='utf-8-sig', index=False)