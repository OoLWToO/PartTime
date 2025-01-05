import json
import os
import random
import time

import requests

headers = {
    "Content-Type": "application/json;charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}
data = {
    'orderBy': "PUBLISHDATE DESC"
}

if __name__ == '__main__':
    # 检查路径是否存在
    if not os.path.exists('银河期贷_PDF'):
        os.makedirs('银河期贷_PDF')
    data = json.dumps(data)
    # 循环6-9页
    for page in range(6, 10):
        url = f'https://www.yhqh.com.cn/ajax/list_page?siteId=1&columnId=452&subId=0&pageNumber={page-1}&pageSize=10'
        response = requests.post(url=url, data=data, headers=headers).json()['info']
        results = response['list']
        for result in results:
            print(f'共{response["totalCount"]}条数据, 正在爬取第{results.index(result)}条')
            download_url = f'https://www.yhqh.com.cn/upload{result["finfo"]["FILE"]}'
            r = requests.get(download_url, headers=headers)
            time.sleep(round(random.uniform(10, 20), 2))
            with open(f'银河期贷_PDF/{result["TITLE"]}.pdf', 'wb') as pdf_file:
                pdf_file.write(r.content)
                print(f'{result["TITLE"]}保存成功！！！')
