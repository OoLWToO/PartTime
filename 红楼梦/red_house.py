import requests
from lxml import etree

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",

    "Cookie": "BIDUPSID=327D0334B7461679153D654034AD62D1; PSTM=1730450560; BAIDUID=327D0334B746167947D3220192778E9E:FG=1; H_PS_PSSID=61027_61243_61246_60853_61359_61368_61391_61392_61444_61429_61509_61504_61529_61497; BAIDUID_BFESS=327D0334B746167947D3220192778E9E:FG=1; ZFY=LEKA8z8xy0SLYuQilD6GKNIuR7ueOJ0RZXH1xVgyH:AI:C; ab_sr=1.0.1_NWE3ZDA4YmIzZmU0MmYzMjc0YTE0MDY3YjBkYzAwZTgwNjRiOTgyMjEzNmZkODFmYjNhNTBmZjJjNWYwNjBlODk0N2JjZmU4YjA3NzI5NGM2YjNiNTc2YTExZDFiYTkzMDM3MDU3MTgyZThlMWRlODU2OWNjOWEzMWVmMzE2YjFkNTIwMDZhYzUzMjMzYjM2M2I1MTgyNjZhZDUwODBjNQ==",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}


if __name__ == '__main__':
    url = 'https://baijiahao.baidu.com/s?id=1794650367122142272'
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    html = etree.HTML(r.text)
    html.xpath('//*[@class="dpu8C _2kCxD "]/p[./strong//*[contains(text(),".")]]')
    print(html)
