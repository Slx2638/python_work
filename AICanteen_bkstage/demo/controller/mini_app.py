from demo import app, db
from flask import request, jsonify
from demo.model.Dish_type import Dish_type
from demo.model.Dish import Dish
from demo.model.Shop import Shop
from demo.model.Record import Record
from demo.model.Train import Train
from demo.model.Dish_image import Dish_image
from demo.model.Shop_owner import Shop_owner
from demo.model.Staff import Staff
import json, os, time
from datetime import datetime

path = 'D:'


def get_image_name(url):
    name = os.path.splitext(url)[0]
    image_id = name.split('/')[-1]
    return image_id


def get_timestamp():
    return round(time.time() * 1000)


def get_type_attr(dish_types):
    """获取菜品类别属性"""
    dish_type = [{'type_id': 0, 'type_name': '全部'}]
    for type in dish_types:
        temp = {}
        temp['type_id'] = type.type_id
        temp['type_name'] = type.type_name
        dish_type.append(temp)
    return dish_type


def get_shop_attr(shop_info):
    shop = {}
    shop['shop_id'] = shop_info.shop_id
    shop['shop_name'] = shop_info.name
    shop['address'] = shop_info.address
    shop['info'] = shop_info.info
    shop['url'] = shop_info.url
    return shop



def get_dish_attr(dishes, shop_id):
    """获取菜品属性"""
    res = []
    for dish in dishes:
        temp = {}
        temp['dish_id'] = dish.dish_id
        temp['dish_name'] = dish.dish_name
        temp['price'] = str('%.2f' % dish.price)
        temp['type_id'] = dish.type_id
        temp['status'] = dish.status
        temp['urls'] = get_url(dish, shop_id)
        temp['selected'] = False
        res.append(temp)
    return res


def get_train_dish(dish,shop_id):
    temp = {}
    print("did",dish.dish_id)
    temp['dish_id'] = dish.dish_id
    temp['dish_name'] = dish.dish_name
    temp['price'] = str('%.2f' % dish.price)
    temp['type_id'] = dish.type_id
    temp['status'] = dish.status
    temp['urls'] = get_url(dish, shop_id)
    temp['selected'] = False
    return temp



def get_train_attr(trains):
    """训练数据信息"""
    res = []

    for train, record in trains:
        temp = {}
        temp['train_id'] = train.train_id
        temp['time'] = train.time.strftime("%Y-%d-%m %H:%M:%S")
        temp['record_id'] = train.record_id
        temp['status'] = record.status
        temp['trained'] = train.train_status

        if record.user_id is not None:
            temp['user_id'] = record.user_id
            temp['identity'] = 0
        else:
            temp['user_id'] = record.staff_id
            temp['identity'] = 1

        name_price = train.name_price
        dict = json.loads(name_price)

        dishes = []
        for key,values in dict.items():
            dish = Dish.query.filter(Dish.dish_name==key,Dish.price==values).first()
            result = get_train_dish(dish, record.shop_id)
            dishes.append(result)

        temp['dishes'] = dishes
        res.append(temp)

    return res


def get_record_attr(records):
    res = []
    for record in records:
        temp = {}
        temp['record_id'] = record.record_id
        temp['datetime'] = record.datetime.strftime("%Y-%m-%d %H:%M:%S")
        temp['status'] = record.status
        if record.user_id is not None:
            temp['user_id'] = record.user_id
            temp['identity'] = 1
        else:
            temp['user_id'] = record.staff_id
            temp['identity'] = 0

        # 获取每条记录对应的菜品信息
        dishes = Dish.query.join(Record).filter_by(record_id=record.record_id).all()
        # print(dishes)
        dish = get_dish_attr(dishes, record.shop_id)
        temp['dishes'] = dish
        res.append(temp)
    return res


def get_url(dish, shop_id):
    dir_path = path + '//static/food_images/' + str(shop_id) + '/rawPics'
    imgs = os.listdir(dir_path + '/' + dish.dish_name)
    image_list = []
    for img in imgs:
        url = dir_path + '/' + dish.dish_name + '/' + img
        image_list.append(url)
    return image_list




@app.route("/get_dish_type")
def get_dish_type():

    dish_types = db.session.query(Dish_type).all()
    dish_type = get_type_attr(dish_types)
    return jsonify(dish_type)



