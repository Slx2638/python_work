import time, os
from demo import app, db
from flask import render_template, request, flash, session, redirect, url_for, json, jsonify
from demo.model.Record import Record
from demo.model.Train import Train
import tensorflow as tf
from demo.utils.cgoujiekou import YOLO
from demo.controller.mini_app import get_timestamp,path
import datetime
import shutil
import keras
from demo.utils.VGG16.imagedata import generator
from demo.utils.VGG16.model import VGG16_train
from time import time as timer


config = tf.ConfigProto(
    device_count={'GPU': 1},
    intra_op_parallelism_threads=1,
    allow_soft_placement=True
)
sess = tf.Session(config=config)

keras.backend.set_session(sess)


global _yolo
global graph
graph = tf.get_default_graph()
_yolo = YOLO()

print("**************************",tf.test.is_gpu_available())


infoDict = {}


def recognize(imgpath, shop_id):
    with graph.as_default():  # 获取他的上下文管理器
        prediction = _yolo.recognizeinterface(imgpath, shop_id)
    return prediction


def listToJson(lst):
    class A:
        def __init__(self, kind, x1, y1, x2, y2, money):
            self.kind = kind
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
            self.money = money

    list = []
    for point in lst:
        list.append(A(point[0], str(point[1]), str(point[2]), str(point[3]), str(point[4]), "20").__dict__)
    return json.dumps(list)

@app.route('/add_train', methods=["POST"])
def add_train():
    record_id = request.values.get('record_id')
    print("reid:",record_id)
    record_info = request.values.get('record_info')
    record_info = json.loads(record_info)
    print("reif:",record_info)
    for ri in record_info:
        print(ri)
        for i in range(len(ri["dishes"])):
            if not ri['dishes'][i]['dish_name'] in infoDict:
                infoDict[ri['dishes'][i]['dish_name']] = ri['dishes'][i]['price']
            else:
                continue
    dish_num = len(infoDict)
    record = Record.query.get(record_id)
    record.status = 2
    new_train = Train()
    new_train.train_id = get_timestamp()
    new_train.time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_train.record_id = record.record_id
    new_train.train_status = 0
    json_info = json.dumps(infoDict)
    new_train.name_price = json_info
    new_train.dish_num = dish_num
    db.session.add(new_train)
    db.session.commit()
    xl2(infoDict, record.shop_id,get_timestamp())
    new_train.train_status = 1
    db.session.commit()
    return 'success'

def images_process(origin_dir, save_dir):
    """将图片中的菜截出来"""
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)
    names = os.listdir(origin_dir)
    for name in names:
        images = os.listdir(origin_dir + name)
        for image in images:
            src = origin_dir + name + '/' + image
            dst = save_dir + name + '/' + image
            if not os.path.exists(save_dir + name):
                os.makedirs(save_dir + name)
            _yolo.cutTrainImage(src, dst)


def xl2(infoDict, shop_id,modelid):
    """使用VGG16模型进行训练"""
    model_path = path + '//static/utils/model/%d/%d.h5' % (shop_id , modelid )  # 模型位置
    with graph.as_default():  # 获取他的上下文管理器
        rawImgPath = path + '//static/food_images/' + str(shop_id)
        images_process(rawImgPath + '/rawPics/', rawImgPath + '/proPics/')  # 处理训练图片
        t1 = timer()
        generator(rawImgPath, shop_id)    # 生成训练、测试图片
        t2 = timer()
        train_dir = rawImgPath + '/generator/train'
        labels = VGG16_train(train_dir, model_path)  # 训练VGG模型
        t3 = timer()
        print('花费时间：', t2-t1, t3-t2)
        price_path = path +'//static/utils/model/%d/price.txt' % shop_id
        name_path = path + '//static/utils/model/%d/name.txt' % shop_id
        with open(name_path, 'w', encoding='utf-8') as f:
            for key in labels.keys():
                f.write(key + '\n')
        with open(price_path, 'w', encoding='utf-8') as f:
            for key in labels.keys():
                f.write(infoDict[key] + '\n')
