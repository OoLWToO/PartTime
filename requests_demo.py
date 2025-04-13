import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

if __name__ == '__main__':
    url = 'https://tps.kdlapi.com/api/gettpspro/?secret_id=oidgnb7luycrdctiwjkh&signature=sezctbabfpt22meej3damun8g5uuex5q&num=1&pt=1&format=json&sep=1'
    r = requests.get(url, headers=headers)
    html = etree.HTML(r.text)
    print()