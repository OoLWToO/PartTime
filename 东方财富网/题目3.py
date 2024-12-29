import time
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

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
    now = datetime.now()
    current_date = now.strftime('%m-%d %H:%M')
    # 创建driver
    driver = create_driver()
    driver.get('http://guba.eastmoney.com/list,872351.html')
    while True:
        # 获取最新文章的时间，如果时间大于当前时间，则退出循环获取详细
        up_to_date = driver.find_element_by_xpath('//*[@class="listbody"]/tr[1]//*[@class="update mod_time"]').text
        # if up_to_date > current_date:
        #     break
        if up_to_date > '12-27 18:25':
            break
        driver.refresh()
        time.sleep(10)
    driver.find_element_by_xpath('//*[@class="listbody"]/tr[1]//*[@class="title"]/a').click()
    time.sleep(3)
    # 切换到新打开的窗口，即最后一个窗口
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    # 获取新闻标题和内容
    news_title = driver.find_element_by_xpath('//*[@class="newstitle"]').text
    news_content = driver.find_element_by_xpath('//*[@class="newstext "]').text
    # 打开小红书登录，发表文章
    driver.get('https://creator.xiaohongshu.com/publish/publish?source=official')
    time.sleep(5)
    # 登录操作
    driver.find_element_by_xpath('//input[@placeholder="手机号"]').send_keys('18665448472')
    driver.find_element_by_xpath('//*[text()="发送验证码"]').click()
    while True:
        print('等待输入验证码中...')
        try:
            driver.find_element_by_xpath('//a[contains(text(),"发布笔记")]')
            time.sleep(3)
            break
        except NoSuchElementException:
            time.sleep(5)
    # 上传文章
    driver.find_element_by_xpath('//*[text()="上传图文"]').click()
    # 上传测试图片
    driver.find_element_by_xpath('//*[@class="upload-input"]').send_keys('D:\Work\PartTime\东方财富网\测试.png')
    time.sleep(3)
    # 输入标题和内容
    driver.find_element_by_xpath('//input[contains(@placeholder,"填写标题")]').send_keys(news_title[:20])
    driver.find_element_by_xpath('//*[contains(@data-placeholder,"输入正文")]').send_keys(news_content[:1000])
    time.sleep(10)
    driver.find_element_by_xpath('//span[text()="发布"]').click()
