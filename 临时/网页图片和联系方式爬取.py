import os
import time
import random
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# 自动检测 Safari 是否可用，否则使用 Chrome
def setup_driver():
    try:
        driver = webdriver.Safari()  # Safari 需要手动启用远程自动化
        print("使用 Safari WebDriver")
    except Exception as e:
        print(f"Safari 启动失败：{e}, 尝试使用 Chrome WebDriver")

        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")  # 反检测
        options.add_argument("--headless")  # 无头模式
        options.add_argument("--disable-gpu")  # 禁用GPU加速
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")  # 设置常见的 User-Agent

        service = Service("chromedriver")  # 需安装 ChromeDriver
        driver = webdriver.Chrome(service=service, options=options)
        print("使用 Chrome WebDriver")

    driver.implicitly_wait(10)  # 设置隐式等待
    return driver

def create_driver():
    chrome_driver_path = '../driver/chromedriver_119.exe'
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=option)
    driver.implicitly_wait(.5)
    driver.maximize_window()
    return driver


# 为每个网址创建文件夹
def create_folder_for_url(base_folder, url, keyword):
    sanitized_url = re.sub(r'\W+', '_', url)  # 仅替换非字母数字字符
    folder_name = f"{base_folder}/{keyword}_{sanitized_url}"  # 将替换后的 URL 插入文件夹名称
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name


# 爬取关键词链接、图片和联系方式
def scrape_keyword_links_and_images(driver, url, keyword, base_folder):
    results = {"links": [], "images": [], "contacts": []}
    driver.get(url)

    try:
        # 等待页面加载完成，通过等待页面上的某个特定元素来确保加载完成
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'company')]"))
            # 等待页面中的某个链接加载完成（可以根据页面的实际元素进行修改）
        )
        print(f"正在访问：{url}（关键词：{keyword}）")

        # 强制等待 30 秒，确保页面完全加载
        time.sleep(30)

        # 获取页面中的所有 <a> 和 <img> 标签
        elements = driver.execute_script("return document.querySelectorAll('a, img');")
        for element in elements:
            text = element.text.strip()
            link = element.get_attribute("href")

            # 提取匹配关键词的链接
            if link and re.search(rf"{keyword}", text, re.IGNORECASE):
                print(f"找到链接：{link}（{keyword}）")
                results["links"].append(link)

            # 提取图片的 src 地址
            src = element.get_attribute("src")
            if src:
                print(f"找到图片：{src}")
                results["images"].append(src)

            # 提取包含联系方式的文本（假设为“联系方式”、“电话”、“微信”等）
            if re.search(r"联系方式|电话|微信", text):
                print(f"找到联系方式：{text}")
                results["contacts"].append(text)

    except Exception as e:
        print(f"页面加载失败：{e}")

    # 创建对应的文件夹
    folder_name = create_folder_for_url(base_folder, url, keyword)

    # 保存图片
    image_folder = os.path.join(folder_name, "图片")
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # 保存图片到文件夹
    for img_url in results["images"]:
        try:
            img_data = requests.get(img_url).content
            img_name = os.path.join(image_folder, img_url.split("/")[-1])
            with open(img_name, 'wb') as img_file:
                img_file.write(img_data)
            print(f"图片已保存：{img_name}")
        except Exception as e:
            print(f"图片下载失败：{e}")

    # 保存信息到文本文件
    with open(os.path.join(folder_name, "extracted_links_images_contacts_summary.txt"), "w", encoding="utf-8") as file:
        file.write(f"关键词：{keyword}\n")
        file.write("链接：\n")
        for link in results["links"]:
            file.write(f"{link}\n")
        file.write("图片：\n")
        for img in results["images"]:
            file.write(f"{img}\n")
        file.write("联系方式：\n")
        for contact in results["contacts"]:
            file.write(f"{contact}\n")

    return results


# 主函数
def main(urls, keywords, base_folder="爬取数据"):
    driver = create_driver()

    try:
        for url in urls:
            for keyword in keywords:
                print(f"开始爬取：{url}，关键词：{keyword}")
                results = scrape_keyword_links_and_images(driver, url, keyword, base_folder)
                time.sleep(random.uniform(5, 10))  # 随机延迟，防止封 IP
    finally:
        driver.quit()

    print("所有关键词提取完成！")


# 运行
if __name__ == "__main__":
    print("启动 WebDriver...")
    urls_to_scrape = [
        "https://s.1688.com/company/pc/factory_search.htm?keywords=%B7%FE%D7%B0&spm=a26352.24780423.searchbox.input",
        "https://s.1688.com/company/pc/factory_search.htm?keywords=%B7%FE%D7%B0&spm=a26352.24780423.searchbox.input&beginPage=2#sm-filtbar",
        "https://s.1688.com/company/pc/factory_search.htm?keywords=%B7%FE%D7%B0&spm=a26352.24780423.searchbox.input&beginPage=3#sm-filtbar",
        # 将生成的 URL 列表添加到这里
        *[
            f"https://s.1688.com/company/pc/factory_search.htm?keywords=%B7%FE%D7%B0&spm=a26352.24780423.searchbox.input&beginPage={i}#sm-filtbar"
            for i in range(4, 152)]
    ]
    keywords = ["服装", "服饰", "工厂"]  # 需要查找的关键词
    main(urls_to_scrape, keywords)
