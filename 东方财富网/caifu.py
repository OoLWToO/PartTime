import pandas as pd
import requests
import json

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "st_si=47120769641646; st_asi=delete; qgqp_b_id=de4bbf0f3f78559d07de4346fe9a055c; st_pvi=20220114071583; st_sp=2024-12-27%2010%3A17%3A38; st_inirUrl=; st_sn=4; st_psi=20241227103140192-113300300976-2288335046; JSESSIONID=311EB0BE8DE82407B39AABCBFC14150F",
    "Host": "datacenter-web.eastmoney.com",
    "Referer": "https://data.eastmoney.com/gdhs/",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "script",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

data = {
    '代码': [],
    '名称': [],
    '股东户数(本次)': [],
    '股东户数(上次)': [],
    '股东户数(增减)': [],
    '股东户数(增减比例)': [],
    '区间涨跌幅': [],
    '户均持股市值(万)': [],
    '户均持股数量(万)': [],
    '总市值(亿)': [],
    '总股本(亿)': [],
    '公告日期': [],
}

def get_data(date):
    url = 'https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112308810524360467862_1735266699917&sortColumns=HOLD_NOTICE_DATE%2CSECURITY_CODE&sortTypes=-1%2C-1&pageSize=300&pageNumber=1&reportName=RPT_HOLDERNUMLATEST&columns=SECURITY_CODE%2CSECURITY_NAME_ABBR%2CEND_DATE%2CINTERVAL_CHRATE%2CAVG_MARKET_CAP%2CAVG_HOLD_NUM%2CTOTAL_MARKET_CAP%2CTOTAL_A_SHARES%2CHOLD_NOTICE_DATE%2CHOLDER_NUM%2CPRE_HOLDER_NUM%2CHOLDER_NUM_CHANGE%2CHOLDER_NUM_RATIO%2CEND_DATE%2CPRE_END_DATE&quoteColumns=f2%2Cf3&quoteType=0&source=WEB&client=WEB'
    r = requests.get(url, headers=headers)
    stock_list = json.loads((r.text[r.text.find('(') + 1:r.text.find(')')]))['result']['data']
    for stock in stock_list:
        code = stock['SECURITY_CODE']
        name = stock['SECURITY_NAME_ABBR']
        holder_num = stock['HOLDER_NUM']
        pre_holder_num = stock['PRE_HOLDER_NUM']
        holder_num_change = stock['HOLDER_NUM_CHANGE']
        holder_num_ratio = round(stock['HOLDER_NUM_RATIO'], 2)
        interval_chrate = round(stock['INTERVAL_CHRATE'], 2)
        avg_market_cap = round(stock['AVG_MARKET_CAP'] / 10000, 2)
        avg_hold_num = round(stock['AVG_HOLD_NUM'] / 10000, 2)
        total_market_cap = round(stock['TOTAL_MARKET_CAP'] / 100000000, 2)
        total_a_shares = round(stock['TOTAL_A_SHARES'] / 100000000, 2)
        hold_notice_date = stock['HOLD_NOTICE_DATE'][:10]
        if hold_notice_date < date:
            continue
        print(f'{code}   {name}   {holder_num}   {pre_holder_num}   {holder_num_change}   {holder_num_ratio}   '
              f'{interval_chrate}   {avg_market_cap}   {avg_hold_num}   {total_market_cap}   {total_a_shares}   {hold_notice_date}')
        data['代码'].append(code)
        data['名称'].append(name)
        data['股东户数(本次)'].append(holder_num)
        data['股东户数(上次)'].append(pre_holder_num)
        data['股东户数(增减)'].append(holder_num_change)
        data['股东户数(增减比例)'].append(holder_num_ratio)
        data['区间涨跌幅'].append(interval_chrate)
        data['户均持股市值(万)'].append(avg_market_cap)
        data['户均持股数量(万)'].append(avg_hold_num)
        data['总市值(亿)'].append(total_market_cap)
        data['总股本(亿)'].append(total_a_shares)
        data['公告日期'].append(hold_notice_date)
    df = pd.DataFrame(data)
    df.to_excel(f'东方财富网股东户数数据.xlsx', index=False)

if __name__ == '__main__':
    get_data('2024-12-26')
