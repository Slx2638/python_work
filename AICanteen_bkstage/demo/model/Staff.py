from demo import db


class Staff(db.Model):
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shop_id = db.Column(db.Integer, unique=True)
    password = db.Column(db.String(20))
    permission = db.Column(db.Integer)
    wx_id = db.Column(db.String(20))
