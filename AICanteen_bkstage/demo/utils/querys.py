import os, uuid
from demo import app, db
from flask import request, jsonify, render_template, url_for, session, make_response
from demo.model.Dish_type import Dish_type
from demo.model.Dish import Dish
from demo.model.Dish_image import Dish_image
from demo.model.Shop import Shop
from demo.model.Record import Record
from demo.model.Order_info import Order_info
from demo.model.Order import Order
from sqlalchemy import and_
import datetime


def queryByShopname(shop):
    data = []
    records = Record.query.filter(Record.shop_id == shop.shop_id).all()
    print(records)
    for record in records:
        dishes = Dish.query.filter(Dish.record_id == record.record_id).all()
        for dish in dishes:
            # list = []
            dish_info = {}
            dish_info['dish_name'] = dish.dish_name
            dish_info['dish_id'] = dish.dish_id
            dish_info['dish_price'] = str(dish.price)
            # d_type = Dish_type.query.filter(Dish_type.type_id == dish.type_id).first()
            # dish_info['dish_type_name'] = d_type.type_name

            # record = Record.query.filter(Record.record_id == dish.record_id).first()
            dish_info['dish_time'] = record.datetime

            # shop = Shop.query.filter(Shop.shop_id == record.shop_id).first()
            dish_info['shop_name'] = shop.name
            dish_info['shop_address'] = shop.address
            dish_info['shop_id'] = shop.shop_id

            # sells = Order_info.query.filter(Order_info.dish_id == dish.dish_id).count()
            # dish_info['dish_sells'] = sells

            # print(dish_info)
            data.append(dish_info)
            print(data)
    # return jsonify({'message': "信息如下！", "data": data})
    return data


