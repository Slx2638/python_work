from demo import db


class Train(db.Model):
    __tablename__ = 'train'
    train_id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    record_id = db.Column(db.Integer, db.ForeignKey('record.record_id'))
    train_status = db.Column(db.Integer)

    name_price = db.Column(db.PickleType)
    dish_num = db.Column(db.Integer)
