import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
}
data = {
    'stockId': '688981',
    'reporttype': '5000'
}

if __name__ == '__main__':
    url = 'https://ssecurity.seentao.com/api/security/security.balancesheet.get'
    response = requests.post(url=url, data=data, headers=headers).json()
    print()

