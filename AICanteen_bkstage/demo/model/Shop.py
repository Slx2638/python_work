from demo import db


class Shop(db.Model):
    __tablename__ = 'shop'
    shop_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)
    address = db.Column(db.String(20))
    info = db.Column(db.String(20))
    url = db.Column(db.String(20))

    key1 = db.relationship('Dish_type', backref='type', lazy='dynamic')      # backref的值不能与外键属性同名
    key2 = db.relationship('Dish', backref='d', lazy='dynamic')
    key3 = db.relationship('Record', backref='record', lazy='dynamic')

    key4 = db.relationship('Order', backref='order', lazy='dynamic')
db.create_all()