@app.route('/get_dishes')
def get_dishes():
    """获取该店所有菜品，重复则取最新日期的"""
    shop_id = request.values.get('shop_id')
    dishes = Dish.query.join(Record).filter_by(shop_id=shop_id).order_by(Record.datetime.desc()).all()
    new_dishes = []
    name = []
    new_name = []
    for dish in dishes:
        name.append(dish.dish_name)
    for dish in dishes:
        if dish.dish_name not in new_name:
            new_name.append(dish.dish_name)
            new_dishes.append(dish)
    res = get_dish_attr(new_dishes, shop_id)
    return jsonify(res)


@app.route('/find_dishes')
def find_dishes():
    keyword = request.values.get('keyword')
    shop_id = request.values.get('shop_id')
    dishes = Dish.query.join(Record).filter(Dish.dish_name.like('%' + keyword + '%'), Record.shop_id == shop_id).all()
    res = get_dish_attr(dishes)
    return res


@app.route('/shop_info')
def get_shop_info():
    shop_id = request.values.get('shop_id')
    xx = Shop.query.filter_by(shop_id=shop_id).first()
    res = get_shop_attr(xx)
    return jsonify(res)


@app.route('/get_train_info')
def get_train_info():
    shop_id = request.values.get('shop_id')
    trains = db.session.query(Train, Record).join(Record).filter(Record.shop_id == shop_id,
                                                                 Record.status == 2).order_by(Train.time.desc()).all()
    res = get_train_attr(trains)
    print('train:', res)
    return jsonify(res)


@app.route('/get_record_info')
def get_record_info():
    shop_id = request.values.get('shop_id')
    record = Record.query.filter_by(shop_id=shop_id).order_by(Record.datetime.desc()).all()
    res = get_record_attr(record)
    return jsonify(res)


@app.route('/generate_record')
def generate_record():
    new_foods = request.values.get('new_foods')
    new_foods = json.loads(new_foods)
    user_id = request.values.get('user_id')
    shop_id = request.values.get('shop_id')
    identity = request.values.get('identity')
    new_record = Record()
    new_record.record_id = get_timestamp()
    new_record.datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if identity == str(1):
        new_record.user_id = user_id
    else:
        new_record.staff_id = user_id
    new_record.shop_id = shop_id
    db.session.add(new_record)
    flag = 0
    for i, dish in enumerate(new_foods):
        new_dish = Dish()
        new_dish.dish_id = get_timestamp() + i
        new_dish.dish_name = dish['dish_name']
        new_dish.price = dish['price']
        new_dish.shop_id = shop_id
        new_dish.record_id = new_record.record_id
        new_dish.type_id = dish['type_id']
        if new_dish.price is not None:
            new_dish.status = 1
        else:
            new_dish.status = 0
            flag = 1
        # 图片表
        print('urls:', dish['urls'])
        dish_url = []
        for j, img in enumerate(dish['urls']):
            image = Dish_image()
            image.image_id = get_timestamp() + i * 9 + j
            image.url = img
            dish_url.append(image.image_id)
            db.session.add(image)
        new_dish.url = dish_url
        db.session.add(new_dish)
    if flag:
        new_record.status = 0
    else:
        new_record.status = 1
    db.session.commit()
    return 'success'


@app.route('/get_images', methods=['get', 'post'])
def get_images():
    file = request.files.get('file')
    suffix = request.values.get('suffix')
    name = request.values.get('name')
    shop_id = request.values.get('shop_id')
    save_dir = path + '//static/food_images/' + str(shop_id) + '/rawPics/' + name
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    filename = save_dir + '/' + str(round(time.time() * 1000)) + '.' + suffix
    file.save(filename)
    return filename


@app.route('/login2', methods=['get', 'post'])
# def login2():
def login2():
    username = request.values.get('username')
    password = request.values.get('password')
    res = {}
    flag = 0
    identity = 1
    user = Shop_owner.query.get(username)
    if user is None:
        user = Staff.query.get(username)
        if password == user.password:
            flag = 1
        identity = 0

    if password == user.password:
        flag = 1
    if user is not None and flag:
        res['shop_id'] = user.shop_id
        res['identity'] = identity
        res['flag'] = flag
    if flag == 0:
        res['flag'] = flag
    return jsonify(res)
    username = request.values.get('username')
    password = request.values.get('password')
    res = {}
    flag = 0
    identity = 1
    user = Shop_owner.query.get(username)
    if password == user.password:
        flag = 1
    if user is None:
        user = Staff.query.get(username)
        if password == user.password:
            flag = 1
        identity = 0
    if user is not None and flag:
        res['shop_id'] = user.shop_id
        res['identity'] = identity
    return jsonify(res)




