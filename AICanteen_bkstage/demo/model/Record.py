from demo import db


class Record(db.Model):
    __tablename__ = 'record'
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime = db.Column(db.DateTime, unique=True)
    user_id = db.Column(db.Integer)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.shop_id'))
    staff_id = db.Column(db.Integer)
    status = db.Column(db.Integer)

    key1 = db.relationship('Dish', backref='dish', lazy='dynamic')      # backref的值不能与外键属性同名
    key2 = db.relationship('Train', backref='train', lazy='dynamic')