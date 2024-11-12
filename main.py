import json
import os
from os import path
from loguru import logger

from constant import category
from set_meta import get_card_list_by_set

success_exit = False
while success_exit is False:
    try:
        config = {
            "category": category,
            "start_year": -1,
            "end_year": -1,
        }

        config_dir_path = path.join('data', config['category'])

        # 读取 config_dir_path 目录下所有的文件名的列表
        year_set_files = [f for f in os.listdir(config_dir_path) if path.isfile(path.join(config_dir_path, f))]

        # 文件名的结构是 output{year}.json, files 需要按照 year 从小到大排序
        year_set_files.sort(key=lambda x: int(x[6:-5]))

        # 找出 start_year 和 end_year 对应的文件名，如果start_year <= 0 则从第一个文件开始，如果 end_year <= 0 则到最后一个文件结束
        # 如果指定了正确的 start_year 和 end_year，那么就取这个区间的文件

        start_index = 0
        end_index = len(year_set_files)

        if config['start_year'] > 0:
            for i, f in enumerate(year_set_files):
                if int(f[6:-5]) == config['start_year']:
                    start_index = i
                    break

        if config['end_year'] > 0 and config['end_year'] >= config['start_year']:
            for i, f in enumerate(year_set_files):
                if int(f[6:-5]) == config['end_year']:
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

            for set_msg in data:
                """
                set_msg ex:
                {
                    "name": "2024 Donruss",
                    "sid": "123"
                }
                """
                get_card_list_by_set(year, set_msg['name'], f'/Checklist.cfm/sid/{set_msg["sid"]}')

            logger.info(f"处理文件: {file} 完成")
        success_exit = True
    except Exception as e:
        logger.exception(f"处理文件时发生异常: {e}")
