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
    bucketlists = database.relationship('Bucketlist', order_by='Bucketlist.id', cascade="all, delete-orphan",
                                        backref='user', lazy='dynamic')

    def __init__(self, email, admin, password=[]):
        self.email = email
        self.password = generate_password_hash(password, method='sha256')
        self.admin = admin

    def is_password_valid(self, given_password):
        return check_password_hash(self.password, given_password)

    def save(self):
        database.session.add(self)
        database.session.commit()


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
    items = database.relationship('BucketlistItem', backref='bucketlist', lazy='dynamic')

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
        return "<Bucketlist: {}>".format(self.name)



class BucketlistItem(database.Model):

    __tablename__ = 'bucketlist_items'

    item_id = database.Column(database.Integer, primary_key=True)
    item_name = database.Column(database.String(255))
    date_created = database.Column(database.Time, default=database.func.current_timestamp())
    date_modified = database.Column(
        database.DateTime, default=database.func.current_timestamp(),
        onupdate=database.func.current_timestamp()
    )
    done = database.Column(database.Boolean, default=False)
    complete_by = database.Column(database.DateTime)
    bucketlist_id = database.Column(database.Integer, database.ForeignKey(Bucketlist.id))

    def __init__(self, item_name, bucketlist, done, complete_by):
        self.item_name = item_name
        self.bucketlist_id = bucketlist
        self.done = done
        self.complete_by = complete_by

    def save(self):
        database.session.add(self)
        database.session.commit()

    @staticmethod
    def get_bucketlist_items(id):
        return BucketlistItem.query.filter_by(id=id).first()

    def delete(self):
        database.session.delete(self)
        database.session.commit()

    def __repr__(self):
        return "<BucketlistItem: {}>".format(self.item_name)


