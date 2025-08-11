import time
from datetime import datetime
import pandas as pd
import requests

# 常量定义
HEADERS = {
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

WEEK_DAYS = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
BASE_URL = "https://openapi.freightower.com"


# 初始化数据结构
def init_data_structure():
    return {
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


def calculate_delay_days(start_date, end_date):
    """计算两个日期之间的天数差"""
    date_format = "%Y-%m-%d %H:%M:%S"
    try:
        date1 = datetime.strptime(start_date, date_format)
        date2 = datetime.strptime(end_date, date_format)
        return (date2 - date1).days
    except ValueError:
        return 0


def get_port_code(port_name, port_type="起始港"):
    """获取港口代码"""
    url = f'{BASE_URL}/vessel2/location/ports?key={port_name}'
    try:
        response = requests.get(url=url, headers=HEADERS).json()
        time.sleep(1)  # 礼貌性延迟

        if len(response['data']) > 1:
            print(f"\n找到多个{port_type}选项:")
            for index, port in enumerate(response['data']):
                print(f"{index + 1}. {port['portCn']}")
            choice = int(input(f'请选择{port_type}编号: ')) - 1
            return response['data'][choice]['portCode']
        return response['data'][0]['portCode']
    except Exception as e:
        print(f"获取{port_type}代码失败: {e}")
        return None


def fetch_ship_data(response_data, data_container, is_transit=False):
    """处理并提取船舶数据"""
    if not response_data.get('content'):
        print('没有找到方案' if not is_transit else '没有找到中转方案')
        return

    print(f'共查到{len(response_data["content"])}条{"中转" if is_transit else "直达"}方案')

    for group in response_data['content']:
        ship_list_url = f'{BASE_URL}/application/schedule/p2p/group?polCode={pol_code}&podCode={pod_code}&etd={search_date}&eta=&weeksOut=8&pageNum=1&pageSize=10000&isTransit={1 if is_transit else 0}&displayGroup={group["groupName"]}'

        try:
            ship_response = requests.get(url=ship_list_url, headers=HEADERS).json()
            time.sleep(1)

            print(f'当前方案下共查到{len(ship_response["content"])}条船只信息')

            for ship in ship_response["content"]:
                # 提取船舶数据
                data_container['船名'].append(ship['vessel'])
                data_container['航次'].append(ship['voyage'])
                data_container['计划离港'].append(ship['staticEtd'])
                data_container['离港准点'].append(calculate_delay_days(ship['staticEtd'], ship['etd']))
                data_container['计划到港'].append(ship['staticEta'])
                data_container['到准点'].append(calculate_delay_days(ship['staticEta'], ship['eta']))
                data_container['总航程'].append(ship['totalDuration'])
                data_container['周几'].append(WEEK_DAYS.index(group['routeEtd']) + 1)
                data_container['天数'].append(group['maxDuration'])
                data_container['起运码头'].append(group['polTerminal'])
                data_container['目的码头'].append(group['podTerminal'])
                data_container['航线'].append(group['groupName'])

                # 打印当前船舶信息
                print(f"{ship['vessel']} {ship['voyage']} {ship['staticEtd']} "
                      f"{calculate_delay_days(ship['staticEtd'], ship['etd'])} "
                      f"{ship['staticEta']} {calculate_delay_days(ship['staticEta'], ship['eta'])} "
                      f"{ship['totalDuration']} {WEEK_DAYS.index(group['routeEtd']) + 1} "
                      f"{group['maxDuration']} {group['polTerminal']} {group['podTerminal']} "
                      f"{group['groupName']}")
        except Exception as e:
            print(f"获取船舶列表失败: {e}")


def save_to_excel(data, file_prefix):
    """保存数据到Excel文件"""
    if any(len(v) > 0 for v in data.values()):  # 检查是否有数据
        df = pd.DataFrame(data)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{pol_name}-{pod_name}{file_prefix}{timestamp}.xlsx"
        df.to_excel(filename, index=False)
        print(f"数据已保存到 {filename}")
    else:
        print("没有数据需要保存")


if __name__ == '__main__':
    # 配置参数
    pol_name = '上海'  # 起始港
    pod_name = '鹿特丹'  # 目的港
    search_date = datetime.now().strftime('%Y-%m-%d')

    # 初始化数据结构
    direct_data = init_data_structure()
    transfer_data = init_data_structure()

    # 获取港口代码
    pol_code = get_port_code(pol_name, "起始港")
    pod_code = get_port_code(pod_name, "目的港")

    if not pol_code or not pod_code:
        print("无法获取港口代码，程序终止")
        exit()

    print(f'\n起始港代码：{pol_code}，目的港代码：{pod_code}，查询时间：{search_date}')
    print('查询中...\n')

    # 获取直达方案
    direct_url = f'{BASE_URL}/application/schedule/p2p/group?polCode={pol_code}&podCode={pod_code}&etd={search_date}&eta=&weeksOut=8&pageNum=1&pageSize=10000&isTransit=0'
    direct_response = requests.get(url=direct_url, headers=HEADERS).json()
    time.sleep(1)
    fetch_ship_data(direct_response, direct_data, is_transit=False)

    # 获取中转方案
    transfer_url = f'{BASE_URL}/application/schedule/p2p/group?polCode={pol_code}&podCode={pod_code}&etd={search_date}&eta=&weeksOut=8&pageNum=1&pageSize=10000&isTransit=1'
    transfer_response = requests.get(url=transfer_url, headers=HEADERS).json()
    time.sleep(1)
    fetch_ship_data(transfer_response, transfer_data, is_transit=True)

    # 保存结果
    save_to_excel(direct_data, "直达方案")
    save_to_excel(transfer_data, "中转方案")

    print('爬取完成')