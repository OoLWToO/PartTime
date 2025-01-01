import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

if __name__ == '__main__':
    url = 'https://www.yuque.com/oolwtoo/lrhzza/grs6kagcekgnrzsy'
    r = requests.get(url, headers=headers)
    html = etree.HTML(r.text)
    image_urls = html.xpath('//*[@class="fileBox"]//li/img/@src')
    for image_url in image_urls:
        r = requests.get(image_url, headers=headers)
        with open(f'作业/{image_urls.index(image_url)}.png', 'wb') as news_image:
            news_image.write(r.content)