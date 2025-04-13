import requests

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-length": "111",
    "content-type": "application/x-www-form-urlencoded",
    "cookie": "shop_version_type=4; anony_token=60e3d3e30b059d2e530d0e2a5723e743; xenbyfpfUnhLsdkZbX=0; sensorsdata2015jssdkcross=%7B%22%24device_id%22%3A%221962e281d50237c-0233a502e5d4948-26011c51-3686400-1962e281d5135d4%22%7D; sajssdk_2015_new_user_appt0hp9gsj7446_xet_citv_cn=1; ko_token=6f47fe04dd00fdd28bf8915bb7c7bca4; newuserdays=90; olduserdays=180; regtime=1675828195; sa_jssdk_2015_appt0hp9gsj7446_xet_citv_cn=%7B%22distinct_id%22%3A%22u_63e31be3468b7_PmbIhpkqgz%22%2C%22first_id%22%3A%221962e281d50237c-0233a502e5d4948-26011c51-3686400-1962e281d5135d4%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%7D; logintime=1744531363",
    "origin": "https://appt0hp9gsj7446.xet.citv.cn",
    "priority": "u=1, i",
    "referer": "https://appt0hp9gsj7446.xet.citv.cn/p/course/text/i_66dbfe9ce4b023c0611dc003?product_id=p_63e1c0b5e4b0fc5d122d9af0",
    "req-uuid": "20250413160321000191903",
    "retry": "1",
    "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

data = {
    'bizData[resource_id]': 'i_66dbfe9ce4b023c0611dc003',
    'bizData[resource_type]': '1',
    'bizData[check_available]': '1',
}

if __name__ == '__main__':
    url = 'https://appt0hp9gsj7446.xet.citv.cn/xe.course.business.courseware_list.get/2.0.0'
    response = requests.post(url=url, data=data, headers=headers)
    print()

