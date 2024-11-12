import json
from http_utils import send
from log import setup_logging
from constant import years

setup_logging()


# 测试获取某个 year 下所有的集合列表
def get_set_list_by_year(year: int):
    url = f"https://www.tcdb.com/ViewAll.cfm/sp/Football/year/{year}"

    soup = send(url, msg="获取某个 year 下所有的集合列表")

    block1_divs = soup.find_all('div', class_='block1')
    index = 0

    li_list = []
    for block1 in block1_divs:
        first_child = block1.find()
        if first_child and first_child.name == 'a':
            ul_tags = block1.find_all('ul')

            for ul in ul_tags:
                for li in ul.find_all('li'):
                    a_tag = li.find('a')
                    if a_tag:
                        li_list.append({
                            "name": a_tag.get_text(strip=True),
                            "sid": a_tag['href'].split('/')[-2]
                        })
                index += 1

    with open(f'data/Football/output{year}.json', 'w', encoding='utf-8') as f:
        json.dump(li_list, f, ensure_ascii=False, indent=4)


# 运行打开此注释
for year in years:
    get_set_list_by_year(year)
