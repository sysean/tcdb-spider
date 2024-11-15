# 图片下载路径为 tcdb/Images/Cards/Football/107092/107092-24598750RepFr.jpg
import os
from constant import category, years
from loguru import logger

from http_utils import download_image_to_s3
from save_db import get_cnt_for_database, iterate_datasets_with_cards, query_card_crawler_log, write_card_crawler_log

config = {
    "start_year": 1954,
    "end_year": -1,
}

bucket_name = 'irida'
root_path = 'tcdb'

category_root = f'Images/Cards/{category}'
if not os.path.exists(category_root):
    os.makedirs(category_root)

start_index = 0
end_index = len(years) - 1

if config['start_year'] > 0:
    for i, year in enumerate(years):
        if year == config['start_year']:
            start_index = i
            break

if config['end_year'] > 0 and config['end_year'] >= config['start_year']:
    for i, year in enumerate(years):
        if year == config['end_year']:
            end_index = i + 1
            break

cnt = get_cnt_for_database(years[start_index], years[end_index])

logger.info(f"需要处理的数据集数量为: {cnt}, 开始年份: {years[start_index]}, 结束年份: {years[end_index]}")
logger.info("start download images...")

for dataset in iterate_datasets_with_cards(cnt, years[start_index], years[end_index]):
    card_status_list = query_card_crawler_log(dataset.id)

    # card_status_list 里面存在的 card，表示已经下载过了，需要过滤掉
    card_status_set = set([card_status.card_id for card_status in card_status_list])

    for card in dataset.cards:
        if not card.front_img and not card.back_img:
            continue

        if card.id in card_status_set:
            continue

        logger.info(f"download image for card: {card.id}, set: {dataset.set_name}, year: {dataset.year}")
        if card.front_img:
            download_image_to_s3(f'https://www.tcdb.com{card.front_img}', bucket_name, f'{root_path}{card.front_img}')
        if card.back_img:
            download_image_to_s3(f'https://www.tcdb.com{card.back_img}', bucket_name, f'{root_path}{card.back_img}')
        logger.info(f"download image for card: {card.id} success")

        write_card_crawler_log(dataset.id, card.id)
