from demo import db

class Order_info(db.Model):
    __tablename__ = "order_info"
    info_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer)
    dish_id = db.Column(db.Integer)

db.create_all()