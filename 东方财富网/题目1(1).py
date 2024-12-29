import time

import pandas as pd
from selenium import webdriver
from datetime import datetime

data = {
    '榜单': [],
    '当前排名': [],
    '历史趋势': [],
    '代码': [],
    '股票名称': [],
}


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
    driver.get('https://guba.eastmoney.com/rank/?from=')
    ranking_list = ['人气榜', '飙升榜']
    for ranking in ranking_list:
        driver.find_element_by_xpath(f'//*[contains(@class,"ranktit") and contains(text(),"{ranking}")]').click()
        time.sleep(2)
        for page in range(4):
            stock_list = driver.find_elements_by_xpath('//*[@class="stock_tbody"]/tr')
            for stock in stock_list:
                try:
                    current_ranking = stock.find_element_by_xpath('./td[1]//*[contains(@class,"ranktop icon icon_rank")]')
                    current_ranking = current_ranking.get_attribute('class')[-1]
                except:
                    current_ranking = stock.find_element_by_xpath('./td[1]').text
                historical_trends = stock.find_element_by_xpath('./td[2]').text
                code = stock.find_element_by_xpath('./td[4]').text
                stock_name = stock.find_element_by_xpath('./td[5]').text
                print(f'{current_ranking}   {historical_trends}   {code}   {stock_name}')
                data['榜单'].append(ranking)
                data['当前排名'].append(current_ranking)
                data['历史趋势'].append(historical_trends)
                data['代码'].append(code)
                data['股票名称'].append(stock_name)
            driver.find_element_by_xpath('//*[@class="go_page" and text()="下一页"]').click()
            time.sleep(2)
    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    df = pd.DataFrame(data)
    df.to_excel(f'{current_date}东方财富网榜单数据.xlsx', index=False)
    driver.quit()