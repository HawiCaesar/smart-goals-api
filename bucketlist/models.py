from bucketlist import database


# class User(database.Model):
#     pass


class Bucketlist(database.Model):

    __tablename__ = 'bucketlists'
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255))
    date_created = database.Column(database.Time, default=database.func.current_timestamp())
    date_modified = database.Column(
        database.DateTime, default=database.func.current_timestamp(),
        onupdate=database.func.current_timestamp()
    )

    def __init__(self, name):
        self.name = name

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
