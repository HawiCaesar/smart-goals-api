from bucketlist import database
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from flask import make_response, jsonify


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
    date_created = database.Column(database.DateTime, default=database.func.current_timestamp())
    date_modified = database.Column(
        database.DateTime, default=database.func.current_timestamp(),
        onupdate=database.func.current_timestamp()
    )
    created_by = database.Column(database.Integer, database.ForeignKey(User.id))
    items = database.relationship('BucketlistItem', backref='bucketlist', lazy='dynamic')

    def __init__(self, name, created_by, date_created):
        self.name = name
        self.created_by = created_by
        self.date_created = date_created

    def save(self):
        database.session.add(self)
        database.session.commit()

    def delete(self):
        database.session.delete(self)
        database.session.commit()

    def __repr__(self):
        return "{} - {}".format(self.id, self.name)


class BucketlistItem(database.Model):

    __tablename__ = 'bucketlist_items'

    item_id = database.Column(database.Integer, primary_key=True)
    item_name = database.Column(database.String(255))
    date_created = database.Column(database.TIMESTAMP, default=database.func.current_timestamp())
    date_modified = database.Column(database.DateTime, default=database.func.current_timestamp(),
                                    onupdate=database.func.current_timestamp())
    done = database.Column(database.Boolean, default=False)
    complete_by = database.Column(database.DateTime)
    bucketlist_id = database.Column(database.Integer, database.ForeignKey(Bucketlist.id))


    def save(self):
        database.session.add(self)
        database.session.commit()

    @staticmethod
    def get_bucketlist_items(id, item_id, user):
        return BucketlistItem.query.filter_by(bucketlist_id=id, item_id=item_id)\
            .join(Bucketlist, BucketlistItem.bucketlist_id == Bucketlist.id)\
            .filter_by(created_by=user).first()

    def delete(self):
        database.session.delete(self)
        database.session.commit()

    def __repr__(self):
        return "<BucketlistItem: {}>".format(self.item_name)


def get_paginated_list(url, model, searchterm, user, bucketlist_id, start, limit):

        if model == 'bucketlist':

            if searchterm is None:
                results = Bucketlist.query.filter_by(created_by=user).all()
            else:
                searchterm = '%'+searchterm+'%'
                results = Bucketlist.query.filter(Bucketlist.name.like(searchterm)).filter_by(created_by=user).all()

        elif model == 'bucketlist_item':
            if searchterm is None:
                results = BucketlistItem.query.filter_by(bucketlist_id=bucketlist_id).all()

            else:
                searchterm = '%'+searchterm+'%'
                results = BucketlistItem.query.\
                    filter_by(bucketlist_id=bucketlist_id).\
                    filter(BucketlistItem.item_name.like(searchterm)).\
                    join(Bucketlist, BucketlistItem.bucketlist_id == Bucketlist.id).\
                    filter_by(created_by=user).all()

        # check if page exists
        count = len(results)
        if count < start:
            return {"status": "Fail", "message": "Page Not Found"}

        # make response
        obj = {}
        obj['start'] = start
        obj['limit'] = limit
        obj['count'] = count
        # make URLs
        # make previous url
        if start == 1:
            obj['previous'] = ''
        else:
            obj['previous'] = url + '?start=%d&limit=%d' % (start - 1, limit)
        # make next url
        if start + limit > count:
            obj['next'] = ''
        else:
            start_copy = start + 1
            obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
        # finally extract result according to bounds
        obj['results'] = results[(start - 1):(start - 1 + limit)]
        return obj


