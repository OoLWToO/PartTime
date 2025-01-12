import os
import time

import requests
from lxml import etree
from selenium import webdriver

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


def create_driver():
    chrome_driver_path = '../driver/chromedriver_131.exe'
    option = webdriver.ChromeOptions()
    option.add_argument(f"--proxy-server=http://{get_proxy_url()}")  # 隧道域名:端口号
    option.page_load_strategy = 'none'
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=option)
    driver.implicitly_wait(.5)
    driver.maximize_window()
    return driver


def get_current_cookie():
    # 获取当前页面Cookie
    cookies_list = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    cookie = ';'.join(item for item in cookies_list)
    return cookie

def switch_to_last_window():
    # 切换到新打开的窗口，即最后一个窗口
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])

def get_proxy_url():
    get_proxy_url = 'https://tps.kdlapi.com/api/gettpspro/?secret_id=oidgnb7luycrdctiwjkh&signature=sezctbabfpt22meej3damun8g5uuex5q&num=1&pt=1&format=json&sep=1'
    r = requests.get(get_proxy_url)
    return r.json()['data']['proxy_list'][0]


def get_sub_item_data(main_item, sub_item, sub_item_url):
    global start_sigin, username, password
    proxy_url = get_proxy_url()
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_url},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_url}
    }
    r = requests.get(sub_item_url, headers=headers, proxies=proxies)
    html = etree.HTML(r.text)
    file_num = int(html.xpath('//*[@class="cover-body"]//sup/text()')[0])
    for page in range(file_num // 20 + 1):
        print(f'正在爬取{main_item}-{sub_item}第{page + 1}页，共{file_num // 20 + 1}页')
        r = requests.get(sub_item_url.replace('.html', f'-{page + 1}.html'), headers=headers)
        html = etree.HTML(r.text)
        detail_urls = html.xpath('//*[@class="list-item default block"]//*[@class="list-body"]/a')
        for index, detail_url in enumerate(detail_urls):
            if index == 10:
                proxy_url = get_proxy_url()
                proxies = {
                    "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_url},
                    "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_url}
                }
            try:
                file_name = detail_url.xpath('./text()')[0]
            except:
                file_name = f'{main_item}_{sub_item}_{page + 1}_{index}'
            if not start_sigin and start_file_name not in file_name:
                continue
            start_sigin = True
            driver.get(detail_url.xpath('./@href')[0])
            time.sleep(1)
            file_type = driver.find_element_by_xpath('//*[text()="文档格式"]/preceding-sibling::div').text
            driver.find_element_by_xpath('(//a[text()="立即获取"])[1]').click()
            time.sleep(1)
            switch_to_last_window()
            try:
                download_url = driver.find_element_by_xpath('//a[text()="立即下载"]').get_attribute('href')
            except:
                driver.refresh()
                time.sleep(3)
                download_url = driver.find_element_by_xpath('//a[text()="立即下载"]').get_attribute('href')
            headers['referer'] = download_url
            headers['cookie'] = get_current_cookie()
            print(f'{detail_url.xpath("./@href")[0]}   {main_item}   {sub_item}   {file_name}   第{index + 1}个文件，共{len(detail_urls)}个')
            try:
                r = requests.get(download_url, headers=headers, timeout=600, proxies=proxies)
            except:
                print(f'文件出错{detail_url.xpath("./@href")[0]}—{file_name}')
                continue
            # 压缩包格式的话修改一下file_type
            if 'Rar' in str(r.content)[:10]:
                file_type = 'zip'
            with open(f'{main_item}/{sub_item}/{file_name}.{file_type}', 'wb') as pdf_file:
                pdf_file.write(r.content)
            # 关闭除了第一个窗口以外的窗口
            for handle in driver.window_handles:
                if handle != driver.window_handles[0]:
                    driver.switch_to.window(handle)
                    driver.close()
            driver.switch_to.window(driver.window_handles[0])


if __name__ == "__main__":
    start_main_item = '教师资料'    # 主标题
    start_sub_item = '教师发言'     # 副标题
    start_file_name = '中职班主任基本功技能大赛演讲（4篇）' # 开始文件
    start_sigin = False
    # 代理账密
    username = "t13669630230763"
    password = "z0hac9iq"
    # 创建driver
    driver = create_driver()
    driver.get('https://jiaowu.ijidi.cn/signin.html')
    input('登录后在控制台按下回车...')
    url = 'https://jiaowu.ijidi.cn/'
    r = requests.get(url, headers=headers)
    html = etree.HTML(r.text)
    main_eles = html.xpath('//*[@class="container"]//li[@class="menu-item menu-item-has-children"]')
    for main_ele in main_eles:
        main_item = main_ele.xpath('./a/text()')[0]
        if main_item != '更多':
            if start_sigin or start_main_item not in main_item:
                continue
        if main_item == '更多':
            more_eles = main_ele.xpath('./ul/li')
            for more_ele in more_eles:
                more_main_item = more_ele.xpath('./div/a/text()')[0]
                more_sub_eles = more_ele.xpath('./span/a')
                for more_sub_ele in more_sub_eles:
                    more_sub_item = more_sub_ele.xpath('./text()')[0]
                    if not os.path.exists(f'{main_item}/{more_sub_item}'):
                        os.makedirs(f'{main_item}/{more_sub_item}')
                    more_sub_url = more_sub_ele.xpath('./@href')[0]
                    if not start_sigin and start_sub_item not in more_sub_item:
                        continue
                    get_sub_item_data(more_main_item, more_sub_item, more_sub_url)
        else:
            if not os.path.exists(main_item):
                os.makedirs(main_item)
            sub_eles = main_ele.xpath('./ul/li/a')
            for sub_ele in sub_eles:
                sub_item = sub_ele.xpath('./text()')[0]
                if not os.path.exists(f'{main_item}/{sub_item}'):
                    os.makedirs(f'{main_item}/{sub_item}')
                sub_item_url = sub_ele.xpath('./@href')[0]
                if not start_sigin and start_sub_item not in sub_item:
                    continue
                get_sub_item_data(main_item, sub_item, sub_item_url)
