import re

floor = '53层'
year = re.search(r"(\d+)层", floor).group(1)
