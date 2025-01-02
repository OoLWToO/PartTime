import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

if __name__ == '__main__':
    url = 'https://www.yuque.com/oolwtoo/lrhzza/grs6kagcekgnrzsy'
    r = requests.get(url, headers=headers)
    html = etree.HTML(r.text)
    print()