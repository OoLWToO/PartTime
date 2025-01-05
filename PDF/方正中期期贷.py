import os
import random
import time

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}
data = {
    'state': '1',
    'size': '12',
    'f1': '135',
    'f2': '62',
}

if __name__ == '__main__':
    # 检查路径是否存在
    if not os.path.exists('方正中期期贷_PDF'):
        os.makedirs('方正中期期贷_PDF')
    # 循环6-9页
    for page in range(6, 10):
        url = 'https://www.founderfu.com/front/ajax_queryDynamicConsultation.do'
        data['page'] = page
        response = requests.post(url=url, data=data, headers=headers).json()
        results = response['msg']
        for result in results:
            print(f'共{response["total"]}条数据, 正在爬取第{results.index(result)}条')
            if not ('期市早班车' in result['title'] or '夜盘提示' in result['title']):
                continue
            download_url = f'https://www.founderfu.com{result["file"]}'
            r = requests.get(download_url, headers=headers)
            time.sleep(round(random.uniform(5, 20), 2))
            with open(f'方正中期期贷_PDF/{result["title"]}.pdf', 'wb') as pdf_file:
                pdf_file.write(r.content)
                print(f'{result["title"]}保存成功！！！')
