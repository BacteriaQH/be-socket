from flask_mongoengine import Document
from mongoengine import StringField, IntField, ListField, BooleanField, DateField

import datetime
import pytz


class Users(Document):
    name = StringField(require=True)
    email = StringField(require=True)
    password = StringField(require=True)
    age = IntField()
    address = StringField()
    isAdmin = IntField(default=0)
    roleUnit = IntField(default=0)
    date_modified = DateField(default=datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')))

    def to_json(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "age": self.age,
            "address": self.address,
            "isAdmin": self.isAdmin,
            "roleUnit": self.roleUnit,
            "date_modified": self.date_modified,
        }


class Units(Document):
    name = StringField(require=True)
    mst = StringField(require=True)
    address = StringField()
    user = ListField()
    admin = StringField()
    adminName = StringField()
    room_name = StringField()
    socket_id = StringField()
    date_modified = DateField(default=datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')))

    def to_json(self):
        return {
            "name": self.name,
            "mst": self.mst,
            "address": self.address,
            "user": self.user,
            "admin": self.admin,
            "room_name": self.room_name,
            "adminName": self.adminName,
            "socket_id": self.socket_id,
            "date_modified": self.date_modified,
        }


class Files(Document):
    code = StringField(require=True)
    name = StringField(require=True)
    link = StringField(require=True)
    createFileAt = DateField(default=datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')))
    createFileBy = StringField()
    isSign = BooleanField(default=False)
    signFileAt = StringField(default='')
    signFileBy = StringField(default=' ')
    date_modified = DateField(default=datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')))

    def to_json(self):
        return {
            "code": self.code,
            "name": self.name,
            "link": self.link,
            "createFileAt": self.createFileAt,
            "createFileBy": self.createFileBy,
            "isSign": self.isSign,
            "signFileAt": self.signFileAt,
            "signFileBy": self.signFileBy,
            "date_modified": self.date_modified,
        }


class Approves(Document):
    unit_id = StringField(require=True)
    user_id = StringField(require=True)
    user_approve = StringField(require=True)
    date_modified = DateField(default=datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')))

    def to_json(self):
        return {
            "unit_id": self.unit_id,
            "user_id": self.user_id,
            "user_approve": self.user_approve,
            "date_modified": self.date_modified,
        }
