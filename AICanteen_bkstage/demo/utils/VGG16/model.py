# from keras.applications.vgg16 import VGG16
from keras.applications import VGG16
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Activation, Dropout, Flatten, Dense, MaxPooling2D, ZeroPadding2D, \
    Convolution2D
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
import numpy as np
import os
import tensorflow as tf
import keras
from time import time as timer
os.environ["CUDA_VISIBLE_DEVICES"] = '0'  # 指定第一块GPU可用
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.5  # 程序最多只能占用指定gpu50%的显存
# config.gpu_options.allow_growth = True  # 程序按需申请内存
session = tf.Session(config=config)
keras.backend.set_session(session)

def VGG16_train(train_path, model_path):
    test_path = train_path.replace('train', 'test')
    class_num = len(os.listdir(train_path))     # 训练类别
    vgg16_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    # 搭建全连接层
    top_model = Sequential()
    top_model.add(Flatten(input_shape=vgg16_model.output_shape[1:]))
    top_model.add(Dense(256, activation='relu'))
    top_model.add(Dropout(0.5))
    top_model.add(Dense(class_num, activation='softmax'))

    model = Sequential()
    model.add(vgg16_model)
    model.add(top_model)

    train_datagen = ImageDataGenerator(
        rotation_range=40,  # 随机旋转度数
        width_shift_range=0.2,  # 随机水平平移
        height_shift_range=0.2,  # 随机竖直平移
        rescale=1 / 255,  # 数据归一化
        shear_range=20,  # 随机错切变换
        zoom_range=0.2,  # 随机放大
        horizontal_flip=True,  # 水平翻转
        fill_mode='nearest',  # 填充方式
    )
    test_datagen = ImageDataGenerator(
        rescale=1 / 255,  # 数据归一化
    )

    batch_size = 16

    # 生成训练数据
    train_generator = train_datagen.flow_from_directory(
        train_path,
        target_size=(224, 224),
        batch_size=batch_size,
    )

    # 测试数据
    test_generator = test_datagen.flow_from_directory(
        test_path,
        target_size=(224, 224),
        batch_size=batch_size,
    )
    model.compile(optimizer=SGD(lr=1e-4, momentum=0.9), loss='categorical_crossentropy', metrics=['accuracy'])

    t1 = timer()
    model.fit_generator(train_generator, steps_per_epoch=len(train_generator), epochs=12, validation_data=test_generator,
                        validation_steps=len(test_generator))
    t2 = timer()
    model.save(model_path)
    return train_generator.class_indices
