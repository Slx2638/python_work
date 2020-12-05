from demo import db


class Dish(db.Model):
    __tablename__ = 'dishes'
    dish_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dish_name = db.Column(db.String(20), unique=True)
    price = db.Column(db.DECIMAL)
    record_id = db.Column(db.Integer, db.ForeignKey('record.record_id'))
    status = db.Column(db.Integer, db.ForeignKey('shop.shop_id'))
    shop_id = db.Column(db.Integer)
    url = db.Column(db.PickleType)

    #增加一列，外键列，引自user表的主键id user和book 1 ： N
    # ownerid = db.Column(db.Integer, db.ForeignKey('user.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('dish_type.type_id'))

db.create_all()