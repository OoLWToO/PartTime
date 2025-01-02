import traceback

import pandas as pd
import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor, Future, wait, ALL_COMPLETED


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
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

def getData(major):
    school_search_url = f'http://kaoyan.cqvip.com/api/kaoyan/info/major/schoolInfo?current=1&size=1000&majorId={major["id"]}'
    r = requests.get(school_search_url, headers=headers).json()['data']['records']
    for school in r:
        schoolId = school['schoolId']
        collegeId = school['collegeId']
        # 获取学校基础信息: 学校名称、创建时间、院校隶属、占地面积、学校地址
        school_url = f'http://kaoyan.cqvip.com/school/{schoolId}'
        r = requests.get(school_url, headers=headers)
        html = etree.HTML(r.text)
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
        if position not in ['河北', '北京', '上海'] or (is_985 != '否' and is_211 != '否'):
            continue

        # 获取专业介绍: 所属院系、招生年份、学习方式、考试方式、计划招生人数、所属门类、所属一级学科
        major_xpath = '//*[@class="title bold" and contains(text(),"{}")]/following-sibling::span/@title'
        major_url = f'http://kaoyan.cqvip.com/school/{schoolId}/introduce/{major["id"]}/{collegeId}?year=2024'
        r = requests.get(major_url, headers=headers)
        html = etree.HTML(r.text)
        major_affiliation = html.xpath(major_xpath.format('所属院系'))[0]
        major_enrollment_year = html.xpath(major_xpath.format('招生年份'))[0]
        major_learning_style = html.xpath(major_xpath.format('学习方式'))[0]
        major_exam_method = html.xpath(major_xpath.format('考试方式'))[0]
        major_enrollment_num = html.xpath(major_xpath.format('计划招生人数'))[0]
        major_category = html.xpath(major_xpath.format('所属门类'))[0]
        major_discipline = html.xpath(major_xpath.format('所属一级学科'))[0]

        # 获取分数线: 学位类型、专业代码、专业名称、总分、政治、英语、专业课一、专业课二
        score_line_url = f'http://kaoyan.cqvip.com/api/kaoyan/info/reExamination/academic-years-scoreline?current=1&size=1000&schoolIds={schoolId}&year=2024'
        r = requests.get(score_line_url, headers=headers)
        score_line_list = r.json()['data']['records']
        for score_line in score_line_list:
            if score_line['majorCode'] == major['code']:
                major_type = score_line['majorType']
                major_code = score_line['majorCode']
                major_name = score_line['majorName']
                total_score = score_line['totalScore']
                politics_score = score_line['politicsScore']
                english_score = score_line['englishScore']
                course_one_score = score_line['courseOneScore']
                course_two_score = score_line['courseTwoScore']
                print(
                    f'{school_name}   {position}   {school_creation_time}   {school_affiliation}   {school_floor_space}   '
                    f'{school_address}   {is_985}   {is_211}   {major_affiliation}   {major_enrollment_year}   '
                    f'{major_learning_style}   {major_exam_method}   {major_enrollment_num}   {major_category}   '
                    f'{major_discipline}   {major_type}   {major_code}   {major_name}   {total_score}   {politics_score}   '
                    f'{english_score}   {course_one_score}   {course_two_score}')
                data['学校名称'].append(school_name)
                data['所在地区'].append(position)
                data['创建时间'].append(school_creation_time)
                data['院校隶属'].append(school_affiliation)
                data['占地面积'].append(school_floor_space)
                data['学校地址'].append(school_address)
                data['是否为985'].append(is_985)
                data['是否为211'].append(is_211)
                data['所属院系'].append(major_affiliation)
                data['招生年份'].append(major_enrollment_year)
                data['学习方式'].append(major_learning_style)
                data['考试方式'].append(major_exam_method)
                data['计划招生人数'].append(major_enrollment_num)
                data['所属门类'].append(major_category)
                data['所属一级学科'].append(major_discipline)
                data['学位类型'].append(major_type)
                data['专业代码'].append(major_code)
                data['专业名称'].append(major_name)
                data['总分'].append(total_score)
                data['政治'].append(politics_score)
                data['英语'].append(english_score)
                data['专业课一'].append(course_one_score)
                data['专业课二'].append(course_two_score)

if __name__ == '__main__':
    major_list = []
    for search_content in ['数学', '计算机']:
        code_search_url = f'http://kaoyan.cqvip.com/api/kaoyan/info/major/page?current=1&name={search_content}&majorType=2&degreeType=1&size=1000'
        r = requests.get(code_search_url, headers=headers).json()['data']['records']
        for r_data in r:
            # 专业代码中包含'Z'的为自定义专业, 不查询
            if 'Z' not in r_data['code']:
                major_list.append(r_data)
    request_executor = ThreadPoolExecutor(max_workers=10, thread_name_prefix='thread_get_data')
    request_futures = []
    for major in major_list:
        futures = request_executor.submit(getData, major)
        request_futures.append(futures)
    # 等待线程结束
    try:
        wait(request_futures, return_when=ALL_COMPLETED, timeout=180)
    except Exception as e:
        print(f'等待线程thread_requests完成时发生异常: {str(e)}')
        print(traceback.format_exc())
    if request_futures:
        for future in request_futures:
            try:
                future.result()
            except Exception as e:
                print(f"{future} 出现异常: {e}")
                print(traceback.format_exc())
                raise e
    request_futures.clear()
    # 存入csv
    df = pd.DataFrame(data)
    df.to_csv('分数线统计(数学、计算机).csv', encoding='utf-8-sig', index=False)
