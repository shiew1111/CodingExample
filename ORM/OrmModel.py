from peewee import SqliteDatabase, Model, TextField, AutoField, DateTimeField, FloatField

DATABASE = 'CoinsDatabase.db'

db = SqliteDatabase(DATABASE)


# {'time_open': '2017-07-25T00:00:00Z', 'close': 0.10587}


class BaseModel(Model):
    class Meta:
        database = db


class PriceAndDate(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    time_open = DateTimeField()
    close = FloatField()
    coin = TextField()
