import os
import time
from datetime import datetime
import pandas as pd
import requests
from selenium import webdriver

# 账号密码
username = 'admin_3941@xiaoman.smart'
password = '3tleg7'
# 关键词
keyword = 'Cloth'
# 筛选国家
county_list = ["RU", "TR", "ID", "IN", "UY", "UA", "BR", "IT", "DE", "FR", "GB", "ES", "US", "JP", "CA", "CO", "SE",
               "KR", "PE", "BE", "CZ", "AL", "AD", "BA", "HR", "GI", "GR", "VA", "MT", "ME", "PT", "SM", "RS", "SI",
               "MK", "BG", "BY", "HU", "MD", "PL", "RO", "SK", "XK", "DK", "EE", "FO", "FI", "AX", "IS", "IE", "LV",
               "LT", "NO", "SJ", "GG", "JE", "IM", "AT", "LI", "LU", "MC", "NL", "CH"]
# 是否获取图片
get_img = False
# 开始位置
start_page = 1
start_company_num = 50
# 开始标记，不需要动这个
start_sign = False

contact_data = {
    '公司名': [],
    '国家': [],
    '官网': [],
    '联系人': [],
    '职位': [],
    '邮箱': [],
    '电话': [],
    '置信度': [],
}


def create_driver():
    chrome_driver_path = '../driver/chromedriver_138.exe'
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=option)
    driver.implicitly_wait(.5)
    driver.maximize_window()
    return driver


# 等待一个元素出现
def wait_ele_show(driver, xpath):
    for _ in range(3):
        try:
            driver.find_element_by_xpath(xpath)
            time.sleep(1)
            break
        except:
            time.sleep(1)


