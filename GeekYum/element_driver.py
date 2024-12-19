from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def find_ele_by_xpath(driver, xpath):
    return driver.find_element_by_xpath(xpath)


def find_ele_and_click(driver, xpath):
    return driver.find_element_by_xpath(xpath).click()


def find_eles_by_xpath(driver, xpath):
    return driver.find_elements_by_xpath(xpath)


def input_by_xpath(driver, xpath, text):
    return driver.find_element_by_xpath(xpath).send_keys(text)


def wait_ele_visibility_by_xpath(driver, xpath):
    return WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))


