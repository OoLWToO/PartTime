import os

import pandas as pd
import requests
from lxml import etree
from matplotlib import pyplot as plt

request_headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "channelcode": "pcKaoyan2",
    "cookie": "duid=5759851817875757805; BOOK_TOKEN_=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJPcmdDb2RlIjoic21hcnRkZW1va3JzIiwibmJmIjoxNzM1NjQ5NzI3LCJleHAiOjE3MzU2NTY5MjcsImlzcyI6IlNtYXJ0TGlicmFyeS5JZGVudGl0eUNlbnRlciIsImF1ZCI6IldlYkFwaSJ9.BBAWo1MaBK_H9wqoSE_DxTB2dSZQxeSpv17M19_mUgL0RWKEqH41IA2ov3ZlaE7nItAZLJ9S_SWEx89pxO5RpZXFMMt76hnMa1X-0RTwLtl92iVtcuNNVyNh-fJfYfRC58mgD4u1KrVOw6AgB-lMpqswVTlvMobRLQ6CaBD1e0IsXFhVSrEFPhN8kaKZGLMFAWwxr9fC7_0KmpiqAVhNHBgwqLe-QtmDWYBUKbo6Sjs2TCDWp924OOtDgapIVxyOoIu8QOrxkhIkL1PzIUniLZE_LNHW0L40oVYx_723jy_QR8E73MiEEXtL9eWsBuDogh48ZzxVsDCJLpIKbx_KVQ; Hm_lvt_04dac094451c2f9591092e758fc05936=1734854971,1734960517,1735569522,1735649733; Hm_lpvt_04dac094451c2f9591092e758fc05936=1735649733; HMACCOUNT=53BEF1F68DC70C31",
    "dt": "pc",
    "ht": "kaoyan.cqvip.com",
    "platform": "PCkaoyan",
    "priority": "u=1, i",
    "referer": "https://kaoyan.cqvip.com/info/school?d=2&y=&s=&x=&t=&z=",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "test": "false",
    "timestamp": "1735649737117",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

data = {
    '学校名称': [],
    '所在地区': [],
    '创建时间': [],
    '院校隶属': [],
    '占地面积': [],
    '学校地址': [],
    '是否为985': [],
    '是否为211': [],
    '所属院系': [],
    '招生年份': [],
    '学习方式': [],
    '考试方式': [],
    '计划招生人数': [],
    '所属门类': [],
    '所属一级学科': [],
    '学位类型': [],
    '专业代码': [],
    '专业名称': [],
    '总分': [],
    '政治': [],
    '英语': [],
    '专业课一': [],
    '专业课二': [],
}


def create_chart(classify, subject, score_list):
    table_name = f'{classify}学校{subject}专业分数线分布条形图'
    item = []
    value = []
    for d in score_list:
        if str(d) in item:
            index = item.index(str(d))
            value[index] += 1
        else:
            item.append(str(d))
            value.append(1)
    if len(item) < 3 or len(value) < 3:
        return
    sorted_pairs = sorted(zip(item, value), key=lambda pair: pair[0])
    sorted_items, sorted_values = zip(*sorted_pairs)
    plt.close('all')
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(6, 6))
    plt.xticks(rotation=45)
    plt.bar(sorted_items, sorted_values)
    plt.title(f'{table_name}')
    plt.xlabel('分数')
    plt.ylabel('数量')
    plt.savefig(f'图片/{table_name}')


def get_subject_list(search_list, degreeType):
    subject_list = []
    for search_content in search_list:
        code_search_url = f'http://kaoyan.cqvip.com/api/kaoyan/info/major/page?current=1&name={search_content}&majorType=2&degreeType={degreeType}&size=100'
        r = requests.get(code_search_url, headers=request_headers)
        records = r.json()['data']['records']
        for record in records:
            # 专业代码中包含'Z'的为自定义专业, 不查询
            if 'Z' not in record['code']:
                subject_list.append(record)
    return subject_list


