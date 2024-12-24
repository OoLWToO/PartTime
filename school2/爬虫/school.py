import pandas as pd
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
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

if __name__ == '__main__':
    subject_list = []
    for search_content in ['数学', '计算机']:
        code_search_url = f'http://kaoyan.cqvip.com/api/kaoyan/info/major/page?current=1&name={search_content}&majorType=2&degreeType=1&size=100'
        response = requests.get(code_search_url, headers=headers)
        records = response.json()['data']['records']
        for record in records:
            # 专业代码中包含'Z'的为自定义专业, 不查询
            if 'Z' not in record['code']:
                subject_list.append(record)
    for subject in subject_list:
        school_search_url = f'http://kaoyan.cqvip.com/api/kaoyan/info/major/schoolInfo?current=1&size=1000&majorId={subject["id"]}'
        response = requests.get(school_search_url, headers=headers)
        school_list = response.json()['data']['records']
        for school in school_list:
            schoolId = school['schoolId']
            collegeId = school['collegeId']
            # 获取学校基础信息: 学校名称、创建时间、院校隶属、占地面积、学校地址
            school_url = f'http://kaoyan.cqvip.com/school/{schoolId}'
            response = requests.get(school_url, headers=headers)
            html = etree.HTML(response.text)
            school_xpath = '//*[@class="basic f-c-second"]//div[./span[text()="{}"]]/text()'
            school_name = html.xpath('//*[@class="title mr-83"]/text()')[0]
            school_creation_time = html.xpath(school_xpath.format('创建时间'))[0].replace(' ', '').replace('\n',
                                                                                                           '').replace(
                ':', '')
            school_affiliation = html.xpath(school_xpath.format('院校隶属'))[0].replace(' ', '').replace('\n',
                                                                                                         '').replace(
                ':', '')
            school_floor_space = html.xpath(school_xpath.format('占地面积'))[0].replace(' ', '').replace('\n',
                                                                                                         '').replace(
                ':', '')
            school_address = html.xpath(school_xpath.format('学校地址'))[0].replace(' ', '').replace('\n', '').replace(
                ':', '')
            # 获取位置用于统计
            position = html.xpath('//*[@class="title mr-83"]/following-sibling::small/text()')[0]
            is_985 = '是' if html.xpath(
                '//*[@class="label-container xy-start mb-83"]/div[contains(text(),"985")]') else '否'
            is_211 = '是' if html.xpath(
                '//*[@class="label-container xy-start mb-83"]/div[contains(text(),"211")]') else '否'

            # 获取专业介绍: 所属院系、招生年份、学习方式、考试方式、计划招生人数、所属门类、所属一级学科
            subject_xpath = '//*[@class="title bold" and contains(text(),"{}")]/following-sibling::span/@title'
            subject_url = f'http://kaoyan.cqvip.com/school/{schoolId}/introduce/{subject["id"]}/{collegeId}?year=2024'
            response = requests.get(subject_url, headers=headers)
            html = etree.HTML(response.text)
            subject_affiliation = html.xpath(subject_xpath.format('所属院系'))[0]
            subject_enrollment_year = html.xpath(subject_xpath.format('招生年份'))[0]
            subject_learning_style = html.xpath(subject_xpath.format('学习方式'))[0]
            subject_exam_method = html.xpath(subject_xpath.format('考试方式'))[0]
            subject_enrollment_num = html.xpath(subject_xpath.format('计划招生人数'))[0]
            subject_category = html.xpath(subject_xpath.format('所属门类'))[0]
            subject_discipline = html.xpath(subject_xpath.format('所属一级学科'))[0]

            # 获取分数线: 学位类型、专业代码、专业名称、总分、政治、英语、专业课一、专业课二
            score_line_url = f'http://kaoyan.cqvip.com/api/kaoyan/info/reExamination/academic-years-scoreline?current=1&size=1000&schoolIds={schoolId}&year=2024'
            response = requests.get(score_line_url, headers=headers)
            score_line_list = response.json()['data']['records']
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
                    print(
                        f'{school_name}   {position}   {school_creation_time}   {school_affiliation}   {school_floor_space}   '
                        f'{school_address}   {is_985}   {is_211}   {subject_affiliation}   {subject_enrollment_year}   '
                        f'{subject_learning_style}   {subject_exam_method}   {subject_enrollment_num}   {subject_category}   '
                        f'{subject_discipline}   {degree_type}   {subject_code}   {subject_name}   {total_score}   {politics}   '
                        f'{english}   {course_one_score}   {course_two_score}')
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
    df = pd.DataFrame(data)
    df.to_csv('数学和计算机分数线数据统计.csv', encoding='utf-8-sig', index=False)
