from dataclasses import dataclass
from datetime import datetime


@dataclass
class DateRange:
    startDate: str or datetime
    endDate: str or datetime


@dataclass
class DayPrice:
    time_open: str or datetime
    close: str or datetime


@dataclass
class DatabaseRow:
    coin: str
    time_open: datetime or str
    close: float

    def __init__(self, coin, time_open, close):
        self.close = close
        self.time_open = time_open
        self.coin = coin

    def trim_time_open(self):
        self.time_open = self.time_open[:-13]


@dataclass
class PriceIncreaseRange:
    date_from: datetime or str
    date_till: datetime or str
    price_increase: float

    def __init__(self, date_from, date_till, price_increase: float):
        self.price_increase = price_increase
        self.date_till = date_till
        self.date_from = date_from

    def update_date_from(self, new_date_from):
        self.date_from = new_date_from

    def update_date_till(self, new_date_till):
        self.date_till = new_date_till

    def update_price_increase(self, new_price_increase):
        self.price_increase = new_price_increase

    def update_all(
        self, new_date_from=None, new_date_till=None, new_price_increase=None
    ):
        if new_date_from is not None:
            self.date_from = new_date_from
        if new_date_till is not None:
            self.date_till = new_date_till
        if new_price_increase is not None:
            self.price_increase = new_price_increase
