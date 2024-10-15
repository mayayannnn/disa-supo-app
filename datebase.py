from peewee import *

db = SqliteDatabase('disa_supo.db')

class User(Model):
    line_id = CharField()
    name = CharField()
    address = CharField()
    birthday = DateField()
    gender = CharField()

    class Meta:
        database = db
    
db.create_tables([User])