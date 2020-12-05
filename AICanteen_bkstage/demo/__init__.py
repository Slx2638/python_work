from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,static_folder='D://static')
app.secret_key = 'aabbccddee'
app.config.from_object('demo.setting')
# 数据库对象
db = SQLAlchemy(app)

from demo.model import Dish, Dish_type, Dish_image, Order, Order_info, Record, Shop_owner, Shop, Train

from demo.controller import  mini_app,index
