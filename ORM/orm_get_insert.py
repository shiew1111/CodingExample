from datetime import datetime

from peewee import chunked

from ORM.orm_model import PriceAndDate, db
from data_classes import DatabaseRow


class CoinsDatabase:
    """It, contains get() and insert() method's, which are responsible for selecting, and inserting data from sqlite database.
    It's build on Peewee framework."""

    @db.connection_context()
    def __init__(self):
        db.create_tables([PriceAndDate], safe=True)

    @staticmethod
    @db.connection_context()
    def get(coin, startDate, endDate):
        return [
            DatabaseRow(
                time_open=datetime.strftime(row["time_open"], "%Y-%m-%dT%H:%M:%SZ"),
                close=row["close"],
                coin=coin,
            )
            for row in PriceAndDate.select(PriceAndDate.time_open, PriceAndDate.close)
            .where(
                PriceAndDate.time_open >= datetime.strptime(startDate, "%Y-%m-%d"),
                PriceAndDate.time_open <= datetime.strptime(endDate, "%Y-%m-%d"),
                PriceAndDate.coin == coin,
            )
            .order_by(PriceAndDate.time_open.asc())
            .dicts()
        ]

    @staticmethod
    @db.connection_context()
    def insert(dataSource, coinName):
        with db.atomic():
            for batch in chunked(
                [
                    {
                        "coin": coinName,
                        "time_open": datetime.strptime(
                            row.time_open, "%Y-%m-%dT%H:%M:%SZ"
                        ),
                        "close": row.close,
                    }
                    for row in dataSource
                ],
                100,
            ):
                PriceAndDate.insert_many(batch).execute()
