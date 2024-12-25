import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
}
data = {
    'searchType': 'MulityTermsSearch',
    'ArticleType': '0',
    'ReSearch': '',
    'ParamIsNullOrEmpty': 'false',
    'Islegal': 'false',
    'Content': '测试',
    'Order': '1',
    'Page': '1',
}

if __name__ == '__main__':
    url = 'https://search.cnki.com.cn/api/search/listresult'
    response = requests.post(url=url, data=data, headers=headers).json()
    print()