if __name__ == "__main__":
    current_timestamp = datetime.now().strftime('%Y%m%d')
    # 创建driver
    driver = create_driver()
    driver.get('https://crm.xiaoman.cn/')
    # 登录账号
    wait_ele_show(driver, '//*[@id="email"]')
    driver.find_element_by_xpath('//*[@id="email"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
    driver.find_element_by_xpath('//*[@class="agree-checkbox"]').click()
    driver.find_element_by_xpath('//span[text()="登录"]').click()
    time.sleep(2)
    # 跳转到搜索页面，
    base_url = "https://crm.xiaoman.cn/new_discovery/mining-v2/list?filter=%7B%22keyword%22%3A%22{}%22%2C%22keywordOperator%22%3A%22OR%22%2C%22countryCode%22%3A%5B"
    country_codes = "%22" + "%22%2C%22".join(county_list) + "%22"
    url = base_url.format(keyword) + country_codes + "%5D%7D"
    driver.get(url)
    wait_ele_show(driver, '//div[contains(text(),"筛选")]')
    # 点击精准
    driver.find_element_by_xpath('//span[text()="精准"]/following-sibling::button').click()
    time.sleep(1)
    # 点击筛选，通过js点击筛选条件，筛选完后选择每页条数为100条
    driver.find_element_by_xpath('//div[contains(text(),"筛选")]').click()
    time.sleep(1)
    click_screening_js = """
     const xpaths = [
        '//span[text()="公司名称"]/preceding-sibling::span/input',
        '//span[text()="进口"]/preceding-sibling::span/input',
        '//span[text()="有联系人"]/preceding-sibling::span/input'
    ];
    xpaths.forEach(xpath => {
        const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue;
        if (element) {
            element.click();
        }
    });
    """
    driver.execute_script(click_screening_js)
    driver.find_element_by_xpath('//button/span[text()="筛 选"]').click()
    wait_ele_show(driver, '//*[contains(@class,"pagination-size-change")]//*[@class="okki-select-selection-item"]')
    time.sleep(3)
    driver.find_element_by_xpath('//*[contains(@class,"pagination-size-change")]//*[@class="okki-select-selection-item"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[text()="100 条/页"]').click()
    wait_ele_show(driver, '//span[contains(text(),"为你搜索信息")]')
    company_page_num = int(driver.find_element_by_xpath('(//*[contains(@class,"okki-pagination-item")]//a[@rel="nofollow"])[last()]').text)
    for company_page in range(company_page_num):
        # 判断从哪一页开始
        if not start_sign and company_page + 1 < start_page:
            driver.find_element_by_xpath('//*[@class="search-result-body"]//*[@title="下一页"]').click()
            time.sleep(1)
            wait_ele_show(driver, '(//*[@class="okki-table-tbody"]/tr[contains(@class,"comment-row")]//*[@class="item-title"])/span[1]')
            continue
        # 获取所有公司列表
        company_eles = driver.find_elements_by_xpath('(//*[@class="okki-table-tbody"]/tr[contains(@class,"comment-row")]//*[@class="item-title"])/span[1]')
        for company_ele in company_eles:
            if not start_sign and company_eles.index(company_ele) + 1 < start_company_num:
                continue
            start_sign = True
            company_ele.click()
            wait_ele_show(driver, '//*[@class="drawer-card-container"]')
            country = driver.find_element_by_xpath('//*[@class="item-country mr-16px"]').text
            try:
                website = driver.find_element_by_xpath('//*[contains(@class,"normal-url")]').text
            except:
                website = ''
            if get_img:
                # 获取商品图
                try:
                    driver.find_element_by_xpath('//*[@class="image-more"]').click()
                    has_image = True
                except:
                    has_image = False
                if has_image:
                    time.sleep(1)
                    os.makedirs(f'图片/{company_ele.text}', exist_ok=True)
                    image_list = driver.find_elements_by_xpath('//*[@class="okki-popover-inner-content"]//*[@class="okki-image-img"]')
                    for image in image_list:
                        response = requests.get(image.get_attribute('src'))
                        if response.status_code == 200:
                            # 将图片保存到本地
                            with open(f"图片/{company_ele.text}/image_{image_list.index(image)}.jpg", "wb") as file:
                                file.write(response.content)
                            print(f"图片下载成功，保存为 {company_ele.text}/image_{image_list.index(image)}.jpg")
                        else:
                            print(f"下载失败，状态码: {response.status_code}")
                        print(f'共{len(image_list)}张图片，正在获取第{image_list.index(image) + 1}张')
            # 获取联系人
            driver.find_element_by_xpath('//div[@role="tab"]//div[contains(text(),"联系人")]').click()
            wait_ele_show(driver, '//span[text()="邮箱"]/following-sibling::button')
            driver.find_element_by_xpath('//span[text()="邮箱"]/following-sibling::button').click()
            driver.find_element_by_xpath('//*[contains(@class,"drawer-card-container")]//*[@class="okki-select-selection-item"]').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[contains(@class,"drawer-card-container")]//*[text()="100 条/页"]').click()
            time.sleep(1)
            contact_page_num = int(driver.find_element_by_xpath('(//*[contains(@class,"drawer-card-container")]//*[@rel="nofollow"])[last()]').text)
            for page in range(contact_page_num):
                contact_list = driver.find_elements_by_xpath('//*[contains(@class,"drawer-card-container")]//*[@class="okki-table-tbody"]/tr[contains(@class,"okki-table-row")]')
                for contact in contact_list:
                    name = contact.find_element_by_xpath('./td[3]//span').text
                    positions = contact.find_element_by_xpath('./td[4]//span').text
                    email = contact.find_element_by_xpath('./td[5]//span').text
                    phone = contact.find_element_by_xpath('./td[6]//span').text.replace('\n', '')
                    confidence = contact.find_element_by_xpath('./td[8]').text
                    print(f'正在爬取第{company_page + 1}页公司，第{company_eles.index(company_ele) + 1}个公司，共{contact_page_num}页联系人，正在获取第{page + 1}页，第{contact_list.index(contact) + 1}个联系人：{name}   {positions}   {email}   {phone}   {confidence}')
                    contact_data['公司名'].append(company_ele.text)
                    contact_data['国家'].append(country)
                    contact_data['官网'].append(website)
                    contact_data['联系人'].append(name)
                    contact_data['职位'].append(positions)
                    contact_data['邮箱'].append(email)
                    contact_data['电话'].append(phone)
                    contact_data['置信度'].append(confidence)
                driver.find_element_by_xpath('//*[contains(@class,"drawer-card-container")]//*[@title="下一页"]').click()
                time.sleep(1)
            driver.find_element_by_xpath('(//*[@d="m8 8 32 32M8 40 40 8"])[last()]').click()
            df = pd.DataFrame(contact_data)
            df.to_excel(f'小满发现联系人_{current_timestamp}.xlsx', index=False)
        driver.find_element_by_xpath('//*[@class="search-result-body"]//*[@title="下一页"]').click()
        time.sleep(1)
        wait_ele_show(driver, '(//*[@class="okki-table-tbody"]/tr[contains(@class,"comment-row")]//*[@class="item-title"])/span[1]')
