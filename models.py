from peewee import *
import datetime

db = SqliteDatabase("file.db")


class File(Model):
    id = PrimaryKeyField(null=False)
    name = CharField(unique=True)
    file_id = CharField(unique=True)
    chat_id = CharField()

    created = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db
        order_by = ('created',)