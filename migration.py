from loguru import logger

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

# from save_db import Dataset, Card, CardCrawlerStatus
from model_v2 import Base, DatasetV2, CardV2, CardCrawlerStatusV2


def create_v2_table():
    pg_engine = create_engine(
        'postgresql+psycopg://postgres:%L%sFxL3}3aKG4al}ZFBFQj-iT.h@tcdb-crawler-db.cluster-c0xt5dijvnyu.us-east-2.rds.amazonaws.com:5432/tcdb',
        echo=True,
        pool_size=20,
        max_overflow=10,
        poolclass=QueuePool)

    Base.metadata.create_all(pg_engine)


# create_v2_table()

# def migrate_dataset():
#     mysql_engine = create_engine(
#         'mysql+pymysql://sean_123:43XLpZssa*Py_!L@rm-2vc52f63lasvix4w7po.mysql.cn-chengdu.rds.aliyuncs.com:3306/tcdb',
#         echo=True)
#
#     pg_engine = create_engine(
#         'postgresql+psycopg://postgres:%L%sFxL3}3aKG4al}ZFBFQj-iT.h@tcdb-crawler-db.cluster-c0xt5dijvnyu.us-east-2.rds.amazonaws.com:5432/tcdb',
#         echo=True,
#         pool_size=20,
#         max_overflow=10,
#         poolclass=QueuePool)
#     PgSession = sessionmaker(bind=pg_engine)
#     pg_session = PgSession()
#
#     MysqlSession = sessionmaker(bind=mysql_engine)
#     mysql_session = MysqlSession()
#
#     try:
#         batch_size = 10
#         query = mysql_session.query(Dataset).yield_per(batch_size)
#         batch = []
#
#         for dataset in query:
#             # Create DatasetV2 object
#             dataset_v2 = DatasetV2(
#                 id=str("Football_" + str(dataset.id)),
#                 year=dataset.year,
#                 set_name=dataset.set_name,
#                 rating=dataset.rating,
#                 total_cards=dataset.total_cards,
#                 release_dates=dataset.release_dates,
#                 set_url=dataset.set_url,
#                 category=dataset.category,
#                 is_empty=dataset.is_empty
#             )
#
#             batch.append(dataset_v2)
#
#             if len(batch) == batch_size:
#                 pg_session.add_all(batch)
#                 pg_session.commit()
#                 batch.clear()
#
#         # Insert remaining records
#         if batch:
#             pg_session.add_all(batch)
#             pg_session.commit()
#
#     except Exception as e:
#         logger.error(f"Error migrating datasets: {e}")
#         pg_session.rollback()
#         raise e
#     finally:
#         mysql_session.close()
#         pg_session.close()
#

# migrate_dataset() # done


# def migrate_card():
#     mysql_engine = create_engine(
#         'mysql+pymysql://sean_123:43XLpZssa*Py_!L@rm-2vc52f63lasvix4w7po.mysql.cn-chengdu.rds.aliyuncs.com:3306/tcdb',
#         echo=True)
#
#     pg_engine = create_engine(
#         'postgresql+psycopg://postgres:%L%sFxL3}3aKG4al}ZFBFQj-iT.h@tcdb-crawler-db.cluster-c0xt5dijvnyu.us-east-2.rds.amazonaws.com:5432/tcdb',
#         echo=True,
#         pool_size=20,
#         max_overflow=10,
#         poolclass=QueuePool)
#     PgSession = sessionmaker(bind=pg_engine)
#     pg_session = PgSession()
#
#     MysqlSession = sessionmaker(bind=mysql_engine)
#     mysql_session = MysqlSession()
#
#     try:
#         batch_size = 100
#         query = mysql_session.query(Card).yield_per(batch_size)
#         batch = []
#
#         for card in query:
#             # Create CardV2 object
#             card_v2 = CardV2(
#                 id='Football_' + card.id,
#                 dataset_id=str("Football_" + str(card.dataset_id)),
#                 index=card.index,
#                 name=card.name,
#                 team=card.team,
#                 card_num=card.card_num,
#                 sub_set=card.sub_set,
#                 player_url=card.player_url,
#                 front_img=card.front_img,
#                 back_img=card.back_img,
#                 front_submitted_time=card.front_submitted_time,
#                 back_submitted_time=card.back_submitted_time,
#                 price=card.price
#             )
#
#             batch.append(card_v2)
#
#             if len(batch) == batch_size:
#                 pg_session.add_all(batch)
#                 pg_session.commit()
#                 batch.clear()
#
#         # Insert remaining records
#         if batch:
#             pg_session.add_all(batch)
#             pg_session.commit()
#
#     except Exception as e:
#         logger.error(f"Error migrating datasets: {e}")
#         pg_session.rollback()
#         raise e
#     finally:
#         mysql_session.close()
#         pg_session.close()


# migrate_card() # done

