import json
import re
import pandas as pd
import requests
from datetime import datetime, timedelta
import urllib.parse
from lxml import etree

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Content-Type": "application/json;charset=UTF-8",
    "Cookie": "_zcy_log_client_uuid=8f055040-e3c4-11ef-9f9b-bd31e87e6a2c",
    "Origin": "https://www.zfcg.sh.gov.cn",
    "Referer": "https://www.zfcg.sh.gov.cn/site/category?parentId=137027&childrenCode=ZcyAnnouncement&utm=site.site-PC-39928.959-pc-websitegroup-navBar-front.3.8f0688c0e3c411ef9f9bbd31e87e6a2c",
    "Sec-Ch-Ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

data = {
    'Title': [],
    '来源': [],
    '发布时间': [],
    '项目编号': [],
    '标项名称': [],
    '中标（成交金额）': [],
    '中标供应商名称': [],
    '中标供应商地址': [],
    '评审总得分': [],
    '采购人名称': [],
    '采购人地址': [],
    '采购人联系方式': [],
    '采购代理机构名称': [],
    '采购代理机构地址': [],
    '采购代理机构联系方式': [],
    '项目联系人': [],
    '项目联系电话': []
}


def match_field_1(detail_result, html):
    title = detail_result['title']
    source_text = detail_result['author']
    time_text = timestamp_to_date(detail_result['publishDate'])
    project_number = detail_result['projectCode']
    try:
        item_name = html.xpath('//*[contains(@class,"code-00003")]/text()')[0]
    except IndexError:
        item_name = ''
    try:
        buyer_name = html.xpath('//*[contains(@class,"code-AM01400014")]/text()')[0]
    except IndexError:
        buyer_name = ''
    try:
        buyer_address = html.xpath('//*[contains(@class,"code-00018")]/text()')[0]
    except IndexError:
        buyer_address = ''
    try:
        buyer_contact = html.xpath('//*[contains(@class,"code-00016")]/text()')[0]
    except IndexError:
        buyer_contact = ''
    try:
        agency_name = html.xpath('//*[contains(@class,"code-00009")]/text()')[0]
    except IndexError:
        agency_name = ''
    try:
        agency_address = html.xpath('//*[contains(@class,"code-00013")]/text()')[0]
    except IndexError:
        agency_address = ''
    try:
        agency_contact = html.xpath('(//*[contains(@class,"code-00011")])[1]/text()')[0]
    except IndexError:
        agency_contact = ''
    try:
        contact_person = html.xpath('//*[contains(@class,"code-00010")]/text()')[0]
    except IndexError:
        contact_person = ''
    try:
        contact_phone = html.xpath('(//*[contains(@class,"code-00011")])[2]/text()')[0]
    except IndexError:
        contact_phone = ''
    winning_infos = html.xpath('//*[contains(@class,"code-AM01441005")]//tbody/tr')
    if winning_infos:
        for winning_info in winning_infos:
            try:
                winning_amount = winning_info.xpath('.//td[@class="code-summaryPrice"]/text()')[0]
            except IndexError:
                winning_amount = ''
            try:
                supplier_name = winning_info.xpath('.//td[@class="code-winningSupplierName"]/text()')[0]
            except IndexError:
                supplier_name = ''
            try:
                supplier_addr = winning_info.xpath('.//td[@class="code-winningSupplierAddr"]/text()')[0]
            except IndexError:
                supplier_addr = ''
            try:
                review_score = winning_info.xpath('.//td[@class="code-reviewTotalScore"]/text()')[0]
            except IndexError:
                review_score = ''
            data['Title'].append(title)
            data['来源'].append(source_text)
            data['发布时间'].append(time_text)
            data['项目编号'].append(project_number)
            data['标项名称'].append(item_name)
            data['中标（成交金额）'].append(winning_amount)
            data['中标供应商名称'].append(supplier_name)
            data['中标供应商地址'].append(supplier_addr)
            data['评审总得分'].append(review_score)
            data['采购人名称'].append(buyer_name)
            data['采购人地址'].append(buyer_address)
            data['采购人联系方式'].append(buyer_contact)
            data['采购代理机构名称'].append(agency_name)
            data['采购代理机构地址'].append(agency_address)
            data['采购代理机构联系方式'].append(agency_contact)
            data['项目联系人'].append(contact_person)
            data['项目联系电话'].append(contact_phone)
    else:
        winning_infos = html.xpath('//td[contains(text(),"标项名称")]/../../tr[not(@class)]')
        if winning_infos:
            for winning_info in winning_infos:
                try:
                    winning_amount = winning_info.xpath('./td[3]/text()')[0]
                except IndexError:
                    winning_amount = ''
                try:
                    supplier_name = winning_info.xpath('./td[4]/text()')[0]
                except IndexError:
                    supplier_name = ''
                try:
                    supplier_addr = winning_info.xpath('./td[5]/text()')[0]
                except IndexError:
                    supplier_addr = ''
                review_score = ''
                data['Title'].append(title)
                data['来源'].append(source_text)
                data['发布时间'].append(time_text)
                data['项目编号'].append(project_number)
                data['标项名称'].append(item_name)
                data['中标（成交金额）'].append(winning_amount)
                data['中标供应商名称'].append(supplier_name)
                data['中标供应商地址'].append(supplier_addr)
                data['评审总得分'].append(review_score)
                data['采购人名称'].append(buyer_name)
                data['采购人地址'].append(buyer_address)
                data['采购人联系方式'].append(buyer_contact)
                data['采购代理机构名称'].append(agency_name)
                data['采购代理机构地址'].append(agency_address)
                data['采购代理机构联系方式'].append(agency_contact)
                data['项目联系人'].append(contact_person)
                data['项目联系电话'].append(contact_phone)
        else:
            data['Title'].append(title)
            data['来源'].append(source_text)
            data['发布时间'].append(time_text)
            data['项目编号'].append(project_number)
            data['标项名称'].append(item_name)
            data['中标（成交金额）'].append('')
            data['中标供应商名称'].append('')
            data['中标供应商地址'].append('')
            data['评审总得分'].append('')
            data['采购人名称'].append(buyer_name)
            data['采购人地址'].append(buyer_address)
            data['采购人联系方式'].append(buyer_contact)
            data['采购代理机构名称'].append(agency_name)
            data['采购代理机构地址'].append(agency_address)
            data['采购代理机构联系方式'].append(agency_contact)
            data['项目联系人'].append(contact_person)
            data['项目联系电话'].append(contact_phone)


