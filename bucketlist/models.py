from bucketlist import database
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os


class User(database.Model):
    __tablename__ = 'users' # table name given during migration

    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(256), nullable=False, unique=True)
    password = database.Column(database.String(256), nullable=False)
    admin = database.Column(database.Boolean)
    bucketlists = database.relationship('Bucketlist', order_by='Bucketlist.id', cascade="all, delete-orphan")

    def __init__(self, email, admin, password=[]):
        self.email = email
        self.password = generate_password_hash(password, method='sha256')
        self.admin = admin

    def is_password_valid(self, given_password):
        return check_password_hash(self.password, given_password)

    def save(self):
        database.session.add(self)
        database.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()


class Bucketlist(database.Model):

    __tablename__ = 'bucketlists'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255))
    date_created = database.Column(database.Time, default=database.func.current_timestamp())
    date_modified = database.Column(
        database.DateTime, default=database.func.current_timestamp(),
        onupdate=database.func.current_timestamp()
    )
    created_by = database.Column(database.Integer, database.ForeignKey(User.id))

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by

    def save(self):
        database.session.add(self)
        database.session.commit()

    @staticmethod
    def get_all():
        return Bucketlist.query.all()

    def delete(self):
        database.session.delete(self)
        database.session.commit()

    def __repr__(self):
        return "<Bucketlis: {}>".format(self.name)



# class BucketlistActivity(database.Model):
#     pass
