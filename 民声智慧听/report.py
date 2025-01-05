import json
import pandas as pd
from lxml import etree

data = {
    '标题': [],
    '单位': [],
    '时间': [],
    '内容': [],
}


if __name__ == "__main__":
    for i in range(1, 12):
        with open(f'response{i}.txt', 'r', encoding='utf-8') as file:
            json_data = file.read()
        results = json.loads(json_data)['data']['infoLibResults']
        for d in results:
            title = d['title']
            dept = d['deptName']
            time = d['pubTime']
            html = etree.HTML(d['content'])
            content = ''.join(html.xpath('//text()')).replace('\n', '')
            data['标题'].append(title)
            data['单位'].append(dept)
            data['时间'].append(time)
            data['内容'].append(content)
        df = pd.DataFrame(data)
        df.to_excel(f'民声智慧听通告.xlsx', index=False)