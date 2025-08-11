import time
import re
from DrissionPage import ChromiumPage
import pandas as pd

username = '5190007100000'
password = 'Xyd+123456'

# 跳过批量添加True false
tiaoguo = False
# 文件名
file_name = '逾限时长-明细表20250621(2).xls'
# 读取个数
read_num = 3000
# 异常种类
error_type = '中转处理邮件类劣三类'
# 异常小类
size_type = '规格类'
# 通知对象
msg_obj = '52840100'

def find_ele_safe(page, xpath):
    try:
        return page.ele(f'xpath:{xpath}', timeout=3)
    except:
        print(f'未找到{xpath}')


# 创建页面对象
page = ChromiumPage()
page.get('https://10.4.188.1/cas/login?service=https://10.4.188.1/portal/a/cas&t=')
page.wait.load_start()
input('手动操作')
page.get('https://10.4.188.1/monitor-web/a/monitor/abnormalitysubmitandquery/tolist')
page.wait.load_start()
if not tiaoguo:
    page.ele('xpath://*[@id="btnBatchAdd"]').click()
    page.wait.load_start()
    # 填写异常种类
    page.ele('xpath://*[contains(@class,"select2-container input-xlarge")]//*[@class="select2-chosen"]').click()
    page.ele(f'xpath://*[@class="select2-result-label" and contains(text(),"{error_type}")]').click()
    # 读取并填写单号
    df = pd.read_excel(file_name)
    time.sleep(1)
    for index, row in df.iterrows():
        if index == read_num:
            break
        page.ele('xpath://*[@name="billNoOne"]').input(f'{row["邮件条码"]}\n')
        tip = find_ele_safe(page, '//*[@id="jbox-content"]')
        if tip:
            page.ele('xpath://button[text()="确定"]').click()
            page.ele('xpath://*[@name="billNoOne"]').clear()
            print(f'行{index}  邮件条码：{row["邮件条码"]}, 单号已存在')
        else:
            print(f'行{index}  邮件条码：{row["邮件条码"]}')
    page.ele('xpath://*[@value="保 存"]').click()
    time.sleep(1)
    page.get('https://10.4.188.1/monitor-web/a/monitor/abnormalitysubmitandquery/tolist')
    page.wait.load_start()
# 选择异常小类
page.ele('xpath://label[contains(text(),"异常小类")]/following-sibling::div//*[@class="select2-chosen"]').click()
page.ele(f'xpath://*[@class="select2-result-label" and contains(text(),"{size_type}")]').click()
# 选择未发验
page.ele('xpath://label[contains(text(),"发验状态")]/following-sibling::div//*[@class="select2-chosen"]').click()
page.ele('xpath://*[@class="select2-result-label" and contains(text(),"未发验")]').click()
page.ele('xpath://*[@id="btnSubmit"]').click()
time.sleep(1)
while find_ele_safe(page, '//*[@id="contentTable"]//tbody/tr[1]'):
    page.get_frame(0)
    page.ele('xpath://input[@name="allCheck"]').click()
    page.ele('xpath://input[@id="sendRecord1"]').click()
    try:
        page.ele('xpath://*[@class="jbox-container"]//*[text()="确定"]', timeout=5).click()
    except:
        page.ele('xpath://input[@id="sendRecord1"]').click()
        page.ele('xpath://*[@class="jbox-container"]//*[text()="确定"]', timeout=5).click()
    time.sleep(2)
    hint = page.ele('xpath://*[@class="jbox-container"]', timeout=5).text
    print(f'弹窗内容：{hint}')
    if '发出局为自动发验机构，无需手动发验' in hint:
        input('手动处理无需手动发验的单号')
    elif '成功发验' in hint:
        continue
    elif '其中失败0条' not in hint:
        error_num = (re.search(r'其中失败(\d+)条', hint).group(1))
        page.ele('xpath://*[@class="jbox-container"]//*[text()="确定"]', timeout=5).click()
        time.sleep(2)
        for i in range(int(error_num)):
            print(f'开始修改第{i+1}个, 共{error_num}条')
            page.get_frame(0, timeout=0)
            page.ele(f'xpath://*[@id="contentTable"]//tbody/tr[{i+1}]//*[@value="修改"]').click()
            page.get_frame('xpath://*[@name="jbox-iframe"]')
            # 选择通知对象
            page.ele('xpath://label[contains(text(),"通知对象")]/following-sibling::div//*[@class="select2-chosen"]').click()
            page.ele('xpath://*[@id="select2-drop"]//input').input(msg_obj)
            page.ele('xpath://*[@class="select2-results"]//li[1]/div').click()
            # 输入总包号
            post_num = page.ele('xpath://label[contains(text(),"邮件号")]/following-sibling::input').value
            page.ele('xpath://label[contains(text(),"总包号")]/following-sibling::input').clear()
            page.ele('xpath://label[contains(text(),"总包号")]/following-sibling::input').input(post_num)
            # 保存
            page.ele('xpath://*[@value="保 存"]').click()
            page.ele('xpath://*[@id="id_close"]').click()
            page.wait.load_start()
        # 错误发验
        for i in range(int(error_num)):
            page.ele(f'xpath://*[@id="contentTable"]//tbody/tr[{i+1}]/td[1]/input').click()
        page.ele('xpath://input[@id="sendRecord1"]').click()
        try:
            page.ele('xpath://*[@class="jbox-container"]//*[text()="确定"]', timeout=5).click()
        except:
            page.ele('xpath://input[@id="sendRecord1"]').click()
            page.ele('xpath://*[@class="jbox-container"]//*[text()="确定"]', timeout=5).click()
        time.sleep(2)
        hint = page.ele('xpath://*[@class="jbox-container"]', timeout=5).text
        print(f'弹窗内容：{hint}')
        page.ele('xpath://*[@class="jbox-container"]//*[text()="确定"]', timeout=5).click()
        time.sleep(2)
print('结束')