from demo import db


class Shop_owner(db.Model):
    __tablename__ = 'shop_owner'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(20), unique=True)
    shop_id = db.Column(db.Integer)
    wx_id = db.Column(db.String(20))