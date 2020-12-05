from demo import db


class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(20))
    status = db.Column(db.Integer)