def match_field_2(detail_result, html):
    title = detail_result['title']
    source_text = detail_result['author']
    time_text = timestamp_to_date(detail_result['publishDate'])
    project_number = detail_result['projectCode']
    item_name = title.replace('的中标公告', '')
    try:
        buyer_name = html.xpath('//span[contains(text(),"采购人：")]/text()')[0].replace('采购人：', '')
    except IndexError:
        buyer_name = ''
    try:
        buyer_address = html.xpath('(//table[@cellpadding="1"]//span[contains(text(),"地址：")])[1]/text()')[0].replace('地址：', '')
    except IndexError:
        buyer_address = ''
    try:
        buyer_contact = html.xpath('(//table[@cellpadding="1"]//span[contains(text(),"电话：")])[1]/text()')[0].replace('电话：', '')
    except IndexError:
        buyer_contact = ''
    try:
        agency_name = html.xpath('//span[contains(text(),"代理机构：")]/text()')[0].replace('代理机构：', '').replace('采购：', '')
    except IndexError:
        agency_name = ''
    try:
        agency_address = html.xpath('(//table[@cellpadding="1"]//span[contains(text(),"地址：")])[2]/text()')[0].replace('地址：', '')
    except IndexError:
        agency_address = ''
    try:
        agency_contact = html.xpath('(//table[@cellpadding="1"]//span[contains(text(),"电话：")])[2]/text()')[0].replace('电话：', '')
    except IndexError:
        agency_contact = ''
    contact_person = ''
    contact_phone = ''
    review_score = ''
    winning_info = html.xpath('//span[contains(text(),"供应商：") and contains(text(),"供应商地址：") and contains(text(),"中标金额：")]/text()')
    if winning_info:
        try:
            supplier_name = re.search(r"中标供应商：(.*?)，", winning_info[0]).group(1)
        except:
            supplier_name = ''
        try:
            supplier_addr = re.search(r"中标供应商地址：(.*?)，", winning_info[0]).group(1)
        except:
            supplier_addr = ''
        try:
            winning_amount = re.search(r"中标金额：(\d+(\.\d+)?)元", winning_info[0]).group(1)
        except:
            winning_amount = ''
    else:
        winning_info = html.xpath('//textarea[contains(text(),"供应商名称：") and contains(text(),"供应商地址：") and contains(text(),"中标金额：")]/text()')
        if winning_info:
            try:
                supplier_name = re.search(r"中标供应商名称：(.*?)，", winning_info[0]).group(1)
            except:
                supplier_name = ''
            try:
                supplier_addr = re.search(r"供应商地址：(.*?)，", winning_info[0]).group(1)
            except:
                supplier_addr = ''
            try:
                winning_amount = re.search(r"中标金额：(\d+(\.\d+)?)", winning_info[0]).group(1)
            except:
                winning_amount = ''
        else:
            supplier_name = ''
            supplier_addr = ''
            winning_amount = ''
    data['Title'].append(title)
    data['来源'].append(source_text)
    data['发布时间'].append(time_text)
    data['项目编号'].append(project_number)
    data['标项名称'].append(item_name)
    data['中标（成交金额）'].append(winning_amount)
    data['中标供应商名称'].append(supplier_name)
    data['中标供应商地址'].append(supplier_addr)
    data['评审总得分'].append(review_score)
    data['采购人名称'].append(buyer_name)
    data['采购人地址'].append(buyer_address)
    data['采购人联系方式'].append(buyer_contact)
    data['采购代理机构名称'].append(agency_name)
    data['采购代理机构地址'].append(agency_address)
    data['采购代理机构联系方式'].append(agency_contact)
    data['项目联系人'].append(contact_person)
    data['项目联系电话'].append(contact_phone)


