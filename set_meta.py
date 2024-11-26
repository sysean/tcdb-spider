from http_utils import send
from log import setup_logging
from loguru import logger
from constant import category
from save_db import query_dataset, get_card_count, insert_dataset, insert_card

setup_logging()

"""
set example:

{
    "set_name": "2024 Donruss",
    "rating": "TBA",
    "total_cards": 400,
    "release_dates": ["Donruss - Oct 24, 2024", "Factory Set - Dec 27, 2024"],
    "set_url": "https://www.tcdb.com/Checklist.cfm/sid/462124",
    "category": "Football",
    "list": [
        {
            
        }
    ]
}

"""


# image url : /Images/Cards/Football/

def get_primary_key_for_card(player_url):
    sid = player_url.split('/')[3]
    cid = player_url.split('/')[5]
    return f"{sid}-{cid}"


def save_card_list(total, set_url, soup=None, index=0):
    if index > total:
        return []
    # 如果能执行此函数，说明该set没有爬完

    # 一页有100张数据，所以需要计算总共有多少页
    total_page = (total + 99) // 100

    # 计算当前 current_page 页数，因为 index 可能不是从 0 开始
    current_page = (index + 100) // 100

    card_list = []
    while current_page <= total_page:
        if not soup:
            soup = send(f"https://www.tcdb.com{set_url}?PageIndex={current_page}", msg="真实的set页面翻页")

        # 找到 class 为 col-md-6 nopadding 的 div 标签
        col_md_6_nopadding = soup.find('div', class_='col-md-6 nopadding')
        # 找到其中 class 为 block1 的 div 标签
        block1_div = col_md_6_nopadding.find('div', class_='block1')

        try:
            # 找到第二个 table 标签
            table_tag = block1_div.find_all('table')[1]
        except Exception:
            # 如果找不到，说明没有card
            return card_list

        # 获取 tr 标签列表
        tr_list = table_tag.find_all('tr')

        # 根据 index 计算当前页的起始位置
        tr_list = tr_list[index % 100:]

        for tr in tr_list:
            # 获取 tr 下第一个 td 标签
            td = tr.find('td')
            # 获取 td 下第二个 a 标签的 href 属性
            player_url = td.find_all('a')[1]['href']

            # 获取 td 下第二个 a 标签的下的 img 的 src 属性
            try:
                img_src = td.find_all('a')[1].find('img')['data-original']
            except Exception:
                img_src = td.find_all('a')[1].find('img')['src']

            is_no_img_card = img_src == '/Images/AddCard.gif'

            # 获取所有 td 标签，找到其中有a标签，并且带有href属性，列出这些 td 标签
            row_td_list = tr.find_all('td')
            td_text_list = [td.get_text(strip=True) for td in row_td_list if td.get_text(strip=True)]

            card_name = td_text_list[-2]
            team_name = td_text_list[-1]

            if not card_name or not team_name:
                raise Exception(f"card_name or team_name is None, card_name: {card_name}, team_name: {team_name}")

            card_metadata = {
                "id": get_primary_key_for_card(player_url),
                "index": index,
                "name": card_name,
                "team": team_name,
                "player_url": player_url,
                "dataset_id": _get_sid(set_url),
                "card_num": td_text_list[0][:50],
            }

            if is_no_img_card:
                index += 1
                card_list.append(card_metadata)
                insert_card(card_metadata)
                continue

            soup = send(f"https://www.tcdb.com{player_url}", "请求卡片详情页面")

            # 开始获取 sub_set 信息
            sub_set = soup.find('h3').get_text().strip()

            card_metadata["sub_set"] = sub_set if sub_set != 'Search eBay...' else None

            # 开始获取卡片图片信息

            # 获取 class 为 col-md-9 nopadding 的 div 标签
            col_md_9_nopadding = soup.find('div', class_='col-md-9 nopadding')

            # 获取第二个 table
            table_tag = col_md_9_nopadding.find_all('table')[1]

            # 获取所有 img 标签
            img_tags = table_tag.find_all('img')

            # 第一个 img 标签的 src 属性
            front_img = img_tags[0]['src']

            # 第二个 img 标签的 src 属性
            back_img = img_tags[1]['src']

            # 获取所有 class 为 easyzoom easyzoom--overlay is-ready 的 div 标签
            # easyzoom_divs = soup.find_all('div', class_='easyzoom easyzoom--overlay')
            #
            # # 获取第一个 easyzoom_div 下面的 a 标签的 href 属性
            # front_img = easyzoom_divs[0].find('a')['href']
            #
            # # 获取第二个 easyzoom_div 下面的 a 标签的 href 属性
            # back_img = easyzoom_divs[1].find('a')['href']

            card_metadata["front_img"] = front_img
            card_metadata["back_img"] = back_img

            # 开始获取 卡片图片下面的 metadata 信息

            # 找到 class 为 col-md-9 nopadding 的 div 标签
            col_md_9_nopadding = soup.find('div', class_='col-md-9 nopadding')
            # 找到其中 class 为 block1 的 div 标签
            block1_div = col_md_9_nopadding.find('div', class_='block1')
            # 找到其中 第 4 个 table 标签
            table_tag = block1_div.find_all('table')[3]
            # 找到其中第1个 tr 标签
            tr_tag = table_tag.find_all('tr')[0]
            # 找到 li 列表
            li_list = tr_tag.find_all('li')

            card_metadata["front_submitted_time"] = li_list[0].get_text().strip()[:50]
            card_metadata["back_submitted_time"] = li_list[1].get_text().strip()[:50]
            card_metadata["price"] = li_list[2].get_text().strip()
            if card_metadata["price"] == 'Submit a Price':
                card_metadata["price"] = None

            insert_card(card_metadata)

            card_list.append(card_metadata)

            index += 1

        current_page += 1

    return card_list


