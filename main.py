import json
import os
from os import path
from loguru import logger
from set_meta import save_card_list_by_set
from patch import p1934

patch_dict = {
    1934: p1934.save_card_list_by_set  # todo: need retry run
    # 1963: p1963.save_card_list_by_set,
    # 1978: p1978.save_card_list_by_set,
    # 1984: p1984.save_card_list_by_set,
    # 1985: p1985.save_card_list_by_set,
    # 1986: p1986.save_card_list_by_set,
    # 1987: p1987.save_card_list_by_set,
}

# stop in 1988

# new start in 2001

# 2024 还没结束

error_year_set = {
    2023: ["Chase-Brown"],
    2017: ["2017-Donruss"],
    2011: ["2011-Panini"],
    2010: ["2010-Ballkardz-", "2010-Panini"],
    2009: ["Topps"],
    2006: ["2006-Philadelphia-Inquirer"],
    2005: ["2005-Philadelphia-Inquirer"],
    2004: ["Topps"],
    2003: ["2003-Coca-Cola", "Topps"],
    2002: ["2002-Coca-Cola"],
}


def check_error_continue(year, sid):
    if year in error_year_set:
        if sid in error_year_set[year]:
            return True


after_dict = {
    2010: "2010-Panini",
    2009: "Topps",
    2008: "235890",
    2007: "167268",
    2006: "152240",
    2005: "2005-Philadelphia-Inquirer",
    2004: "4688",
    2003: "38219",
    2002: "4575",
}

success_exit = False
while success_exit is False:
    start_year_env = int(os.getenv('START_YEAR', 2023))
    end_year_env = int(os.getenv('END_YEAR', 2023))
    category = os.getenv('CATEGORY', 'Football')
    if not category:
        raise Exception("CATEGORY not set")

    try:
        config = {
            "category": category,
            "start_year": start_year_env,
            "end_year": end_year_env,
        }

        config_dir_path = path.join('data', config['category'])

        # 读取 config_dir_path 目录下所有的文件名的列表
        year_set_files = [f for f in os.listdir(config_dir_path) if path.isfile(path.join(config_dir_path, f))]

        # 文件名的结构是 output{year}.json, files 需要按照 year 从小到大排序
        # year_set_files.sort(key=lambda x: int(x[6:-5]))

        # 文件名的结构是 output{year}.json, files 需要按照 year 从大到小排序
        year_set_files.sort(key=lambda x: int(x[6:-5]), reverse=True)

        # 找出 start_year 和 end_year 对应的文件名，如果start_year <= 0 则从第一个文件开始，如果 end_year <= 0 则到最后一个文件结束
        # 如果指定了正确的 start_year 和 end_year，那么就取这个区间的文件

        start_index = 0
        end_index = len(year_set_files)

        # 现在需要倒着来，start_year 和 end_year 都是从大到小的

        if config['start_year'] > 0:
            for i, file in enumerate(year_set_files):
                year = int(file[6:-5])
                if year == config['start_year']:
                    start_index = i
                    break

        if config['end_year'] > 0:
            for i, file in enumerate(year_set_files):
                year = int(file[6:-5])
                if year == config['end_year']:
                    end_index = i + 1
                    break

        year_set_files = year_set_files[start_index:end_index]

        logger.info("读取配置成功，需要处理的文件列表如下:")
        logger.info(year_set_files)

        # 循环处理每个文件
        for file in year_set_files:
            logger.info(f"开始处理文件: {file}")
            with open(path.join(config_dir_path, file), 'r', encoding='utf-8') as f:
                data = json.load(f)

            year = int(file[6:-5])

            has_after_done = False
            for set_msg in data:
                """
                set_msg ex:
                {
                    "name": "2024 Donruss",
                    "sid": "123"
                }
                """
                if not has_after_done and year in after_dict:
                    if set_msg["sid"] == after_dict[year]:
                        has_after_done = True
                    else:
                        continue

                if check_error_continue(year, set_msg["sid"]):
                    logger.warning(f"set [{set_msg['name']}] in [{year}] is error, ignore this set")
                    continue

                if year in patch_dict:
                    # 某些年份的页面结构不一样，需要单独处理
                    patch_dict[year](year, set_msg['name'], f'/Checklist.cfm/sid/{set_msg["sid"]}')
                else:
                    # 通用处理
                    save_card_list_by_set(year, set_msg['name'], f'/Checklist.cfm/sid/{set_msg["sid"]}')

            logger.info(f"处理文件: {file} 完成")
        success_exit = True
    except Exception as e:
        logger.exception(f"处理文件时发生异常: {e}")
