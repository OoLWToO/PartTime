import json

import requests
import base64

search_url = 'https://etax.guangdong.chinatax.gov.cn:8443/szc/szzh/sjswszzh/zhcx/v1/DescribeSbmxcx2'
detail_url = 'https://etax.liaoning.chinatax.gov.cn:8443/szc/szzh/sjswszzh/zhcx/v1/exportSbmxxqcx'
sub_table_list_url = 'https://etax.guangdong.chinatax.gov.cn:8443/szc/szzh/sjswszzh/zhcx/v1/DescribeSbmxxqzfbTree'
url = 'https://etax.anhui.chinatax.gov.cn:8443/szc/szzh/sbss/ssmx/zlbs/v1/queryZlbscjb'

headers = {
    "Host": "etax.anhui.chinatax.gov.cn:8443",
    "Origin": "https://etax.anhui.chinatax.gov.cn:8443",
    "Accept": "application/json;charset=UTF-8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Connection": "keep-alive",
    "Content-Length": "231",
    "Content-Type": "application/json",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Referer": "https://etax.anhui.chinatax.gov.cn:8443/szc/szzh/sbss/view/",
    "Cookie": "tpass_vw5vafc9w7dd4e9e9w8d5vbc66889d55=eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6ImExM2ViMzcwYTFmMDQ0ZGRiYmIyNzMzN2UzNmYyNTNhIn0.eG8fYdv_RvmnnGHGK35C8H8CS8uMvSL845ZA4CRU1fxACr4M6mjgu-VuxoTtomHcwCHfVeDRiMAteouEXY3eLg;ZNHD_SECURITY_CHECK_TOKEN=4d5ddc9e3c2b4e6aa9a9b4baceca985f;znhd-ssotoken=6086df398ee942e6adb582848300a275;sl-session=yU2FNC00XWf6LjmZcSWSAw==;tpass_n7b7ecp5696hna6f969b22pacch966nn=eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6Ijc2OGYxMmQ1MDJhODRlZTg5MWYxOGY5NWVlYzUyOTJmIn0.QDRHB4mWnwCGXXaPeMJqqU4ZTBhH05qkpPw1SLv4Zie2GeYgN_X00lY7QVYNgrqA1m7_Qoy34icxC_z2vG9K4g;sajssdk_2015_cross_new_user=1;oauth2_referer=etax.anhui.chinatax.gov.cn;sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22193beef84ab581-06cce3464dad8bc-12462c6f-1387200-193beef84aca19%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkzYmVlZjg0YWI1ODEtMDZjY2UzNDY0ZGFkOGJjLTEyNDYyYzZmLTEzODcyMDAtMTkzYmVlZjg0YWNhMTkifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22193beef84ab581-06cce3464dad8bc-12462c6f-1387200-193beef84aca19%22%7D"
}

json_j = {
    "ZlbsxlDm": "",
    "Lrrqq": "",
    "Lrrqz": "",
    "Skssqq": "2024-01-01",
    "Skssqz": "2024-12-31",
    "PageNum": 1,
    "PageSize": 50
}

search_data = json.dumps(json_j)
response = requests.post(url=url, data=search_data, headers=headers)
response.encoding = 'GBK'
print()

# data = {
#     "exportParam": [],
#     "reportIdList": [
#         "BDA0610611",
#         "BDA0610612",
#         "BDA0610613",
#         "BDA0610759"
#     ],
#     "sbuuid": "7EC0DF6721881F5246EA0E7F626A5723",
#     "skssqq": "2024-07-01",
#     "skssqz": "2024-09-30",
#     "zbdzbzdsDm": "BDA0610611",
#     "djxh": "",
#     "sbrq": "2024-10-12"
# }
#
# data = '{"exportParam":[],"reportIdList":["BDA0610611","BDA0610612","BDA0610613","BDA0610759"],"sbuuid":"69F88862ADCB108117BA71CA0D3F15DD","skssqq":"2023-07-01","skssqz":"2023-09-30","zbdzbzdsDm":"BDA0610611","djxh":"","sbrq":"2023-10-21"}'
# response = requests.post(detail_url, data=data, headers=headers)
#
# base64_data = response.json()['Response']['Data'][0]['pdfStr']
# pdf_data = base64.b64decode(base64_data)
#
# with open('E:\增值税5.pdf', 'wb') as pdf_file:
#     pdf_file.write(pdf_data)


print(response.text)
