from demo import db

class Order(db.Model):
    __tablename__ = "order"
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_price = db.Column(db.DECIMAL)
    time = db.Column(db.DATETIME)
    dishes = db.Column(db.PickleType)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.shop_id'))
    pay_status = db.Column(db.String)
    pay_way = db.Column(db.String)
    model_version = db.Column(db.Integer)

db.create_all()


