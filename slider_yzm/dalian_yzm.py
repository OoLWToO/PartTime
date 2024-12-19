import os
import re
import time

from selenium import webdriver
from selenium.webdriver import ActionChains


def create_driver():
    chrome_driver_path = '../driver/chromedriver_119.exe'
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=option)
    driver.implicitly_wait(.5)
    driver.maximize_window()
    return driver


def handle_slider_yzm(threshold):
    import base64
    image_path = 'image_cache'
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    time.sleep(.5)
    background_base64 = driver.find_element_by_xpath('//*[@id="slideVerify"]//img[not(@style)]').get_attribute('src').replace('data:image/jpg;base64,', '')
    target_base64 = driver.find_element_by_xpath('//*[@id="slideVerify"]//img[@style]').get_attribute('src').replace('data:image/png;base64,', '')
    image_data = base64.b64decode(background_base64)
    with open(f'{image_path}\\background.png', 'wb') as file:
        file.write(image_data)
    image_data = base64.b64decode(target_base64)
    with open(f'{image_path}\\target.png', 'wb') as file:
        file.write(image_data)
    with open(f'{image_path}\\background.png', 'rb') as f:
        background_bytes = f.read()
    with open(f'{image_path}\\target.png', 'rb') as f:
        target_bytes = f.read()
    # 滑块验证码匹配，获取匹配结果
    res = slide_match(target_bytes, background_bytes, threshold)
    print(f'滑块验证码坐标: {res}')
    return res['target'][0]


def slide_match(target_bytes: bytes = None, background_bytes: bytes = None, threshold: int = 100):
    import cv2
    import numpy as np
    target = cv2.imdecode(np.frombuffer(target_bytes, np.uint8), cv2.IMREAD_ANYCOLOR)

    background = cv2.imdecode(np.frombuffer(background_bytes, np.uint8), cv2.IMREAD_ANYCOLOR)

    background = cv2.Canny(background, threshold, threshold * 2)
    target = cv2.Canny(target, threshold, threshold * 2)

    background = cv2.cvtColor(background, cv2.COLOR_GRAY2RGB)
    target = cv2.cvtColor(target, cv2.COLOR_GRAY2RGB)

    res = cv2.matchTemplate(background, target, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    h, w = target.shape[:2]
    bottom_right = (max_loc[0] + w, max_loc[1] + h)
    return {"target": [int(max_loc[0]), int(max_loc[1]), int(bottom_right[0]), int(bottom_right[1])]}


if __name__ == "__main__":
    driver = create_driver()
    driver.get('https://etax.dalian.chinatax.gov.cn/')
    driver.find_element_by_xpath('//*[@title="关闭"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//i[@class="icon icon-login"]').click()
    driver.find_elements_by_xpath('//*[contains(@placeholder,"统一社会信用代码")]')
    driver.find_element_by_xpath('//*[contains(@placeholder,"统一社会信用代码")]').send_keys('1')
    driver.find_element_by_xpath('//*[contains(@placeholder,"居民身份证号码")]').send_keys('1')
    driver.find_element_by_xpath('//*[contains(@placeholder,"个人用户密码")]').send_keys('1')
    driver.find_element_by_xpath('//button/span[text()="登录"]').click()

    success = fail = 0

    for i in range(100):
        print(i + 1)
        threshold = 100
        time.sleep(.5)
        yzm = handle_slider_yzm(threshold)
        slider = driver.find_element_by_xpath('//*[@class="slide-verify-slider-mask-item-icon"]')
        ActionChains(driver).click_and_hold(slider).perform()
        ActionChains(driver).move_by_offset(yzm, 0).perform()
        slider_position = driver.find_element_by_xpath('//*[@id="slideVerify"]//img[@style]').get_attribute('style')
        try:
            slider_position = float(re.search(r'left:\s*(\d+\.\d+)px', slider_position).group(1))
            ActionChains(driver).move_by_offset(yzm - slider_position + 1, 0).perform()
        except:
            print()
        ActionChains(driver).release(slider).perform()
        time.sleep(1)
        try:
            driver.find_element_by_xpath('//*[@role="alert"]')
            print('验证成功')
            time.sleep(5)
            driver.find_element_by_xpath('//button/span[text()="登录"]').click()
            success += 1
        except:
            print('验证失败')
            time.sleep(1.5)
            for _ in range(2):
                threshold += 100
                yzm = handle_slider_yzm(threshold)
                slider = driver.find_element_by_xpath('//*[@class="slide-verify-slider-mask-item-icon"]')
                ActionChains(driver).click_and_hold(slider).perform()
                ActionChains(driver).move_by_offset(yzm, 0).perform()
                slider_position = driver.find_element_by_xpath('//*[@id="slideVerify"]//img[@style]').get_attribute(
                    'style')
                slider_position = float(re.search(r'left:\s*(\d+\.\d+)px', slider_position).group(1))
                ActionChains(driver).move_by_offset(yzm - slider_position + 1, 0).perform()
                ActionChains(driver).release(slider).perform()
                time.sleep(1.5)
                try:
                    driver.find_element_by_xpath('//*[@role="alert"]')
                    break
                except:
                    pass
            driver.find_element_by_xpath('//button/span[text()="登录"]').click()
            fail += 1
    print(f'成功数：{success}')
    print(f'失败数：{fail}')
    print(f'成功率：{success / 100}%')
