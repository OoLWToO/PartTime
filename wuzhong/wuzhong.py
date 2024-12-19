import pandas as pd
import requests

# 设置请求头，用于模拟用户真实请求
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Cookie': '__jsluid_s=c9bf2381199315a3f9d70fab5efbea9b; __jsl_clearance_s=1718590950.375|0|BNVMH65p0N9580f3nELVxfBlj1g%3D; PHPSESSID=mnnnrrlijttt606feek3bkdvg0; mfw_uuid=666f9de7-be92-5b8a-42db-f09d461618a6; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222024-06-17+10%3A22%3A31%22%3B%7D; __mfwc=direct; __mfwa=1718590951232.55084.1.1718590951232.1718590951232; __mfwlv=1718590951; __mfwvn=1; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1718590951; uva=s%3A150%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1718590952%3Bs%3A10%3A%22last_refer%22%3Bs%3A82%3A%22https%3A%2F%2Fwww.mafengwo.cn%2Flocaldeals%2F0-0-M10132-0-0-0-0-0.html%3Ffrom%3Dlocaldeals_index%22%3Bs%3A5%3A%22rhost%22%3BN%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1718590952%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=666f9de7-be92-5b8a-42db-f09d461618a6; __mfwb=7d6d46205828.2.direct; __mfwlt=1718590972; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1718590973; bottom_ad_status=0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

if __name__ == '__main__':
    # 读取xlsx文件可能要10秒左右
    df = pd.read_excel('occurrence.xlsx', index_col=None)
    rows = 137
    # 循环表格中所有数据，如果爬取中断就从指定行开始爬取，如下所示从2000行开始爬取
    for name in df['scientificName'][137:]:
    # for name in df['scientificName']:
        # 详细信息url，设置%s占位符
        detail_url = 'https://api.checklistbank.org/dataset/296511/taxon/%s/info'
        # 详细页url，用于对比数据是否正确
        web_url = 'https://www.catalogueoflife.org/data/taxon/%s'
        # 请求搜索api
        url = f'https://api.checklistbank.org/dataset/296511/nameusage/suggest?fuzzy=false&limit=25&q={name}'
        r1 = requests.get(url, headers=headers).json()
        # 检查是否有status为accepted的元素
        accepted_suggestion = next((suggestion for suggestion in r1['suggestions'] if suggestion.get('status') == 'accepted'), None)

        if accepted_suggestion:
            u_id = accepted_suggestion.get('acceptedUsageId', accepted_suggestion.get('usageId'))
        else:
            u_id = r1['suggestions'][0].get('acceptedUsageId', r1['suggestions'][0].get('usageId'))

        detail_url = detail_url % u_id
        web_url = web_url % u_id

        # 输出web_url，方便比较数据是否正确
        print(web_url)
        r2 = requests.get(detail_url, headers=headers).json()
        # 请求到的类别数组是乱序的，循环找到对应的rank
        for classification in r2['classification']:
            if classification['rank'] == 'kingdom':
                df.at[rows, 'kingdom'] = classification['label']
            if classification['rank'] == 'phylum':
                df.at[rows, 'phylum'] = classification['label']
            if classification['rank'] == 'class':
                df.at[rows, 'class'] = classification['label']
            if classification['rank'] == 'order':
                df.at[rows, 'order'] = classification['label']
            if classification['rank'] == 'family':
                df.at[rows, 'family'] = classification['label']
            if classification['rank'] == 'genus':
                df.at[rows, 'genus'] = classification['label']
        df.at[rows, 'species'] = r2['usage']['label']
        print(f'{rows}  {name}  {df.at[rows, "kingdom"]}  {df.at[rows, "phylum"]}  {df.at[rows, "class"]}  {df.at[rows, "order"]}  {df.at[rows, "family"]}  {df.at[rows, "genus"]}  {df.at[rows, "species"]}')
        rows += 1
        # 每爬取1000行数据就存入一次表格，避免在爬取过程中出现网络问题导致中断后数据未保存
        # if rows % 1000 == 0:
        df.to_excel('occurrence.xlsx', index=False)
        print()
