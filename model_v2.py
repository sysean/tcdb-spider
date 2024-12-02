import logging
from datetime import datetime
from dataclasses import dataclass
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column, relationship, joinedload, contains_eager, selectinload
from sqlalchemy import String, DateTime, Integer, Boolean, ForeignKey, func
from sqlalchemy.orm import declarative_base

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


@dataclass
class DatasetV2(Base, TimestampMixin):
    __tablename__ = "dataset_v2"

    id: Mapped[str] = mapped_column(primary_key=True)  # 主键: category_sid
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    set_name: Mapped[str] = mapped_column(String(512), nullable=False)
    rating: Mapped[str] = mapped_column(String(64), nullable=True)
    total_cards: Mapped[int] = mapped_column(Integer, nullable=False)
    release_dates: Mapped[str] = mapped_column(String(1024), nullable=True)
    set_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    category: Mapped[str] = mapped_column(String(128), nullable=False)
    is_empty: Mapped[bool] = mapped_column(Boolean, nullable=True)

    cards: Mapped[List['CardV2']] = relationship('CardV2', back_populates='dataset')


@dataclass
class CardV2(Base, TimestampMixin):
    __tablename__ = "card_v2"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)  # 使用 sid-cid 作为主键
    dataset_id: Mapped[str] = mapped_column(String, ForeignKey('dataset_v2.id'), nullable=False)
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

    dataset: Mapped['DatasetV2'] = relationship('DatasetV2', back_populates='cards')


@dataclass
class CardCrawlerStatusV2(Base, TimestampMixin):
    __tablename__ = "card_crawler_status_v2"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String(128), nullable=False)
    dataset_id: Mapped[str] = mapped_column(String, nullable=False)
    card_id: Mapped[str] = mapped_column(String(255), nullable=False)
