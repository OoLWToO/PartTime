from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def find_ele_by_xpath(driver, xpath):
    try:
        return driver.find_element_by_xpath(xpath)
    except:
        print(f'{xpath} not find')
        return ''


def find_ele_and_click(driver, xpath):
    return driver.find_element_by_xpath(xpath).click()


def find_eles_by_xpath(driver, xpath):
    return driver.find_elements_by_xpath(xpath)


def input_by_xpath(driver, xpath, text):
    return driver.find_element_by_xpath(xpath).send_keys(text)


def find_ele_visibility_by_xpath(driver, xpath):
    return WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))


def wait_ele_disappear(driver, xpath):
    try:
        WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.XPATH, xpath)))
    except Exception as e:
        print(f'ele located fall {xpath} {e}')


def scroll_to_bottom(driver):
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", find_ele_by_xpath(driver, '//*[@class="rate-container-results"]'))
