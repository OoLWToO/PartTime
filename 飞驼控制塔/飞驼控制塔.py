import json
import time
from datetime import datetime

import requests

data = {
    '船名': [],
    '航次': [],
    '计划离港': [],
    '离港准点': [],
    '计划到港': [],
    '到准点': [],
    '总航程': [],
    '周几': [],
    '天数': [],
    '起运码头': [],
    '目的码头': [],
    '航线': [],
}

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "authorization": "Bearer ddba5e50-ee51-4d02-b542-7ec52efead76",
    "iframe-referrer": "https://www.freightower.com/",
    "origin": "https://i.saas.freightower.com",
    "priority": "u=1, i",
    "referer": "https://i.saas.freightower.com/",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}

polName = '上海'  # 起始港
podName = '鹿特丹'  # 目的港

if __name__ == '__main__':
    pol_url = 'https://openapi.freightower.com/vessel2/location/ports?key=' + polName
    pod_url = 'https://openapi.freightower.com/vessel2/location/ports?key=' + podName
    pol_response = requests.get(url=pol_url, headers=headers).json()
    time.sleep(5)
    pod_response = requests.get(url=pod_url, headers=headers).json()
    if len(pol_response['data']) > 1:
        for index, r in enumerate(pol_response['data']):
            print(f"{index + 1}.{r['portCn']}")
        choice = input('有多个选项，请选择起始港港口编号: ')
        polCode = pol_response['data'][int(choice)]['portCode']
    else:
        polCode = pol_response['data'][0]['portCode']
    if len(pod_response['data']) > 1:
        for index, r in enumerate(pod_response['data']):
            print(f"{index + 1}.{r['portCn']}")
        choice = int(input('有多个选项，请选择目的港港口编号: ')) - 1
        podCode = pod_response['data'][int(choice)]['portCode']
    else:
        podCode = pod_response['data'][0]['portCode']
    search_date = datetime.now().strftime('%Y-%m-%d')
    print('\n起始港代码：' + polCode + '，目的港代码：' + podCode + '，查询时间：' + search_date)
    print('查询中...\n')
    direct_url = f'https://openapi.freightower.com/application/schedule/p2p/group?polCode={polCode}&podCode={podCode}&etd={search_date}&eta=&weeksOut=8&pageNum=1&pageSize=10000&isTransit=0'
    transfer_url = f'https://openapi.freightower.com/application/schedule/p2p/group?polCode={polCode}&podCode={podCode}&etd={search_date}&eta=&weeksOut=8&pageNum=1&pageSize=10000&isTransit=1'
    direct_response = requests.get(url=direct_url, headers=headers).json()
    time.sleep(5)
    transfer_response = requests.get(url=transfer_url, headers=headers).json()
    if direct_response['content'] == 0:
        print('没有直达方案')
    else:
        print(f'共查到{len(direct_response["content"])}直达方案')
        for r in direct_response['content']:
            ship_list_url = f'https://openapi.freightower.com/application/schedule/p2p/group?polCode={polCode}&podCode={podCode}&etd={search_date}&eta=&weeksOut=8&pageNum=1&pageSize=10000&isTransit=0&displayGroup={r["groupName"]}'
            ship_list_response = requests.get(url=detail_url, headers=headers).json()
            time.sleep(5)
            print(f'共查到{len(ship_list_response["content"])}条船只信息')
            for ship in ship_list_response["content"]:
                ship_name = ship['']
                ship_code = ship['']
                plan_to_leave = ship['']
                leave_on_time = ship['']
                plan_to_arrive = ship['']
                arrive_on_time = ship['']
                total_voyage = ship['']
                week = ship['']
                days = ship['']
                start_port = ship['']
                end_port = ship['']
                route = ship['']
                print(f'{ship_name}   {ship_code}   {plan_to_leave}   {leave_on_time}   {plan_to_arrive}   {arrive_on_time}   {total_voyage}   {week}   {days}   {start_port}   {end_port}   {route}');
                direct_data = data.copy()
                direct_data['船名'].append(ship_name)
                direct_data['航次'].append(ship_code)
                direct_data['计划离港'].append(plan_to_leave)
                direct_data['离港准点'].append(leave_on_time)
                direct_data['计划到港'].append(plan_to_arrive)
                direct_data['到准点'].append(arrive_on_time)
                direct_data['总航程'].append(total_voyage)
                direct_data['周几'].append(week)
                direct_data['天数'].append(days)
                direct_data['起运码头'].append(start_port)
                direct_data['目的码头'].append(end_port)
                direct_data['航线'].append(route)
    # if transfer_response['content'] == 0:
    #     print('没有中转方案')
    # else:
    #     print(f'共查到{len(transfer_response.json()["content"])}中转方案')
    #     for r in transfer_response['data']['list']:
    #         print(f"{r['vesselName']} {r['polName']} {r['polCode']} {r['polEta']} {r['podName']} {r['podCode']} {r['podEta']}")
