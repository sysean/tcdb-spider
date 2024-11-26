import logging
from datetime import datetime
from dataclasses import dataclass
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column, relationship, joinedload, contains_eager, selectinload
from sqlalchemy import String, DateTime, Text, create_engine, Integer, Boolean, ForeignKey, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

Base = declarative_base()


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


"""
dataset json example:

{
    "id": 462124,
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


@dataclass
class Dataset(Base, TimestampMixin):
    __tablename__ = "dataset"

    id: Mapped[int] = mapped_column(primary_key=True)  # 使用 sid 作为主键
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    set_name: Mapped[str] = mapped_column(String(512), nullable=False)
    rating: Mapped[str] = mapped_column(String(64), nullable=True)
    total_cards: Mapped[int] = mapped_column(Integer, nullable=False)
    release_dates: Mapped[str] = mapped_column(String(1024), nullable=True)
    set_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    is_empty: Mapped[bool] = mapped_column(Boolean, nullable=True)

    cards: Mapped[List['Card']] = relationship('Card', back_populates='dataset')


"""
card example:

{
    "index": 0,
    "name": "NNO Robert Acton",
    "team": "Harvard Crimson",
    "card_num": "11",
    "sub_set": "Chrome",
    "player_url": "/ViewCard.cfm/sid/462124/cid/26386897/2024-Donruss-3-Jerry-Jeudy?PageIndex=1",
    "front_img": "124068/124068-8374444Fr.jpg",
    "back_img": "124068/124068-8374444Bk.jpg",
    "front_submitted_time": "Front submitted by styxscottii on 12/8/2021",
    "back_submitted_time": "Back submitted by styxscottii on 12/8/2021",
    "price": "Submit a Price"
}
"""


@dataclass
class Card(Base, TimestampMixin):
    __tablename__ = "card"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)  # 使用 sid-cid 作为主键
    dataset_id: Mapped[int] = mapped_column(Integer, ForeignKey('dataset.id'), nullable=False)
    index: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    team: Mapped[str] = mapped_column(String(512), nullable=False)
    card_num: Mapped[str] = mapped_column(String(64), nullable=True)
    sub_set: Mapped[str] = mapped_column(String(128), nullable=True)
    player_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    front_img: Mapped[str] = mapped_column(String(512), nullable=True)
    back_img: Mapped[str] = mapped_column(String(512), nullable=True)
    front_submitted_time: Mapped[str] = mapped_column(String(128), nullable=True)
    back_submitted_time: Mapped[str] = mapped_column(String(128), nullable=True)
    price: Mapped[str] = mapped_column(String(128), nullable=True)

    dataset: Mapped['Dataset'] = relationship('Dataset', back_populates='cards')


@dataclass
class CardCrawlerStatus(Base, TimestampMixin):
    __tablename__ = "card_crawler_status"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dataset_id: Mapped[int] = mapped_column(Integer, nullable=False)
    card_id: Mapped[str] = mapped_column(String(255), nullable=False)


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
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


# 插入 Dataset 数据，输入为 dict
def insert_dataset(data: dict):
    session = Session()
    dataset = session.query(Dataset).filter(Dataset.id == data['id']).first()
    if dataset:
        for key, value in data.items():
            setattr(dataset, key, value)
    else:
        dataset = Dataset(**data)
        session.add(dataset)
    session.commit()
    session.close()


# 查询 Dataset 数据，输入为 sid
def query_dataset(sid: int):
    session = Session()
    dataset = session.query(Dataset).filter(Dataset.id == sid).first()
    session.close()
    return dataset


# 插入 Card 数据，输入为 dict
def insert_card(data: dict):
    try:
        session = Session()
        card = Card(**data)
        session.add(card)
        session.commit()
        session.close()
    except IntegrityError as e:
        logging.error(f"IntegrityError: {e}")
        return


def get_card_count(sid: int):
    session = Session()
    count = session.query(Card).filter(Card.dataset_id == sid).count()
    session.close()
    return count


def get_cnt_for_database(start_year: int, end_year: int):
    session = Session()
    return session.query(Dataset).filter(Dataset.is_empty == False,
                                         Dataset.total_cards > 0,
                                         Dataset.year >= start_year,
                                         Dataset.year <= end_year
                                         ).count()


# 迭代 Dataset 数据
def iterate_datasets_with_cards(cnt: int, start_year: int, end_year: int):
    session = Session()
    try:
        query = session.query(Dataset).options(
            selectinload(Dataset.cards)
        ).filter(
            Dataset.is_empty == False,
            Dataset.total_cards > 0,
            Dataset.year >= start_year,
            Dataset.year <= end_year
        ).order_by(Dataset.year.desc()).yield_per(cnt)
        for dataset in query:
            dataset.cards.sort(key=lambda card: card.index)
            yield dataset
    finally:
        session.close()


# 根据 dataset_id 查询 CardCrawlerLog
def query_card_crawler_log(dataset_id: int):
    session = Session()
    card_status_list = session.query(CardCrawlerStatus).filter(CardCrawlerStatus.dataset_id == dataset_id).all()
    session.close()
    return card_status_list


def write_card_crawler_log(dataset_id: int, card_id: str):
    session = Session()
    card_status = CardCrawlerStatus(dataset_id=dataset_id, card_id=card_id)
    session.add(card_status)
    session.commit()
    session.close()


def get_total_cards_count():
    session = Session()
    count = session.query(Card).count()
    session.close()
    return count