def queryByDishname(dishname):
    data = []
    #dishes = Dish.query.filter(Dish.dish_name == dishname).all()
    dishes = Dish.query.filter(Dish.dish_name.like("%"+dishname+"%")if dishname is not None else "").all()

    # dishes = Dish.query.join(Record).filter_by(shop_id=shop_id).order_by(Record.datetime.desc()).all()
    # dishes = Dish.query.join(Record).filter(Record.record_id == Dish.record_id).all()
    # print(dishes)
    for dish in dishes:
        # list = []
        dish_info = {}
        # dish_type = Dish_type.query.filter(Dish_type.type_id == dish.type_id).first()
        dish_info['dish_name'] = dish.dish_name
        dish_info['dish_id'] = dish.dish_id
        dish_info['dish_price'] = str(dish.price)
        # d_type = Dish_type.query.filter(Dish_type.type_id == dish.type_id).first()
        # dish_info['dish_type_name'] = d_type.type_name

        dish_info['dish_time'] = datetime.datetime.fromtimestamp(dish.record_id // 1000)

        record = Record.query.filter(Record.record_id == dish.record_id).first()
        shop = Shop.query.filter(Shop.shop_id == record.shop_id).first()
        dish_info['shop_name'] = shop.name
        dish_info['shop_address'] = shop.address
        dish_info['shop_id'] = record.shop_id

        # sells = Order_info.query.filter(Order_info.dish_id == dish.dish_id).count()
        # dish_info['dish_sells'] = sells

        data.append(dish_info)
        # print(data)
    # return jsonify({'message': "信息如下！", "data": data})
    return data


def queryByShopnameAndDishname(shop, dishname):
    data = []
    records = Record.query.filter(Record.shop_id == shop.shop_id).all()
    for record in records:
        dishes = Dish.query.filter(and_(Dish.record_id == record.record_id, Dish.dish_name == dishname)).all()
        for dish in dishes:
            # list = []
            dish_info = {}
            # dish_type = Dish_type.query.filter(Dish_type.type_id == dish.type_id).first()
            dish_info['dish_name'] = dish.dish_name
            dish_info['dish_id'] = dish.dish_id
            dish_info['dish_price'] = str(dish.price)
            # d_type = Dish_type.query.filter(Dish_type.type_id == dish.type_id).first()
            # dish_info['dish_type_name'] = d_type.type_name

            # record = Record.query.filter(Record.record_id == dish.record_id).first()
            dish_info['dish_time'] = record.datetime

            # shop = Shop.query.filter(Shop.shop_id == record.shop_id).first()
            dish_info['shop_name'] = shop.name
            dish_info['shop_address'] = shop.address
            dish_info['shop_id'] = shop.shop_id

            # sells = Order_info.query.filter(Order_info.dish_id == dish.dish_id).count()
            # dish_info['dish_sells'] = sells

            data.append(dish_info)
            print(data)
    # return jsonify({'message': "信息如下！", "data": data})
    return data


def queryByShopnameAndTime(shop, time, now):
    print("参数：", time)
    date_formmed = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
    range = date_formmed - datetime.timedelta(days=int(time))  # 截至时间，时间范围为res-now
    records = Record.query.join(Shop).filter(
        and_(Record.datetime >= range, Shop.shop_id == Record.shop_id)).all()  # 在时间范围内的所有记录

    data = []
    # records = Record.query.filter(Record.shop_id == shop.shop_id).all()
    print(records)
    for record in records:
        dishes = Dish.query.filter(Dish.record_id == record.record_id).all()
        for dish in dishes:
            # list = []
            dish_info = {}
            dish_info['dish_name'] = dish.dish_name
            dish_info['dish_id'] = dish.dish_id
            dish_info['dish_price'] = str(dish.price)
            # d_type = Dish_type.query.filter(Dish_type.type_id == dish.type_id).first()
            # dish_info['dish_type_name'] = d_type.type_name

            # record = Record.query.filter(Record.record_id == dish.record_id).first()
            dish_info['dish_time'] = record.datetime

            # shop = Shop.query.filter(Shop.shop_id == record.shop_id).first()
            dish_info['shop_name'] = shop.name
            dish_info['shop_address'] = shop.address
            dish_info['shop_id'] = shop.shop_id

            # sells = Order_info.query.filter(Order_info.dish_id == dish.dish_id).count()
            # dish_info['dish_sells'] = sells

            # print(dish_info)
            data.append(dish_info)
            print(data)
    # return jsonify({'message': "信息如下！", "data": data})
    return data


def queryByDishnameAndTime(dishname, time, now):
    print("参数：", time)
    print(dishname)
    date_formmed = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
    range = date_formmed - datetime.timedelta(days=int(time))  # 截至时间，时间范围为res-now

    records = Record.query.join(Dish).filter(Record.datetime >= range).all()

    data = []
    for record in records:
        dishes = Dish.query.filter(and_(Dish.record_id == record.record_id, Dish.dish_name == dishname)).all()
        for dish in dishes:
            # list = []
            dish_info = {}
            # dish_type = Dish_type.query.filter(Dish_type.type_id == dish.type_id).first()
            dish_info['dish_name'] = dish.dish_name
            dish_info['dish_id'] = dish.dish_id
            dish_info['dish_price'] = str(dish.price)
            # d_type = Dish_type.query.filter(Dish_type.type_id == dish.type_id).first()
            # dish_info['dish_type_name'] = d_type.type_name

            # record = Record.query.filter(Record.record_id == dish.record_id).first()
            dish_info['dish_time'] = record.datetime

            shop = Shop.query.filter(Shop.shop_id == record.shop_id).first()
            dish_info['shop_name'] = shop.name
            dish_info['shop_address'] = shop.address
            dish_info['shop_id'] = shop.shop_id

            # sells = Order_info.query.filter(Order_info.dish_id == dish.dish_id).count()
            # dish_info['dish_sells'] = sells

            data.append(dish_info)
            print(data)
    return data


def queryByShopnameAndDishnameAndTime(shop, dishname, time, now):
    print("参数：", time)
    date_formmed = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
    range = date_formmed - datetime.timedelta(days=int(time))  # 截至时间，时间范围为res-now
    records = Record.query.join(Shop).filter(
        and_(Record.datetime >= range, Shop.shop_id == Record.shop_id)).all()  # 在时间范围内的所有记录

    data = []
    # records = Record.query.filter(Record.shop_id == shop.shop_id).all()
    print(records)
    for record in records:
        dishes = Dish.query.filter(and_(Dish.record_id == record.record_id, Dish.dish_name == dishname)).all()
        for dish in dishes:
            # list = []
            dish_info = {}
            dish_info['dish_name'] = dish.dish_name
            dish_info['dish_id'] = dish.dish_id
            dish_info['dish_price'] = str(dish.price)
            # d_type = Dish_type.query.filter(Dish_type.type_id == dish.type_id).first()
            # dish_info['dish_type_name'] = d_type.type_name

            # record = Record.query.filter(Record.record_id == dish.record_id).first()
            dish_info['dish_time'] = record.datetime

            # shop = Shop.query.filter(Shop.shop_id == record.shop_id).first()
            dish_info['shop_name'] = shop.name
            dish_info['shop_address'] = shop.address
            dish_info['shop_id'] = shop.shop_id

            # sells = Order_info.query.filter(Order_info.dish_id == dish.dish_id).count()
            # dish_info['dish_sells'] = sells

            # print(dish_info)
            data.append(dish_info)
            print(data)
    # return jsonify({'message': "信息如下！", "data": data})
    return data


def queryByTime(time, now):  # time 时间范围 now 现在的时间
    print("参数:", time)
    data = []
    date_formmed = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
    range = date_formmed - datetime.timedelta(days=int(time))  # 截至时间，时间范围为res-now
    print(range)
    records = Record.query.filter(Record.datetime >= range).all()  # 在时间范围内的所有记录
    for record in records:
        dishes = Dish.query.filter(Dish.record_id == record.record_id).all()
        for dish in dishes:
            # list = []
            dish_info = {}
            # dish_type = Dish_type.query.filter(Dish_type.type_id == dish.type_id).first()
            dish_info['dish_name'] = dish.dish_name
            dish_info['dish_id'] = dish.dish_id
            dish_info['dish_price'] = str(dish.price)
            # d_type = Dish_type.query.filter(Dish_type.type_id == dish.type_id).first()
            # dish_info['dish_type_name'] = d_type.type_name

            # record = Record.query.filter(Record.record_id == dish.record_id).first()
            dish_info['dish_time'] = record.datetime

            shop = Shop.query.filter(Shop.shop_id == record.shop_id).first()
            dish_info['shop_name'] = shop.name
            dish_info['shop_address'] = shop.address
            dish_info['shop_id'] = shop.shop_id

            # sells = Order_info.query.filter(Order_info.dish_id == dish.dish_id).count()
            # dish_info['dish_sells'] = sells

            data.append(dish_info)
            print(data)
    return data
    # range = datetime.datetime.fromtimestamp(range // 1000)
    # dishes = Dish.query.filter(Dish.record_id >= range).all()


def get_dish_attr(dishes, shop_name, shop_address):
    """获取菜品属性"""

    type_list = []
    tyeps = Dish_type.query.all()
    for ts in tyeps:
        type_list.append(ts.type_name)
    res = []
    for dish in dishes:
        temp = {}
        temp['dish_id'] = dish.dish_id
        # temp['dish_id'] = dish.price
        temp['dish_sells'] = 10
        temp['shop_name'] = shop_name
        temp['shop_address'] = shop_address
        temp['dish_name'] = dish.dish_name
        temp['price'] = str('%.1f' % dish.price)
        temp['type_name'] = type_list[int(dish.type_id) - 1]
        temp['status'] = dish.status
        temp['urls'] = ""
        temp['selected'] = False
        res.append(temp)
    # print('res:', res)
    return res


def cplb_search(dishname, shopname):
    print("canshu:", dishname)
    print("canshu:", shopname)
    data = []
#    shops = Shop.query.all()
    shops = Shop.query.filter(Shop.name.like('%' + shopname + '%')).all()

    for shop in shops:
        print(shop.name)
        sp = Shop.query.filter(Shop.shop_id == shop.shop_id).first()
        shop_name = sp.name
        shop_address = sp.address
        dishes = Dish.query.join(Record).filter_by(shop_id=shop.shop_id).order_by(Record.datetime.desc()).all()
        new_dishes = []
        name = []
        new_name = []

        for dish in dishes:
            name.append(dish.dish_name)
        # print('name:', name)
        for dish in dishes:
            if dish.dish_name not in new_name:
                new_name.append(dish.dish_name)
                new_dishes.append(dish)
        # print('new_dishes:', new_dishes)
        res = get_dish_attr(new_dishes, shop_name, shop_address)
        data += res
        # print(res)
    # print("data:", data)
    newdata = []
    for d in data:
        # 根据菜名查询
        if d['dish_name'] == dishname and shopname == '':
            newdata.append(d)


        # 根据店名查询
        elif d['shop_name'] == shopname and dishname == '':
            newdata.append(d)

        # 组合查找
        elif d['dish_name'] == dishname and d['shop_name'] == shopname:
            # print(d)
            newdata.append(d)

    print("newdata:", newdata)
    return newdata


def get_dish_attr2(dishes):
    """获取菜品属性"""

    type_list = []
    tyeps = Dish_type.query.all()
    for ts in tyeps:
        type_list.append(ts.type_name)

    shop_list = []
    shops = Shop.query.all()
    for sp in shops:
        shop_list.append(sp.name)

    res = []
    for dish in dishes:
        temp = {}
        temp['dish_id'] = dish.dish_id
        # temp['dish_id'] = dish.price
        temp['dish_sells'] = 10
        # temp['shop_name'] = shop_list[int()]
        # temp['shop_address'] = shop_address
        temp['dish_name'] = dish.dish_name
        temp['price'] = str('%.1f' % dish.price)
        temp['type_name'] = type_list[int(dish.type_id) - 1]
        temp['status'] = dish.status
        temp['urls'] = ""
        temp['selected'] = False
        res.append(temp)
    # print('res:', res)
    return res


def query_sameday(time, shopid, shopname):
    newdata = []
    # dish_time = datetime.datetime(2020, 7, 27, 17, 37, 52)
    # dish_time2 = datetime.datetime(2020, 7, 30, 17, 37, 52)
    # time = [dish_time, dish_time2]
    # print("time:", time)
    t = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    data = []
    year = t.year
    month = t.month
    day = t.day

    conditon1 = datetime.datetime(year, month, day)
    conditon2 = datetime.datetime(year, month, day) + datetime.timedelta(days=1)
    records = Record.query.filter(
        and_(Record.datetime >= conditon1, Record.datetime <= conditon2,
             Record.shop_id == shopid)).all()  # 一条记录所属店铺的同一天的所有记录

    for record in records:
        # print(record.record_id)
        dishes = Dish.query.filter(Dish.record_id == record.record_id).all()
        for dish in dishes:
            # list = []
            dish_info = {}
            # index = {}
            # index['index'] = i
            # data.append(index)
            dish_type = Dish_type.query.filter(Dish_type.type_id == dish.type_id).first()
            dish_info['dish_name'] = dish.dish_name
            dish_info['dish_id'] = dish.dish_id
            dish_info['dish_price'] = str(dish.price)
            d_type = Dish_type.query.filter(Dish_type.type_id == dish.type_id).first()
            dish_info['dish_type_name'] = d_type.type_name

            record = Record.query.filter(Record.record_id == dish.record_id).first()
            dish_info['dish_time'] = record.datetime

            # shop = Shop.query.filter(Shop.shop_id == record.shop_id).first()
            dish_info['shop_name'] = shopname
            dish_info['shop_id'] = shopid

            sells = Order_info.query.filter(Order_info.dish_id == dish.dish_id).count()
            dish_info['dish_sells'] = sells

            data.append(dish_info)
            # print("data:", data)
            # print(len(data)
        newdata.append(data)
    return newdata


def queryByOrderId(order_id):
    data = []
    order = Order.query.filter(Order.order_id == order_id).first()
    info_dict = {}

    order_id = order.order_id
    total_price = str(order.total_price)
    time = order.time

    info_dict["order_id"] = order_id
    info_dict["total_price"] = total_price
    info_dict["time"] = time

    data.append(info_dict)
    return data


def queryByTime2(time, now):  # time 时间范围 now 现在的时间
    print("参数:", time)
    data = []
    date_formmed = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
    range = date_formmed - datetime.timedelta(days=int(time))  # 截至时间，时间范围为res-now
    print(range)
    orders = Order.query.filter(Order.time >= range).all()  # 在时间范围内的所有记录
    for order in orders:
        item = Order.query.filter(Order.order_id == order.order_id).first()
        info_dict = {}

        order_id = item.order_id
        total_price = str(item.total_price)
        time = item.time

        info_dict["order_id"] = order_id
        info_dict["total_price"] = total_price
        info_dict["time"] = time
        data.append(info_dict)
    return data


def queryByTime3(shop_id):
    """查询30天的订单数和营业额"""
    date = []
    sale = []
    order_num = []
    now = datetime.datetime.now()
    start_time = now - datetime.timedelta(days=30)
    print('shop_id', shop_id)
    # orders = Order.query.filter(Order.time >= range).all()  # 在时间范围内的所有记录
    for i in range(30):
        cur = start_time + datetime.timedelta(days=i)
        if shop_id:
            print('1111111')
            orders = Order.query.filter(db.cast(Order.time, db.DATE) == db.cast(cur, db.DATE), Order.shop_id == shop_id).all()  # 当天所有订单
        else:
            print('22222222')
            orders = Order.query.filter(db.cast(Order.time, db.DATE) == db.cast(cur, db.DATE)).all()    # 当天所有订单
        order_num.append(len(orders))
        cur = cur.strftime('%Y-%m-%d')   # 当前日期
        date.append(str(cur))
        sum = 0
        for order in orders:
            sum += float(order.total_price)
        sale.append(sum)
    print("---------------------------------------")
    print(date)
    print(sale)
    print(order_num)
    return [date, sale, order_num]


def queryByOrderIdAndTime(order_id, now, time):
    data = []
    order = Order.query.filter(Order.order_id == order_id).first()
    date_formmed = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
    range = date_formmed - datetime.timedelta(days=int(time))  # 截至时间，时间范围为res-now
    print(range)
    if order.time < range:
        return data
    else:
        data = queryByOrderId(order_id)
        return data


def queryByShopname2(shop_id):
    data = []
    orders = Order.query.filter(Order.shop_id == shop_id).all()
    for order in orders:
        info_dict = {}
        order_id = order.order_id
        info_dict["order_id"] = order_id
        dish_order = order.dishes
        print("dish_order:", dish_order)
        shop = Shop.query.filter(Shop.shop_id == order.shop_id).first()
        info_dict["num"] = len(dish_order)
        info_dict["time"] = order.time
        info_dict['shop_name'] = shop.name
        # info = []
        # for order_info in orders_info:
        #     dish = Dish.query.filter(Dish.dish_id == order_info.info_id).first()
        #     name = dish.dish_name
        #     price = dish.price
        #     info.append(name)
        #     info.append(price)

        info_dict["total_price"] = str(order.total_price)

        # info_dict["info"] = info

        data.append(info_dict)
    return data


#def queryByShopname3(shop):
#    print(shop)
#    data = []
#    orders = Order.query.filter(Order.shop_id == shop_id).all()
#    for order in orders:
#        info_dict = {}
#        order_id = order.order_id
#        info_dict["order_id"] = order_id
#        dish_order = order.dishes
#        print("dish_order:", dish_order)
#        shop = Shop.query.filter(Shop.shop_id == order.shop_id).first()
#        info_dict["num"] = len(dish_order)
#        info_dict["time"] = order.time
#        info_dict['shop_name'] = shop.name
#        # info = []
#        # for order_info in orders_info:
#        #     dish = Dish.query.filter(Dish.dish_id == order_info.info_id).first()
#        #     name = dish.dish_name
#        #     price = dish.price
#        #     info.append(name)
#        #     info.append(price)
#
#        info_dict["total_price"] = str(order.total_price)
#
#        # info_dict["info"] = info
#
#        data.append(info_dict)
#    return data
def queryByShopname3(shop):
    print(shop)
    data = []
    for sp in shop:
        print(sp.name)
        print(sp.shop_id)
        orders = Order.query.filter(Order.shop_id == sp.shop_id).all()
        for order in orders:
            info_dict = {}
            order_id = order.order_id
            info_dict["order_id"] = order_id
            dish_order = order.dishes
            # print("dish_order:", dish_order)
            shop = Shop.query.filter(Shop.shop_id == order.shop_id).first()
            info_dict["num"] = len(dish_order)
            info_dict["time"] = order.time
            info_dict['shop_name'] = shop.name
            # info = []
            # for order_info in orders_info:
            #     dish = Dish.query.filter(Dish.dish_id == order_info.info_id).first()
            #     name = dish.dish_name
            #     price = dish.price
            #     info.append(name)
            #     info.append(price)

            info_dict["total_price"] = str(order.total_price)

            # info_dict["info"] = info

            data.append(info_dict)
    print("data:", data)
    return data



def queryByShopnameAndTime2(shop_id, time, now):
    print("参数：", time)
    date_formmed = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
    range = date_formmed - datetime.timedelta(days=int(time))  # 截至时间，时间范围为res-now
    orders = Order.query.join(Shop).filter(
        and_(Order.time >= range, Shop.shop_id == Order.shop_id)).all()  # 在时间范围内的所有记录
    # records = Record.query.join(Shop).filter(
    #     and_(Record.datetime >= range, Shop.shop_id == Record.shop_id)).all()  # 在时间范围内的所有记录
    print("orders:", orders)

    data = []
    for order in orders:
        info_dict = {}
        order_id = order.order_id
        info_dict["order_id"] = order_id
        dish_order = order.dishes
        print("dish_order:", dish_order)
        shop = Shop.query.filter(Shop.shop_id == order.shop_id).first()
        info_dict["num"] = len(dish_order)
        info_dict["time"] = order.time
        info_dict['shop_name'] = shop.name
        # info = []
        # for order_info in orders_info:
        #     dish = Dish.query.filter(Dish.dish_id == order_info.info_id).first()
        #     name = dish.dish_name
        #     price = dish.price
        #     info.append(name)
        #     info.append(price)

        info_dict["total_price"] = str(order.total_price)

        # info_dict["info"] = info

        data.append(info_dict)
    return data