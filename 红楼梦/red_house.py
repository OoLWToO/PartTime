import pandas as pd
from selenium import webdriver

data = {
    '名字': [],
    '介绍': []
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
    driver.get('https://baijiahao.baidu.com/s?id=1794650367122142272')
    # 根据xpath获取所有人物
    person_list = driver.find_elements_by_xpath('//*[@class="dpu8C _2kCxD " and ./p[./strong]]')
    for person in person_list[:-1]:
        name = person.text[3:]
        index = 1
        info = ''
        while True:
            next_ele = person.find_element_by_xpath(f'./following-sibling::div[{index}]')
            if next_ele == person_list[person_list.index(person) + 1]:
                break
            info += next_ele.text
            index += 1
        data['名字'].append(name)
        data['介绍'].append(info)
    df = pd.DataFrame(data)
    df.to_excel(f'红楼梦人物数据.xlsx', index=False)