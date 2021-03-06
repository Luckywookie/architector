from auth.db import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    def __repr__(self):
        return '{}<{}>'.format(self.username, self.id)

    def to_dict(self):
        properties = ['user_id', 'username']
        return {prop: self.id if prop == 'user_id' else getattr(self, prop, None) for prop in properties}
