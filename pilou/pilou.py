import requests
from lxml import etree

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9',
    'host': 'www.chinabond.com.cn',
    'referer': 'https://www.chinabond.com.cn/dfz/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

if __name__ == '__main__':
    url = 'https://www.chinabond.com.cn/cbiw/lgb/infoListByPath'
    for page in range(566):
        params = {"_tp_lgbInfo": f"{page+1}", 'pageSize': '10', 'channelName': 'zdfzxxpl_xxplwj'}
        r = requests.get(url, headers=headers, params=params)
        doc_list = r.json()['lgbInfoList']
        for doc in doc_list:
            doc_title = doc['title']
            doc_date = doc['createTime']
            print(f'{doc_title}   {doc_date}')
