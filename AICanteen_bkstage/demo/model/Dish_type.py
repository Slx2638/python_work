from demo import db

class Dish_type(db.Model):
    __tablename__ = 'dish_type'
    type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(20))
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.shop_id'))

    #指明关系,books不是一个字段，backref为Book添加了一个user属性，可以通过book.user查询用户信息,可以通过book找到所有者
    #同时也能通过user找到books
    # books = db.relationship('Book', backref='user', lazy='dynamic')



db.create_all()