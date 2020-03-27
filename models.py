from peewee import *
import datetime

db = SqliteDatabase("file.db")


class File(Model):
    id = PrimaryKeyField(null=False)
    name = CharField()
    file_id = CharField()
    chat_id = CharField()

    updated = DateTimeField(default=datetime.datetime.now())
    created = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db
        order_by = ('created',)