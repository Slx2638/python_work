from demo import db

class Dish_image(db.Model):
    __tablename__ = 'dish_image'
    image_id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))



db.create_all()