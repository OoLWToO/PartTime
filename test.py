import re

# 输入的字符串
address = "无锡市新吴区太科园传感网大学科技园立业楼B区203、204、205号"

# 正则表达式匹配省、市、区
pattern = r'(?P<province>[^省]+省)?(?P<city>[^市]+市)?(?P<district>[^区]+区)?'
match = re.match(pattern, address)

if match:
    province = match.group('province')
    city = match.group('city')
    district = match.group('district')

    print(f"省: {province}")
    print(f"市: {city}")
    print(f"区: {district}")
else:
    print("未匹配到省市区信息")