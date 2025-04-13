import pandas as pd
import requests
import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

data = {
    '001': {
        '编号': [],
        '时间': [],
        '比分': [],
        '总进球': [],
        '全半场胜负平': [],
    },
    '002': {
        '编号': [],
        '时间': [],
        '比分': [],
        '总进球': [],
        '全半场胜负平': [],
    },
    '003': {
        '编号': [],
        '时间': [],
        '比分': [],
        '总进球': [],
        '全半场胜负平': [],
    },
    '004': {
        '编号': [],
        '时间': [],
        '比分': [],
        '总进球': [],
        '全半场胜负平': [],
    },
    '005': {
        '编号': [],
        '时间': [],
        '比分': [],
        '总进球': [],
        '全半场胜负平': [],
    },
}


def get_month_start_end(year, month):
    start_date = datetime.date(year, month, 1)
    if month == 12:
        next_month = datetime.date(year + 1, 1, 1)
    else:
        next_month = datetime.date(year, month + 1, 1)
    end_date = next_month - datetime.timedelta(days=1)
    return start_date, end_date

if __name__ == '__main__':
    # for year in range(2019, 2025):
    #     for month in range(1, 13):
    #         begin_date, end_date = get_month_start_end(year, month)
    begin_date = '2025-01-01'
    end_date = '2025-01-20'
    print(f"开始时间: {begin_date}, 结束时间: {end_date}")
    url = f'https://webapi.sporttery.cn/gateway/uniform/football/getUniformMatchResultV1.qry?matchBeginDate={begin_date}&matchEndDate={end_date}&leagueId=&pageSize=100&pageNo=2&isFix=0&matchPage=1&pcOrWap=1'
    try:
        r = requests.get(url, headers=headers).json()
    except:
        try:
            r = requests.get(url, headers=headers).json()
        except:
            r = requests.get(url, headers=headers).json()
    data_num = int(r['value']['total'])
    if data_num != 0:
        pages = data_num // 100 + 1
        for page in range(pages):
            url = f'https://webapi.sporttery.cn/gateway/uniform/football/getUniformMatchResultV1.qry?matchBeginDate={begin_date}&matchEndDate={end_date}&leagueId=&pageSize=100&pageNo={page + 1}&isFix=0&matchPage=1&pcOrWap=1'
            try:
                r = requests.get(url, headers=headers).json()
            except:
                try:
                    r = requests.get(url, headers=headers).json()
                except:
                    r = requests.get(url, headers=headers).json()
            matchs = r['value']['matchResult']
            for match in matchs:
                number = match['matchNumStr']
                if not ('001' in number or '002' in number or '003' in number or '004' in number or '005' in number):
                    continue
                match_time = match['matchDate']
                match_id = match['matchId']
                url = f'https://webapi.sporttery.cn/gateway/uniform/football/getFixedBonusV1.qry?clientCode=3001&matchId={match_id}'
                try:
                    r = requests.get(url, headers=headers).json()
                except:
                    try:
                        r = requests.get(url, headers=headers).json()
                    except:
                        r = requests.get(url, headers=headers).json()
                score = total_goals = win_or_lose = ''
                for result in r['value']['matchResultList']:
                    if result['code'] == 'CRS':
                        score = result['combinationDesc']
                    if result['code'] == 'TTG':
                        total_goals = result['combinationDesc']
                    if result['code'] == 'HAFU':
                        win_or_lose = result['combinationDesc']
                if score == '' or total_goals == '' or win_or_lose == '':
                    print()
                print(f'{number}   {match_time}   {score}   {total_goals}   {win_or_lose}, 总共{data_num}条数据, 正在爬取第{page * 100 + matchs.index(match) + 1}条')
                num = number[-3:]
                data[num]['编号'].append(number)
                data[num]['时间'].append(match_time)
                data[num]['比分'].append(score)
                data[num]['总进球'].append(total_goals)
                data[num]['全半场胜负平'].append(win_or_lose)
        for num in ['001', '002', '003', '004', '005']:
            df = pd.DataFrame(data[num])
            df = df.sort_values(by='时间')
            df.to_excel(f'{num}_____.xlsx', index=False)