def get_data(begin_time, end_time):
    data_json = {
        "keyword": "",
        "firstCode": "ZcyAnnouncement",
        "secondCode": "ZcyAnnouncement4",
        "districtCode": [],
        "pageSize": 15,
        "isTitleSearch": 1,
        "order": "desc",
        "leaf": "0"
    }
    url = f'https://www.zfcg.sh.gov.cn/portal/all'
    data_json["publishDateBegin"] = date_to_timestamp(begin_time)
    data_json["publishDateEnd"] = date_to_timestamp(end_time)
    data_json["pageNo"] = 1
    post_data = json.dumps(data_json)
    try:
        response = requests.post(url=url, data=post_data, headers=headers).json()
    except:
        try:
            response = requests.post(url=url, data=post_data, headers=headers).json()
        except:
            try:
                response = requests.post(url=url, data=post_data, headers=headers).json()
            except:
                pass
    data_num = response['result']['data']['total']
    page_num = data_num // 15
    for page in range(page_num):
        print(f'正在爬取{begin_time}-{end_time}数据, 共{page_num}页, 当前页数{page + 1}')
        data_json["pageNo"] = page + 1
        post_data = json.dumps(data_json)
        try:
            response = requests.post(url=url, data=post_data, headers=headers).json()
        except:
            try:
                response = requests.post(url=url, data=post_data, headers=headers).json()
            except:
                try:
                    response = requests.post(url=url, data=post_data, headers=headers).json()
                except:
                    pass
        results = response['result']['data']['data']
        for result in results:
            try:
                article_id = result['articleId']
            except:
                continue
            detail_url = f'https://www.zfcg.sh.gov.cn/portal/detail?articleId={urllib.parse.quote(article_id)}&parentId=137027&timestamp=1738767982'
            try:
                response = requests.get(detail_url, headers=headers)
            except:
                try:
                    response = requests.get(detail_url, headers=headers)
                except:
                    try:
                        response = requests.get(detail_url, headers=headers)
                    except:
                        pass
            detail_result = response.json()['result']['data']
            html = etree.HTML(detail_result['content'])
            title = detail_result['title']
            # 跳过失败公告
            if '失败' in title or title.endswith('成交公告'):
                print(f'跳过: {title}')
                continue
            print(f'https://www.zfcg.sh.gov.cn/site/detail?categoryCode=ZcyAnnouncement&parentId=137027&articleId={article_id}&utm=site.site-PC-39936.1045-pc-wsg-mainSearchPage-front.17.80230ff0e3d711efb95315a65a05fb7f')
            if html.xpath('//strong[contains(text(),"项目编号")]'):
                match_field_1(detail_result, html)
            elif html.xpath('//strong//span[text()="中标公告"]') or html.xpath('//strong//span[text()="成交公告"]'):
                match_field_2(detail_result, html)
            elif html.xpath('//strong//span[text()="失败公告"]'):
                print(f'跳过: {title}')
        df = pd.DataFrame(data)
        df.to_csv('上海政府采购网采购结果公告.csv', encoding='utf-8-sig', index=False)


def date_to_timestamp(date_str):
    """
    将时间字符串（格式为YYYY-MM-DD）转换为时间戳（秒级）。
    """
    # 将字符串 解析为datetime对象
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    # 转换为时间戳（秒级）
    timestamp = int(dt.timestamp())
    return timestamp * 1000


def timestamp_to_date(timestamp_ms):
    """
    将毫秒级时间戳转换为日期字符串（格式为YYYY-MM-DD）。
    """
    # 将毫秒级时间戳转换为秒级
    timestamp = timestamp_ms / 1000.0
    # 将时间戳转换为datetime对象
    dt = datetime.fromtimestamp(timestamp)
    # 格式化为日期字符串
    date_str = dt.strftime("%Y-%m-%d")
    return date_str


def get_month_start_end(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        # 获取当月的第一天
        month_start = current_date.replace(day=1)
        # 获取下个月的第一天
        if current_date.month == 12:
            next_month_start = current_date.replace(year=current_date.year + 1, month=1, day=1)
        else:
            next_month_start = current_date.replace(month=current_date.month + 1, day=1)
        # 当月的最后一天是下个月第一天的前一天
        month_end = next_month_start - timedelta(days=1)

        get_data(month_start.strftime('%Y-%m-%d'), month_end.strftime('%Y-%m-%d'))

        # 更新当前日期为下个月的第一天
        current_date = next_month_start


if __name__ == '__main__':
    # 设置开始时间和结束时间
    end_date = datetime(2025, 2, 6)
    # 调用函数
    get_month_start_end(start_date, end_date)
