import logging
from typing import Type

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from model_v2 import DatasetV2, CardV2, CardCrawlerStatusV2, OutputYearDataset, ErrorDatasetLog, DatasetCursor

# sqlite3
# engine = create_engine('sqlite:///tcdb_cards.db', echo=True)

# mysql
# engine = create_engine(
#     'mysql+pymysql://sean_123:43XLpZssa*Py_!L@rm-2vc52f63lasvix4w7po.mysql.cn-chengdu.rds.aliyuncs.com:3306/tcdb',
#     echo=True)

# pgsql
engine = create_engine(
    'postgresql+psycopg://postgres:%L%sFxL3}3aKG4al}ZFBFQj-iT.h@tcdb-crawler-db.cluster-c0xt5dijvnyu.us-east-2.rds.amazonaws.com:5432/tcdb',
    echo=True,
    pool_size=20,  # The size of the pool to be maintained
    max_overflow=10,  # The maximum overflow size of the pool
    poolclass=QueuePool
)

# 创建表结构
# Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def insert_year_dataset_output_batch(data: list[dict]):
    session = Session()
    with session.begin():
        session.add_all([OutputYearDataset(**d) for d in data])
    session.close()


def query_year_dataset_output(start_year: int, end_year: int, category: str) -> list[Type[OutputYearDataset]]:
    session = Session()
    year_datasets = session.query(OutputYearDataset).filter(
        OutputYearDataset.year >= start_year,
        OutputYearDataset.year <= end_year,
        OutputYearDataset.category == category
    ).order_by(OutputYearDataset.year.desc()).all()
    session.close()
    return year_datasets


def query_error_year_set(start_year: int, end_year: int, category: str) -> list[Type[ErrorDatasetLog]]:
    session = Session()
    year_datasets = session.query(ErrorDatasetLog).filter(
        ErrorDatasetLog.year >= start_year,
        ErrorDatasetLog.year <= end_year,
        ErrorDatasetLog.category == category
    ).order_by(ErrorDatasetLog.year.desc()).all()
    session.close()
    return year_datasets


def query_one_error_dataset(id: str) -> Type[ErrorDatasetLog]:
    session = Session()
    error_dataset = session.query(ErrorDatasetLog).filter(ErrorDatasetLog.id == id).first()
    session.close()
    return error_dataset


def update_error_dataset(error_dataset: Type[ErrorDatasetLog]):
    session = Session()
    with session.begin():
        session.merge(error_dataset)
    session.close()


def insert_error_dataset(error_dataset: ErrorDatasetLog):
    session = Session()
    with session.begin():
        session.add(error_dataset)
    session.close()


def query_dataset_cursor(category: str) -> list[Type[DatasetCursor]]:
    session = Session()
    dataset_cursor = session.query(DatasetCursor).filter(DatasetCursor.category == category).order_by(
        DatasetCursor.year.desc()).all()
    session.close()
    return dataset_cursor


def insert_or_update_dataset_cursor(category, year, sid):
    session = Session()
    with session.begin():
        cursor = session.query(DatasetCursor).filter(DatasetCursor.category == category,
                                                     DatasetCursor.year == year).first()
        if cursor:
            cursor.sid = sid
        else:
            cursor = DatasetCursor(category=category, year=year, sid=sid)
            session.add(cursor)
    session.close()


# 插入 Dataset 数据，输入为 dict
def insert_dataset(data: dict):
    session = Session()
    with session.begin():
        dataset = session.query(DatasetV2).filter(DatasetV2.id == data['id']).first()
        if dataset:
            for key, value in data.items():
                setattr(dataset, key, value)
        else:
            dataset = DatasetV2(**data)
            session.add(dataset)
    session.close()


# 查询 Dataset 数据，输入为 sid
def query_dataset(sid: str):
    session = Session()
    dataset = session.query(DatasetV2).filter(DatasetV2.id == sid).first()
    session.close()
    return dataset


# 插入 Card 数据，输入为 dict
def insert_card(data: dict):
    session = Session()
    try:
        with session.begin():
            card = CardV2(**data)
            session.add(card)
    except IntegrityError as e:
        logging.error(f"IntegrityError: {e}")
    finally:
        session.close()


def get_card_count(sid: str):
    session = Session()
    count = session.query(CardV2).filter(CardV2.dataset_id == sid).count()
    session.close()
    return count


def get_cnt_for_database(start_year: int, end_year: int):
    session = Session()
    cnt = session.query(DatasetV2).filter(DatasetV2.is_empty == False,
                                          DatasetV2.total_cards > 0,
                                          DatasetV2.year >= start_year,
                                          DatasetV2.year <= end_year
                                          ).count()
    session.close()
    return cnt


# 迭代 Dataset 数据
def iterate_datasets_with_cards(start_year: int, end_year: int):
    batch_size = 100

    session = Session()
    try:
        query = session.query(DatasetV2).options(
            selectinload(DatasetV2.cards)
        ).filter(
            DatasetV2.is_empty == False,
            DatasetV2.total_cards > 0,
            DatasetV2.year >= start_year,
            DatasetV2.year <= end_year
        ).order_by(DatasetV2.year.desc()).yield_per(batch_size)
        for dataset in query:
            dataset.cards.sort(key=lambda card: card.index)
            yield dataset
    finally:
        session.close()


# 根据 dataset_id 查询 CardCrawlerLog
def query_card_crawler_log(dataset_id: str):
    session = Session()
    card_status_list = session.query(CardCrawlerStatusV2).filter(CardCrawlerStatusV2.dataset_id == dataset_id).all()
    session.close()
    return card_status_list


def query_card_crawler_log_one(card_id: str):
    session = Session()
    card_status = session.query(CardCrawlerStatusV2).filter(CardCrawlerStatusV2.card_id == card_id).first()
    session.close()
    return card_status


def write_card_crawler_log(dataset_id: str, card_id: str, category: str):
    session = Session()
    with session.begin():
        card_status = CardCrawlerStatusV2(dataset_id=dataset_id, card_id=card_id, category=category)
        session.add(card_status)
    session.close()


def get_total_cards_count():
    session = Session()
    count = session.query(CardV2).count()
    session.close()
    return count


def query_card_crawler_status(card_id: str):
    session = Session()
    card_status = session.query(CardCrawlerStatusV2).filter(CardCrawlerStatusV2.card_id == card_id).first()
    session.close()
    return card_status
