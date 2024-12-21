import os

import pandas as pd
import requests
from lxml import etree
from openpyxl.styles.builtins import total

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

data = {
    '学校名称': [],
    '创建时间': [],
    '院校隶属': [],
    '占地面积': [],
    '学校地址': [],
    '学位类型': [],
    '专业代码': [],
    '专业名称': [],
    '总分': [],
    '政治': [],
    '英语': [],
    '专业课一': [],
    '专业课二': [],
}

if __name__ == '__main__':
    # 检查路径是否存在
    if not os.path.exists('爬虫'):
        # 如果路径不存在，则创建路径
        os.makedirs('爬虫')
    codeId_list = {}
    for search_content in ['数学', '计算机科学与技术']:
        code_search_url = f'http://kaoyan.cqvip.com/api/kaoyan/info/major/page?current=1&name={search_content}&majorType=2&degreeType=1&size=100'
        r = requests.get(code_search_url, headers=headers)
        subject_list = r.json()['data']['records']
        for subject in subject_list:
            # 专业代码中包含'Z'的为自定义专业, 不查询
            if 'Z' not in subject['code'] and search_content == subject['name']:
                codeId_list[(subject['id'])] = subject['code']
    for codeId, code in codeId_list.items():
        school_search_url = f'http://kaoyan.cqvip.com/api/kaoyan/info/major/schoolInfo?current=1&size=1000&majorId={codeId}'
        r = requests.get(school_search_url, headers=headers)
        school_list = r.json()['data']['records']
        for school in school_list:
            schoolId = school['schoolId']
            collegeId = school['collegeId']
            # 获取学校基础信息: 学校名称、创建时间、院校隶属、占地面积、学校地址
            school_url = f'http://kaoyan.cqvip.com/school/{schoolId}'
            r = requests.get(school_url, headers=headers)
            html = etree.HTML(r.text)
            school_xpath = '//*[@class="basic f-c-second"]//div[./span[text()="{}"]]/text()'
            school_name = html.xpath('//*[@class="title mr-83"]/text()')[0]
            school_creation_time = html.xpath(school_xpath.format('创建时间'))[0].replace(' ', '').replace('\n', '').replace(':', '')
            school_affiliation = html.xpath(school_xpath.format('院校隶属'))[0].replace(' ', '').replace('\n', '').replace(':', '')
            school_floor_space = html.xpath(school_xpath.format('占地面积'))[0].replace(' ', '').replace('\n', '').replace(':', '')
            school_address = html.xpath(school_xpath.format('学校地址'))[0].replace(' ', '').replace('\n', '').replace(':', '')

            # 获取分数线: 学位类型、专业代码、专业名称、总分、政治、英语、专业课一、专业课二
            score_line_url = f'http://kaoyan.cqvip.com/api/kaoyan/info/reExamination/academic-years-scoreline?current=1&size=1000&schoolIds={schoolId}&year=2024'
            r = requests.get(score_line_url, headers=headers)
            score_line_list = r.json()['data']['records']
            for score_line in score_line_list:
                if score_line['majorCode'] == code:
                    degree_type = score_line['majorType']
                    subject_code = score_line['majorCode']
                    subject_name = score_line['majorName']
                    total_score = score_line['totalScore']
                    politics = score_line['politicsScore']
                    english = score_line['englishScore']
                    course_one_score = score_line['courseOneScore']
                    course_two_score = score_line['courseTwoScore']
                    print(f'{school_name}   {school_creation_time}   {school_affiliation}   {school_floor_space}   {school_address}   '
                          f'{degree_type}   {subject_code}   {subject_name}   {total_score}   {politics}   {english}   '
                          f'{course_one_score}   {course_two_score}')
                    data['学校名称'].append(school_name)
                    data['创建时间'].append(school_creation_time)
                    data['院校隶属'].append(school_affiliation)
                    data['占地面积'].append(school_floor_space)
                    data['学校地址'].append(school_address)
                    data['学位类型'].append(degree_type)
                    data['专业代码'].append(subject_code)
                    data['专业名称'].append(subject_name)
                    data['总分'].append(total_score)
                    data['政治'].append(politics)
                    data['英语'].append(english)
                    data['专业课一'].append(course_one_score)
                    data['专业课二'].append(course_two_score)
            df = pd.DataFrame(data)
            df.to_csv('爬虫/数学与计算机专业分数线数据统计1.csv', encoding='utf-8-sig', index=False)