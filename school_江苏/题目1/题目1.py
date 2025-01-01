import traceback
import pandas as pd
import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

# 请求头
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

# 数据存储结构
DATA = {
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

def fetch_school_info(school_id):
    """获取学校基础信息"""
    school_url = f'http://kaoyan.cqvip.com/school/{school_id}'
    response = requests.get(school_url, headers=REQUEST_HEADERS)
    html = etree.HTML(response.text)
    xpath = '//*[@class="basic f-c-second"]//div[./span[text()="{}"]]/text()'
    try:
        school_name = html.xpath('//*[@class="title mr-83"]/text()')[0]
        creation_time = html.xpath(xpath.format('创建时间'))[0].replace(' ', '').replace('\n', '').replace(':', '')
        affiliation = html.xpath(xpath.format('院校隶属'))[0].replace(' ', '').replace('\n', '').replace(':', '')
        floor_space = html.xpath(xpath.format('占地面积'))[0].replace(' ', '').replace('\n', '').replace(':', '')
        address = html.xpath(xpath.format('学校地址'))[0].replace(' ', '').replace('\n', '').replace(':', '')
        position = html.xpath('//*[@class="title mr-83"]/following-sibling::small/text()')[0]
        is_985 = '是' if html.xpath('//*[@class="label-container xy-start mb-83"]/div[contains(text(),"985")]') else '否'
        is_211 = '是' if html.xpath('//*[@class="label-container xy-start mb-83"]/div[contains(text(),"211")]') else '否'
        return school_name, creation_time, affiliation, floor_space, address, position, is_985, is_211
    except Exception as e:
        print(f"获取学校信息失败: {e}")
        return None

def fetch_major_info(school_id, major_id, college_id):
    """获取专业介绍信息"""
    major_url = f'http://kaoyan.cqvip.com/school/{school_id}/introduce/{major_id}/{college_id}?year=2024'
    response = requests.get(major_url, headers=REQUEST_HEADERS)
    html = etree.HTML(response.text)
    xpath = '//*[@class="title bold" and contains(text(),"{}")]/following-sibling::span/@title'
    try:
        department = html.xpath(xpath.format('所属院系'))[0]
        enrollment_year = html.xpath(xpath.format('招生年份'))[0]
        learning_style = html.xpath(xpath.format('学习方式'))[0]
        exam_method = html.xpath(xpath.format('考试方式'))[0]
        enrollment_num = html.xpath(xpath.format('计划招生人数'))[0]
        category = html.xpath(xpath.format('所属门类'))[0]
        discipline = html.xpath(xpath.format('所属一级学科'))[0]
        return department, enrollment_year, learning_style, exam_method, enrollment_num, category, discipline
    except Exception as e:
        print(f"获取专业信息失败: {e}")
        return None

def fetch_score_line(school_id, major_code):
    """获取分数线信息"""
    score_line_url = f'http://kaoyan.cqvip.com/api/kaoyan/info/reExamination/academic-years-scoreline?current=1&size=1000&schoolIds={school_id}&year=2024'
    response = requests.get(score_line_url, headers=REQUEST_HEADERS)
    score_line_list = response.json()['data']['records']
    for score_line in score_line_list:
        if score_line['majorCode'] == major_code:
            return score_line
    return None

def process_major(major):
    """处理单个专业的数据"""
    school_search_url = f'http://kaoyan.cqvip.com/api/kaoyan/info/major/schoolInfo?current=1&size=1000&majorId={major["id"]}'
    response = requests.get(school_search_url, headers=REQUEST_HEADERS).json()['data']['records']
    for school in response:
        school_id = school['schoolId']
        college_id = school['collegeId']
        school_info = fetch_school_info(school_id)
        if not school_info:
            continue
        school_name, creation_time, affiliation, floor_space, address, position, is_985, is_211 = school_info
        if position not in ['河北', '北京', '江苏'] or (is_985 != '否' and is_211 != '否'):
            continue
        major_info = fetch_major_info(school_id, major["id"], college_id)
        if not major_info:
            continue
        department, enrollment_year, learning_style, exam_method, enrollment_num, category, discipline = major_info
        score_line = fetch_score_line(school_id, major['code'])
        if not score_line:
            continue
        major_type = score_line['majorType']
        major_code = score_line['majorCode']
        major_name = score_line['majorName']
        total_score = score_line['totalScore']
        politics_score = score_line['politicsScore']
        english_score = score_line['englishScore']
        course_one_score = score_line['courseOneScore']
        course_two_score = score_line['courseTwoScore']
        print(
            f'{school_name}   {position}   {creation_time}   {affiliation}   {floor_space}   '
            f'{address}   {is_985}   {is_211}   {department}   {enrollment_year}   '
            f'{learning_style}   {exam_method}   {enrollment_num}   {category}   '
            f'{discipline}   {major_type}   {major_code}   {major_name}   {total_score}   {politics_score}   '
            f'{english_score}   {course_one_score}   {course_two_score}')
        DATA['学校名称'].append(school_name)
        DATA['所在地区'].append(position)
        DATA['创建时间'].append(creation_time)
        DATA['院校隶属'].append(affiliation)
        DATA['占地面积'].append(floor_space)
        DATA['学校地址'].append(address)
        DATA['是否为985'].append(is_985)
        DATA['是否为211'].append(is_211)
        DATA['所属院系'].append(department)
        DATA['招生年份'].append(enrollment_year)
        DATA['学习方式'].append(learning_style)
        DATA['考试方式'].append(exam_method)
        DATA['计划招生人数'].append(enrollment_num)
        DATA['所属门类'].append(category)
        DATA['所属一级学科'].append(discipline)
        DATA['学位类型'].append(major_type)
        DATA['专业代码'].append(major_code)
        DATA['专业名称'].append(major_name)
        DATA['总分'].append(total_score)
        DATA['政治'].append(politics_score)
        DATA['英语'].append(english_score)
        DATA['专业课一'].append(course_one_score)
        DATA['专业课二'].append(course_two_score)

def main():
    major_list = []
    for search_content in ['数学', '计算机']:
        code_search_url = f'http://kaoyan.cqvip.com/api/kaoyan/info/major/page?current=1&name={search_content}&majorType=2&degreeType=1&size=1000'
        response = requests.get(code_search_url, headers=REQUEST_HEADERS).json()['data']['records']
        for major_data in response:
            if 'Z' not in major_data['code']:
                major_list.append(major_data)
    with ThreadPoolExecutor(max_workers=10, thread_name_prefix='thread_get_data') as executor:
        futures = [executor.submit(process_major, major) for major in major_list]
        try:
            wait(futures, return_when=ALL_COMPLETED, timeout=180)
        except Exception as e:
            print(f'等待线程完成时发生异常: {str(e)}')
            print(traceback.format_exc())
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"线程执行异常: {e}")
                print(traceback.format_exc())
    # 存入CSV
    df = pd.DataFrame(DATA)
    df.to_csv('数学与计算机分数线数据.csv', encoding='utf-8-sig', index=False)

if __name__ == '__main__':
    main()