def get_set_metadata(soup):
    # 获取第一个 class 为 col-md-3 nopadding 的 div 标签
    col_md_3_nopadding = soup.find('div', class_='col-md-3 nopadding')
    # 获取第一个 class 为 block1 的 div 标签
    block1_div = col_md_3_nopadding.find('div', class_='block1')
    # 获取该 block1_div 的第二个 p 标签
    p_total_card_tag = block1_div.find_all('p')[1]
    # 获取 p_total_card_tag 标签的内容， 去掉空格，并转为 int 类型

    try:
        total_cards = int(p_total_card_tag.get_text()[13:].strip())
    except Exception:
        return {
            "total_cards": 0,
        }

    # 获取 block1_div 的第三个 p 标签
    p_rating_tag = block1_div.find_all('p')[2]
    # 获取 p_rating_tag 标签的内容
    rating = p_rating_tag.get_text().split('\n')[0].split(':')[1].strip()

    # 获取 block1_div 下的第一个 ul 标签，并再获取其中的 ul 标签，并继续获取其中的所有 li 标签
    li_list = []
    try:
        li_list = block1_div.find('ul').find('ul').find_all('li')
    except Exception:
        # 说明没有 release_dates，忽略
        pass

    release_dates = [li.get_text().strip() for li in li_list] if li_list else []

    return {
        "total_cards": total_cards,
        "rating": rating,
        "release_dates": '|'.join(release_dates)
    }


def _get_sid(set_url):
    return int(set_url.split('/')[-1])


# 获取某个集合下所有的卡片列表
def save_card_list_by_set(year, name, set_url):
    sid = _get_sid(set_url)

    dataset = query_dataset(sid)
    if dataset:
        if dataset.is_empty:
            logger.warning(f"set [{name}] in [{year}] is empty, ignore this set")
            return

        card_count = get_card_count(sid)
        if card_count == dataset.total_cards:
            logger.warning(f"set [{name}] in [{year}] all cards have been saved, ignore this set")
            return

        if card_count > dataset.total_cards:
            logger.error(f"set [{name}] in [{year}] card count is more than total cards, ignore this set")
            # raise Exception(f"set [{name}] in [{year}] card count is more than total cards, error")
            return

        # 说明该set没有爬完
        index = card_count
        save_card_list(dataset.total_cards, set_url, index=index)

        logger.info(f"success get residue set for [{name}] in[{year}]")
        return

    logger.info(f"first start get set for [{name}] in [{year}]")

    # 请求真实的 set 网站
    soup = send(f"https://www.tcdb.com{set_url}", msg="真实的set页面")

    set_metadata = get_set_metadata(soup)
    set_metadata["set_name"] = name
    set_metadata["set_url"] = f"https://www.tcdb.com{set_url}"
    set_metadata["year"] = year
    set_metadata["id"] = sid
    set_metadata["category"] = category
    set_metadata["is_empty"] = set_metadata["total_cards"] == 0

    insert_dataset(set_metadata)

    card_list = save_card_list(set_metadata["total_cards"], set_url, soup=soup)

    if not card_list:
        set_metadata["is_empty"] = True

    # total cards 以实际获取的卡片数量为准
    if len(card_list) != set_metadata["total_cards"]:
        set_metadata["total_cards"] = len(card_list)

    # name 将所有空格替换为中划线
    name = name.replace(' ', '-')

    logger.info(f"success get set for [{name}] in [{year}]")

# get_card_list_by_set(2024, "2024 Donruss", "/Checklist.cfm/sid/462124")

# get_card_list_by_set(1907, '1907 Missouri Tigers Postcards', '/Checklist.cfm/sid/245772')
