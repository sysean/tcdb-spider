import os
from log import setup_logging
from loguru import logger

from model_v2 import ErrorDatasetLog
from save_db import query_year_dataset_output, query_dataset_cursor, query_one_error_dataset, \
    insert_error_dataset, update_error_dataset, insert_or_update_dataset_cursor
from set_meta import save_card_list_by_set

setup_logging()

start_year_env = int(os.getenv('START_YEAR', 2023))
end_year_env = int(os.getenv('END_YEAR', 2023))
category = os.getenv('CATEGORY', 'Football')
if not category:
    raise Exception("CATEGORY not set")

year_dataset_list = query_year_dataset_output(start_year_env, end_year_env, category)

year_dataset_dict = {}
for year_dataset in year_dataset_list:
    if year_dataset.year not in year_dataset_dict:
        year_dataset_dict[year_dataset.year] = []
    year_dataset_dict[year_dataset.year].append(year_dataset)

logger.info(f"这些年份的数据需要被处理: {year_dataset_dict.keys()}")
for year, dataset_list in year_dataset_dict.items():
    logger.info(f"year: {year}, dataset size: {len(dataset_list)}")

# 年份的游标
year_cursor_list = query_dataset_cursor(category)
year_cursor_dict = {}
for year_cursor in year_cursor_list:
    year_cursor_dict[year_cursor.year] = year_cursor.sid

if year_cursor_list:
    for year, sid in year_cursor_dict.items():
        if year not in year_dataset_dict:
            continue

        # 判断 year 所在的 sid 在 year_dataset_dict[year] 中的位置
        index = -1
        for i, dataset in enumerate(year_dataset_dict[year]):
            if dataset.sid == sid:
                index = i
                break
        logger.info(
            f"year: {year} 一共有 {year_dataset_dict[year]}个集合, 已处理 {index + 1} 个集合, "
            f"剩余 {len(year_dataset_dict[year]) - index - 1} 个集合未处理")

        year_dataset_dict[year] = year_dataset_dict[year][index + 1:]

        if not year_dataset_dict[year]:
            logger.info(f"year: {year} 的数据已经全部处理完毕")
            del year_dataset_dict[year]

for year, dataset_list in year_dataset_dict.items():
    logger.info(f"开始处理年份 {year} 的数据")

    for dataset in dataset_list:
        logger.info(f"开始处理集合: [{dataset.set_name}], year: {year}, sid: {dataset.sid}")

        retry_times = 0
        while retry_times <= 3:
            try:
                save_card_list_by_set(year, dataset.set_name, f'/Checklist.cfm/sid/{dataset.sid}')

                # 更新游标
                insert_or_update_dataset_cursor(category, year, dataset.sid)
                break
            except Exception as e:
                logger.error(f"集合 {dataset.set_name} 处理出错: {e}")
                error_dataset = query_one_error_dataset(f"{category}_{dataset.sid}")
                if error_dataset:
                    logger.warning(f"集合 [{dataset.set_name}] 已经记录过错误")
                    error_dataset.retry_times += 1
                    error_dataset.error_msg = str(e)
                    update_error_dataset(error_dataset)
                else:
                    logger.warning(f"集合 [{dataset.set_name}] 记录错误")
                    insert_error_dataset(ErrorDatasetLog(
                        id=f"{category}_{dataset.sid}",
                        category=category,
                        year=year,
                        set_name=dataset.set_name,
                        error_msg=str(e),
                        retry_times=1
                    ))
                retry_times += 1

        logger.info(f"集合: {dataset.set_name} 处理完成,  year: {year}, sid: {dataset.sid}")
    logger.info(f"年份 {year} 的数据处理完成")

logger.info("所有数据处理完成")
