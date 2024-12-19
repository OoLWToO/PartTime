import base64
import io
import time

import pandas as pd
from PIL import Image as PILImage
from openpyxl.drawing.image import Image as ExcelImage
import requests
from lxml import etree

headers = {
    'cookie': 'uuid_tt_dd=10_20289225050-1712579300113-806402; UserName=weixin_53739903; UserInfo=1fd9be78046c4363bb683ed3997916c1; UserToken=1fd9be78046c4363bb683ed3997916c1; UserNick=OoLWToO; AU=61D; UN=weixin_53739903; BT=1712580151959; p_uid=U010000; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22weixin_53739903%22%2C%22scope%22%3A1%7D%7D; dc_sid=afc97094252011ae932c8ce130e748c0; c_segment=2; c_dl_prid=1712591840139_733152; c_dl_rid=1719308357671_747450; c_dl_fref=default; c_dl_fpage=/download/liyupinglj/10941894; c_dl_um=-; FCNEC=%5B%5B%22AKsRol_1YLx6mNDN24T6WcdofYc95nFyjMVPGkIOXfeZbQRZo0giG86DWaACKSlFnXA4dV46rq3s-_cWutW-WZwDJ38FU-sPxfVkk0eyrapnuhU1xkZ6rmJTJe96TavZ-mEmDQx_JsWhGZ55-Z9oRVyFBqq__5NECA%3D%3D%22%5D%5D; _clck=1w00wox%7C2%7Cfn3%7C0%7C1559; __gads=ID=7411a952d94bdee4:T=1712580165:RT=1719825156:S=ALNI_MY-xoz5pv5tEGz1ZozW0tR1l_sFSA; __gpi=UID=00000de42d605433:T=1712580165:RT=1719825156:S=ALNI_MYgZSqu9f4r4pu_7KmI5snA7syBDQ; __eoi=ID=d3d2b6d2db7edea4:T=1712580165:RT=1719825156:S=AA-AfjaEvjtATzB5pn0HhxxA2rFG; dc_session_id=10_1721113956602.503978; c_pref=default; c_first_ref=default; c_first_page=https%3A//www.csdn.net/; c_dsid=11_1721113956021.223167; c_page_id=default; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=; HMACCOUNT=985C1AF64BC5565E; https_waf_cookie=9db7097a-5b95-43412374ec103329197ccc9bcad68f62c0d3; c_ref=https%3A//www.csdn.net/; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1721113963; fe_request_id=1721113962935_3527_5359451; log_Id_pv=153; dc_tos=sgpg17; log_Id_click=334; log_Id_view=7488',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

data = {
    'number': [],
    'Name': [],
    'CAS_no': [],
    'Mol.formula': []
}

if __name__ == '__main__':
    start = 150
    # start_num = 570
    end = 100
    for i in range(start, 164):
        # n = start_num if i == start else 0
        code1 = '{:0>3}'.format(i)
        url = f'https://echa.europa.eu/substance-information/-/substanceinfo/100.{code1}.000'
        print(url)
        try:
            r = requests.get(url, headers=headers, timeout=10)
        except:
            try:
                r = requests.get(url, headers=headers, timeout=10)
            except:
                continue
        time.sleep(.5)
        html = etree.HTML(r.text)
        try:
            if len(html.xpath('//*[@class="noInfocard"]')) > 0 or html.xpath('//*[@class="lead"]'):
                name = html.xpath('//*[@class="noInfocard"]/h2/text()')[0].replace('\n', '').replace('\t', '')
                if 'not yet' in name or 'No public' in name:
                    continue
            else:
                name = html.xpath('//*[@class="hasInfocard"]/h2/text()')[0].replace('\n', '').replace('\t', '')
                if 'not yet' in name or 'No public' in name:
                    continue
        except:
            continue
        try:
            cas_no = \
                html.xpath(
                    '//*[@class="TooltipInline" and contains(text(),"CAS")]/../following-sibling::span/text()')[
                    0]
        except:
            cas_no = ''
        try:
            mol_folmula = html.xpath('//*[@class="TooltipInline" and contains(text(),"formula")]/../../text()')[
                0]
        except:
            mol_folmula = ''
        print(f'{code1}000   {name}   {cas_no}   {mol_folmula}')
        data['number'].append(f'{code1}000')
        data['Name'].append(name)
        data['CAS_no'].append(cas_no)
        data['Mol.formula'].append(mol_folmula)
        df = pd.DataFrame(data)
        code1 = '{:0>3}'.format(start)
        df.to_excel(f'substance补充.xlsx', index=False)