def get_data(search_list, degreeType):
    score_hebei = {}
    score_beijing = {}
    score_jiangsu = {}
    score_985 = {}
    score_211 = {}
    subject_list = get_subject_list(search_list, degreeType)
    for subject in subject_list:
        school_search_url = f'http://kaoyan.cqvip.com/api/kaoyan/info/major/schoolInfo?current=1&size=1000&majorId={subject["id"]}'
        r = requests.get(school_search_url, headers=request_headers)
        school_list = r.json()['data']['records']
        for school in school_list:
            schoolId = school['schoolId']
            collegeId = school['collegeId']
            # 获取学校基础信息: 学校名称、创建时间、院校隶属、占地面积、学校地址
            school_url = f'http://kaoyan.cqvip.com/school/{schoolId}'
            r = requests.get(school_url, headers=request_headers)
            html = etree.HTML(r.text)
            school_xpath = '//*[@class="basic f-c-second"]//div[./span[text()="{}"]]/text()'
            school_name = html.xpath('//*[@class="title mr-83"]/text()')[0]
            school_creation_time = html.xpath(school_xpath.format('创建时间'))[0].replace(' ', '').replace('\n', '').replace(':', '')
            school_affiliation = html.xpath(school_xpath.format('院校隶属'))[0].replace(' ', '').replace('\n', '').replace(':', '')
            school_floor_space = html.xpath(school_xpath.format('占地面积'))[0].replace(' ', '').replace('\n', '').replace(':', '')
            school_address = html.xpath(school_xpath.format('学校地址'))[0].replace(' ', '').replace('\n', '').replace(':', '')
            # 获取位置用于统计
            position = html.xpath('//*[@class="title mr-83"]/following-sibling::small/text()')[0]
            is_985 = '是' if html.xpath('//*[@class="label-container xy-start mb-83"]/div[contains(text(),"985")]') else '否'
            is_211 = '是' if html.xpath('//*[@class="label-container xy-start mb-83"]/div[contains(text(),"211")]') else '否'
            if position not in ['河北', '北京', '江苏'] or (is_985 != '否' and is_211 != '否'):
                continue

            # 获取专业介绍: 所属院系、招生年份、学习方式、考试方式、计划招生人数、所属门类、所属一级学科
            subject_xpath = '//*[@class="title bold" and contains(text(),"{}")]/following-sibling::span/@title'
            subject_url = f'http://kaoyan.cqvip.com/school/{schoolId}/introduce/{subject["id"]}/{collegeId}?year=2024'
            r = requests.get(subject_url, headers=request_headers)
            html = etree.HTML(r.text)
            subject_affiliation = html.xpath(subject_xpath.format('所属院系'))[0]
            subject_enrollment_year = html.xpath(subject_xpath.format('招生年份'))[0]
            subject_learning_style = html.xpath(subject_xpath.format('学习方式'))[0]
            subject_exam_method = html.xpath(subject_xpath.format('考试方式'))[0]
            subject_enrollment_num = html.xpath(subject_xpath.format('计划招生人数'))[0]
            subject_category = html.xpath(subject_xpath.format('所属门类'))[0]
            subject_discipline = html.xpath(subject_xpath.format('所属一级学科'))[0]

            # 获取分数线: 学位类型、专业代码、专业名称、总分、政治、英语、专业课一、专业课二
            score_line_url = f'http://kaoyan.cqvip.com/api/kaoyan/info/reExamination/academic-years-scoreline?current=1&size=1000&schoolIds={schoolId}&year=2024'
            r = requests.get(score_line_url, headers=request_headers)
            score_line_list = r.json()['data']['records']
            for score_line in score_line_list:
                if score_line['majorCode'] == subject['code']:
                    degree_type = score_line['majorType']
                    subject_code = score_line['majorCode']
                    subject_name = score_line['majorName']
                    total_score = score_line['totalScore']
                    politics = score_line['politicsScore']
                    english = score_line['englishScore']
                    course_one_score = score_line['courseOneScore']
                    course_two_score = score_line['courseTwoScore']
                    print(f'{school_name}   {school_creation_time}   {school_affiliation}   {school_floor_space}   {school_address}   '
                          f'{subject_affiliation}   {subject_enrollment_year}   {subject_learning_style}   {subject_exam_method}   '
                          f'{subject_enrollment_num}   {subject_category}   {subject_discipline}   {degree_type}   {subject_code}   '
                          f'{subject_name}   {total_score}   {politics}   {english}   {course_one_score}   {course_two_score}')
                    data['学校名称'].append(school_name)
                    data['所在地区'].append(position)
                    data['创建时间'].append(school_creation_time)
                    data['院校隶属'].append(school_affiliation)
                    data['占地面积'].append(school_floor_space)
                    data['学校地址'].append(school_address)
                    data['是否为985'].append(is_985)
                    data['是否为211'].append(is_211)
                    data['所属院系'].append(subject_affiliation)
                    data['招生年份'].append(subject_enrollment_year)
                    data['学习方式'].append(subject_learning_style)
                    data['考试方式'].append(subject_exam_method)
                    data['计划招生人数'].append(subject_enrollment_num)
                    data['所属门类'].append(subject_category)
                    data['所属一级学科'].append(subject_discipline)
                    data['学位类型'].append(degree_type)
                    data['专业代码'].append(subject_code)
                    data['专业名称'].append(subject_name)
                    data['总分'].append(total_score)
                    data['政治'].append(politics)
                    data['英语'].append(english)
                    data['专业课一'].append(course_one_score)
                    data['专业课二'].append(course_two_score)
                    # 统计爬取专业在河北、北京、天津、985、211
                    if position == '河北':
                        if not score_hebei.get(subject['name']):
                            score_hebei[subject['name']] = []
                        score_hebei[subject['name']].append(total_score)
                    if position == '北京':
                        if not score_beijing.get(subject['name']):
                            score_beijing[subject['name']] = []
                        score_beijing[subject['name']].append(total_score)
                    if position == '江苏':
                        if not score_jiangsu.get(subject['name']):
                            score_jiangsu[subject['name']] = []
                        score_jiangsu[subject['name']].append(total_score)
                    if is_985:
                        if not score_985.get(subject['name']):
                            score_985[subject['name']] = []
                        score_985[subject['name']].append(total_score)
                    if is_211:
                        if not score_211.get(subject['name']):
                            score_211[subject['name']] = []
                        score_211[subject['name']].append(total_score)
    for key, value in score_hebei.items():
        create_chart('河北', key, value)
    for key, value in score_beijing.items():
        create_chart('北京', key, value)
    for key, value in score_jiangsu.items():
        create_chart('江苏', key, value)
    for key, value in score_985.items():
        create_chart('985', key, value)
    for key, value in score_211.items():
        create_chart('211', key, value)

if __name__ == '__main__':
    # 检查路径是否存在, 如果路径不存, 则创建路径
    if not os.path.exists('图片'):
        os.makedirs('图片')
    # 获取数据, '1'代表学术型硕士, '0'代表专业型硕士
    get_data(['物理'], 1)
    get_data(['数学', '计算机'], 0)
    df = pd.DataFrame(data)
    df.to_csv('分数线统计(数学、计算机、物理).csv', encoding='utf-8-sig', index=False)