# dataset to dataset_v2
# def migrate_dataset_from_pg():
#     pg_engine = create_engine(
#         'postgresql+psycopg://postgres:%L%sFxL3}3aKG4al}ZFBFQj-iT.h@tcdb-crawler-db.cluster-c0xt5dijvnyu.us-east-2.rds.amazonaws.com:5432/tcdb',
#         echo=True,
#         pool_size=20,
#         max_overflow=10,
#         poolclass=QueuePool)
#     PgSession = sessionmaker(bind=pg_engine)
#     pg_session = PgSession()
#
#     try:
#         with pg_session.begin():
#             batch_size = 100
#             query = pg_session.query(Dataset).yield_per(batch_size)
#             batch = []
#
#             for dataset in query:
#                 # Create DatasetV2 object
#                 dataset_v2 = DatasetV2(
#                     id=str("Football_" + str(dataset.id)),
#                     year=dataset.year,
#                     set_name=dataset.set_name,
#                     rating=dataset.rating,
#                     total_cards=dataset.total_cards,
#                     release_dates=dataset.release_dates,
#                     set_url=dataset.set_url,
#                     category=dataset.category,
#                     is_empty=dataset.is_empty
#                 )
#
#                 batch.append(dataset_v2)
#
#                 if len(batch) == batch_size:
#                     pg_session.add_all(batch)
#                     batch.clear()
#
#             # Insert remaining records
#             if batch:
#                 pg_session.add_all(batch)
#
#     except Exception as e:
#         logger.error(f"Error migrating datasets: {e}")
#         raise e
#     finally:
#         pg_session.close()


# migrate_dataset_from_pg() # done


# card to card_v2
# def migrate_card_from_pg():
#     pg_engine = create_engine(
#         'postgresql+psycopg://postgres:%L%sFxL3}3aKG4al}ZFBFQj-iT.h@tcdb-crawler-db.cluster-c0xt5dijvnyu.us-east-2.rds.amazonaws.com:5432/tcdb',
#         echo=True,
#         pool_size=20,
#         max_overflow=10,
#         poolclass=QueuePool)
#     PgSession = sessionmaker(bind=pg_engine)
#     pg_session = PgSession()
#
#     try:
#         with pg_session.begin():
#             batch_size = 1000
#             query = pg_session.query(Card).yield_per(batch_size)
#             batch = []
#
#             for card in query:
#                 # Create CardV2 object
#                 card_v2 = CardV2(
#                     id='Football_' + card.id,
#                     dataset_id=str("Football_" + str(card.dataset_id)),
#                     index=card.index,
#                     name=card.name,
#                     team=card.team,
#                     card_num=card.card_num,
#                     sub_set=card.sub_set,
#                     player_url=card.player_url,
#                     front_img=card.front_img,
#                     back_img=card.back_img,
#                     front_submitted_time=card.front_submitted_time,
#                     back_submitted_time=card.back_submitted_time,
#                     price=card.price
#                 )
#
#                 batch.append(card_v2)
#
#                 if len(batch) == batch_size:
#                     pg_session.add_all(batch)
#                     batch.clear()
#
#             # Insert remaining records
#             if batch:
#                 pg_session.add_all(batch)
#     except Exception as e:
#         logger.error(f"Error migrating datasets: {e}")
#         raise e


# migrate_card_from_pg() # done

# def migrate_card_status_from_mysql():
#     mysql_engine = create_engine(
#         'mysql+pymysql://sean_123:43XLpZssa*Py_!L@rm-2vc52f63lasvix4w7po.mysql.cn-chengdu.rds.aliyuncs.com:3306/tcdb',
#         echo=True)
#
#     pg_engine = create_engine(
#         'postgresql+psycopg://postgres:%L%sFxL3}3aKG4al}ZFBFQj-iT.h@tcdb-crawler-db.cluster-c0xt5dijvnyu.us-east-2.rds.amazonaws.com:5432/tcdb',
#         echo=True,
#         pool_size=20,
#         max_overflow=10,
#         poolclass=QueuePool)
#     PgSession = sessionmaker(bind=pg_engine)
#     pg_session = PgSession()
#
#     MysqlSession = sessionmaker(bind=mysql_engine)
#     mysql_session = MysqlSession()
#
#     try:
#         with pg_session.begin():
#             batch_size = 1000
#             query = mysql_session.query(CardCrawlerStatus).yield_per(batch_size)
#             batch = []
#
#             for card_status in query:
#                 card_status_v2 = CardCrawlerStatusV2(
#                     category="Football",
#                     dataset_id=str("Football_" + str(card_status.dataset_id)),
#                     card_id='Football_' + card_status.card_id
#                 )
#
#                 batch.append(card_status_v2)
#
#                 if len(batch) == batch_size:
#                     pg_session.add_all(batch)
#                     batch.clear()
#
#             # Insert remaining records
#             if batch:
#                 pg_session.add_all(batch)
#     except Exception as e:
#         logger.error(f"Error migrating datasets: {e}")
#         raise e


# migrate_card_status_from_mysql() # done

# def migrate_card_status_from_pg():
#     pg_engine = create_engine(
#         'postgresql+psycopg://postgres:%L%sFxL3}3aKG4al}ZFBFQj-iT.h@tcdb-crawler-db.cluster-c0xt5dijvnyu.us-east-2.rds.amazonaws.com:5432/tcdb',
#         echo=True,
#         pool_size=20,
#         max_overflow=10,
#         poolclass=QueuePool)
#     PgSession = sessionmaker(bind=pg_engine)
#     pg_session = PgSession()
#
#     try:
#         with pg_session.begin():
#             batch_size = 1000
#             query = pg_session.query(CardCrawlerStatus).yield_per(batch_size)
#             batch = []
#
#             for card_status in query:
#                 card_status_v2 = CardCrawlerStatusV2(
#                     category="Football",
#                     dataset_id=str("Football_" + str(card_status.dataset_id)),
#                     card_id='Football_' + card_status.card_id
#                 )
#
#                 batch.append(card_status_v2)
#
#                 if len(batch) == batch_size:
#                     pg_session.add_all(batch)
#                     batch.clear()
#
#             # Insert remaining records
#             if batch:
#                 pg_session.add_all(batch)
#     except Exception as e:
#         logger.error(f"Error migrating datasets: {e}")
#         raise e

# migrate_card_status_from_pg() # done
