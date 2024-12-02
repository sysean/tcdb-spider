import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from model_v2 import DatasetV2, CardV2, CardCrawlerStatusV2

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
