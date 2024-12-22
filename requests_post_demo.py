import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
}
data = {
    'limit': '1000',
    'current': '',
    'pubDateStartTime': '2024-01-01',
    'pubDateEndTime': '2024-12-22',
    'prodPcatid': '',
    'prodCatid': '',
    'prodName': '大白菜',
}

if __name__ == '__main__':
    url = 'http://www.xinfadi.com.cn/getPriceData.html'
    response = requests.post(url=url, data=data, headers=headers).json()
    print()

