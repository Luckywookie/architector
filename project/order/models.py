from project.db import db


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    total_cost = db.Column(db.Numeric(precision=12, scale=8), default=0)
    total_amount = db.Column(db.Integer)
    delivery = db.Column(db.Numeric(precision=12, scale=8))


class OrderProducts(db.Model):
    __tablename__ = 'order_product'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), index=True)
    cost = db.Column(db.Numeric(precision=12, scale=8))
    amount = db.Column(db.Integer)
