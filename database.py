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
    
class Family(Model):
    from_user = ForeignKeyField(User,backref="family")
    to_user = ForeignKeyField(User,backref="family")

    class Meta:
        database = db

class Shelter(Model):
    name = CharField()
    address = CharField()
    category = CharField()
    capacity = CharField()
    phone_number = CharField()

    class Meta:
        database = db

class Hospital(Model):
    name = CharField()
    address = CharField()
    category = CharField()
    capacity = CharField()
    phone_number = CharField()

    class Meta:
        database = db

class Pharmacy(Model):
    name = CharField()
    address = CharField()
    capacity = CharField()
    phone_number = CharField()

    class Meta:
        database = db

class ReliefSuppliesCateogy(Model):
    name = CharField()

    class Meta:
        database = db

class ReliefSupplies(Model):
    shelter = ForeignKeyField(Shelter,backref="reliefsupplies")
    reliefsuppliescateogy = ForeignKeyField(ReliefSuppliesCateogy,backref="reliefsuppliescateogy")
    required_number = IntegerField()
    used_number = IntegerField()


    class Meta:
        database = db

class Knowledge(Model):
    question = CharField()
    answwer = CharField()

    class Meta:
        database = db

db.create_tables([User,Family])
