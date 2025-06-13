import random
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

# keywords = ['故宫文创', '寺庙景区', '寺庙旅游', '寺庙伴手礼', '寺庙周边']
keyword = '寺庙周边'


if __name__ == "__main__":
    # 设置爬取数量
    climb_num = 200
    # 创建driver
    driver = create_driver()
    driver.get('https://www.xiaohongshu.com/explore')
    time.sleep(2)
    # 登录账号
    driver.find_element_by_xpath('//*[text()="获取验证码"]').click()
    input('手动输入验证码登录一下账号')
    driver.find_element_by_xpath('//*[@placeholder="搜索小红书"]').send_keys(keyword)
    driver.find_element_by_xpath('//*[@class="search-icon"]').click()
    time.sleep(2)
    data = {
        '链接': [],
        '标题': [],
        '点赞量': [],
        '收藏量': [],
        '评论量': [],
        '发布时间': [],
        '标签': [],
    }
    while len(data['链接']) < climb_num:
        article_list = driver.find_elements_by_xpath('//*[@class="feeds-container"]/section')
        for article in article_list:
            try:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", article)
            except:
                break
            try:
                link = article.find_element_by_xpath('.//a[@class="cover mask ld"]').get_attribute('href')
            except:
                continue
            if link in data['链接']:
                continue
            time.sleep(random.uniform(2, 4))
            article.click()
            time.sleep(.5)
            detail_ele = driver.find_element_by_xpath('//*[@class="interaction-container"]')
            try:
                # 可能没有标题
                title = detail_ele.find_element_by_xpath('.//*[@class="title"]').text
            except:
                title = ''
            like_num = detail_ele.find_element_by_xpath('.//*[@class="left"]//*[@class="reds-icon like-icon"]/following-sibling::span').text.replace('点赞', '0')
            collect_num = detail_ele.find_element_by_xpath('.//*[@class="left"]//*[@class="reds-icon collect-icon"]/following-sibling::span').text.replace('收藏', '0')
            comment_num = detail_ele.find_element_by_xpath('.//*[@class="left"]//*[@class="reds-icon"]/following-sibling::span').text.replace('评论', '0')
            publish_time = detail_ele.find_element_by_xpath('.//*[@class="bottom-container"]/span[@class="date"]').text.replace('编辑于', '').replace(' ', '')
            tag = '/'.join([tag.text for tag in detail_ele.find_elements_by_xpath('.//*[@class="note-text"]//a')])
            print(link, title, like_num, collect_num, comment_num, publish_time, tag)
            data['链接'].append(link)
            data['标题'].append(title)
            data['点赞量'].append(like_num)
            data['收藏量'].append(collect_num)
            data['评论量'].append(comment_num)
            data['发布时间'].append(publish_time)
            data['标签'].append(tag)
            print(f'当前{keyword}数据数量{len(data["链接"])}')
            driver.find_element_by_xpath('//*[@class="close close-mask-dark"]').click()
            time.sleep(.5)
        df = pd.DataFrame(data)
        df.to_excel(f'小红书{keyword}文章数据.xlsx', index=False)
    print('爬取完成')
    driver.quit()
