import re
import numpy as np
import cv2 as cv
from sklearn.model_selection import train_test_split
from keras import backend as K
from keras.layers import Activation
from keras.layers import Input, Lambda, Dense, Dropout, Convolution2D, MaxPooling2D, Flatten
from keras.layers import Conv2D,BatchNormalization
from keras.models import Sequential, Model
from keras.optimizers import RMSprop
from keras.regularizers import l2
import os

# def read_image(filename, byteorder='>'):
#     with open(filename, 'rb') as f:
#         buffer = f.read()
#     header, width, height, maxval = re.search(
#         b"(^P5\s(?:\s*#.*[\r\n])*"
#         b"(\d+)\s(?:\s*#.*[\r\n])*"
#         b"(\d+)\s(?:\s*#.*[\r\n])*"
#         b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
#     return np.frombuffer(buffer,
#                          dtype='u1' if int(maxval) < 256 else byteorder + 'u2',
#                          count=int(width) * int(height),
#                          offset=len(header)
#                          ).reshape((int(height), int(width)))


size = 2
total_sample_size = 1500  # 样本数量


def get_data(size, total_sample_size, path, kind, num, shop_id):
    print("path:", path)  # trainDatasets_pgm\1\1591858394393.pgm
    # root = path.split('\\')[0]
    # root = os.path.join(os.getcwd(), root)
    # root = os.getcwd() + '/demo/traindatas_pgm'
    root = os.getcwd() + '/demo//static/food_images/' + str(shop_id) + '/pgmPics'
    print('root:', root)
    # path = os.path.join(os.getcwd(), path)
    # firstImgPath = os.path.join(os.getcwd(), '/s1/1.pgm')
    # print("firstImgPath；", firstImgPath)
    dirlist = os.listdir(root)  # 文件夹名称列表
    # image = read_image(path, 'rw+')
    image = cv.imread(path)
#    image = image[::size, ::size]
    dim1 = image.shape[0]
    dim2 = image.shape[1]
    count = 0
    x_geuine_pair = np.zeros([total_sample_size, 2, 1, dim1, dim2])  # 2 is for pairs
    y_genuine = np.zeros([total_sample_size, 1])
    for i in range(kind):  # i 7
        number = len(os.listdir(root + '/' + dirlist[i]))
        print(dirlist[i] + '  文件夹下有:' + str(number) + '张图片，在' + str(number) + '中随机')
        for j in range(int(total_sample_size / kind)):  # t j 214
            ind1 = 0
            ind2 = 0
            while ind1 == ind2:
                ind1 = np.random.randint(number)  # 6是一个文件夹下的图片数
                ind2 = np.random.randint(number)
            # read the two images
            # print("xx:" + root + '/' + str(dirlist[i]) + '/' + str(ind1 + 1) + '.jpg')
            # print("xx:" + root + '/' + str(dirlist[i]) + '/' + str(ind2 + 1) + '.jpg')
            # img1 = read_image(root + '/' + str(dirlist[i]) + '/' + str(ind1 + 1) + '.pgm', 'rw+')
            # img2 = read_image(root + '/' + str(dirlist[i]) + '/' + str(ind2 + 1) + '.pgm', 'rw+')
            img1 = cv.imread(root + '/' + str(dirlist[i]) + '/' + str(ind1 + 1) + '.jpg', cv.IMREAD_GRAYSCALE)
            img2 = cv.imread(root + '/' + str(dirlist[i]) + '/' + str(ind2 + 1) + '.jpg', cv.IMREAD_GRAYSCALE)
            # reduce the size
#            img1 = img1[::size, ::size]
#            img2 = img2[::size, ::size]
            # store the images to the initialized numpy array
            x_geuine_pair[count, 0, 0, :, :] = img1
            x_geuine_pair[count, 1, 0, :, :] = img2
            # as we are drawing images from the same directory we assign label as 1. (genuine pair)
            y_genuine[count] = 1
            count += 1
        print('test')
    print('test1')
    count = 0
    x_imposite_pair = np.zeros([total_sample_size, 2, 1, dim1, dim2])
    y_imposite = np.zeros([total_sample_size, 1])
    for i in range(int(total_sample_size / num)):
        for j in range(num):
            while True:
                ind1 = np.random.randint(kind)
                ind2 = np.random.randint(kind)
                if ind1 != ind2:
                    break
            # print('xxxx1:',
            #       root + '/' + str(dirlist[ind1]) + '/' + str(
            #           np.random.randint(len(os.listdir(root + '/' + dirlist[ind1]))) + 1) + '.jpg')
            # print('xxxx2:',
            #       root + '/' + str(dirlist[ind2]) + '/' + str(
            #           np.random.randint(len(os.listdir(root + '/' + dirlist[ind2]))) + 1) + '.jpg')
            # img1 = read_image(root + '/' + str(dirlist[ind1]) + '/' + str(j + 1) + '.pgm', 'rw+')
            # img2 = read_image(root + '/' + str(dirlist[ind2]) + '/' + str(j + 1) + '.pgm', 'rw+')
            img1 = cv.imread(
                root + '/' + str(dirlist[ind1]) + '/' + str(
                    np.random.randint(len(os.listdir(root + '/' + dirlist[ind1]))) + 1) + '.jpg',
                cv.IMREAD_GRAYSCALE)
            img2 = cv.imread(
                root + '/' + str(dirlist[ind2]) + '/' + str(
                    np.random.randint(len(os.listdir(root + '/' + dirlist[ind2]))) + 1) + '.jpg',
                cv.IMREAD_GRAYSCALE)
#            img1 = img1[::size, ::size]
#            img2 = img2[::size, ::size]
            x_imposite_pair[count, 0, 0, :, :] = img1
            x_imposite_pair[count, 1, 0, :, :] = img2
            y_imposite[count] = 0
            count += 1
    X = np.concatenate([x_geuine_pair, x_imposite_pair], axis=0) / 255
    Y = np.concatenate([y_genuine, y_imposite], axis=0)
    return X, Y


# X, Y = get_data(size, total_sample_size)
# print(X.shape)
# x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=.25)
# print(x_test.shape)
def build_base_network(input_shape):
    seq = Sequential()
    nb_filter = [6, 12]
    kernel_size = 3
    # convolutional layer 1
    seq.add(Convolution2D(nb_filter[0], kernel_size, kernel_size, input_shape=input_shape,
                          border_mode='valid', dim_ordering='th'))
    seq.add(Activation('relu'))
    seq.add(MaxPooling2D(pool_size=(2, 2)))
    seq.add(Dropout(.25))
    # convolutional layer 2
    seq.add(Convolution2D(nb_filter[1], kernel_size, kernel_size, border_mode='valid', dim_ordering='th'))
    seq.add(Activation('relu'))
    seq.add(MaxPooling2D(pool_size=(2, 2), dim_ordering='th'))
    seq.add(Dropout(.25))
    # flatten
    seq.add(Flatten())
    seq.add(Dense(128, activation='relu'))
    seq.add(Dropout(0.1))
    seq.add(Dense(50, activation='relu'))
    return seq

def build_base_network2(input_shape, reg=0.0002):
    model = Sequential()
    # inputShape = (height, width, depth)
    height, width, depth = input_shape
    chanDim = -1

    if K.image_data_format() == "channels_first":
        input_shape = (depth, height, width)
        chanDim = 1

    # model.add(Conv2D(96, (11, 11), strides=(4, 4), input_shape=input_shape, padding="same",
    #                  kernel_regularizer=l2(reg), data_format='channels_first'))
    model.add(Conv2D(96, (5, 5), strides=(2, 2), input_shape=input_shape, padding="same",
                     kernel_regularizer=l2(reg), data_format='channels_first'))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2), data_format='channels_first'))
    model.add(Dropout(0.25))

    model.add(Conv2D(256, (5, 5), padding="same", kernel_regularizer=l2(reg), data_format='channels_first'))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2), data_format='channels_first'))
    model.add(Dropout(0.25))

    model.add(Conv2D(384, (3, 3), padding="same", kernel_regularizer=l2(reg), data_format='channels_first'))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(Conv2D(384, (3, 3), padding="same", kernel_regularizer=l2(reg), data_format='channels_first'))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(Conv2D(256, (3, 3), padding="same", kernel_regularizer=l2(reg), data_format='channels_first'))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2), data_format='channels_first'))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(4096, kernel_regularizer=l2(reg)))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(Dropout(0.25))

    model.add(Dense(4096, kernel_regularizer=l2(reg)))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(Dropout(0.25))

    model.add(Dense(4096, kernel_regularizer=l2(reg)))
    # model.add(Activation("softmax"))
    # model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    return model


# input_dim = x_train.shape[2:]
# # print("input_dim", input_dim)
# img_a = Input(shape=input_dim)
# img_b = Input(shape=input_dim)
# print(img_a.shape)
# print("input_dim", input_dim)
# base_network = build_base_network(input_dim)
# feat_vecs_a = base_network(img_a)
# feat_vecs_b = base_network(img_b)
# print(feat_vecs_a.shape)
# exit()
#def euclidean_distance(vects):
#    x, y = vects
#    return K.sqrt(K.sum(K.square(x - y), axis=1, keepdims=True))


def eucl_dist_output_shape(shapes):
    shape1, shape2 = shapes
    return (shape1[0], 1)


# distance = Lambda(euclidean_distance, output_shape=eucl_dist_output_shape)([feat_vecs_a, feat_vecs_b])
# epochs = 2
# #def __init__(self, lr=0.001, rho=0.9, epsilon=None, decay=0.,**kwargs):
# rms = RMSprop(lr=0.0005)

# model = Model(input=[img_a, img_b], output=distance)
def contrastive_loss(y_true, y_pred):
    margin = 1
    return K.mean(y_true * K.square(y_pred) + (1 - y_true) * K.square(K.maximum(margin - y_pred, 0)))


# model.compile(loss=contrastive_loss, optimizer=rms)
# img_1 = x_train[:, 0]
# img_2 = x_train[:, 1]

def accuracy(y_true, y_pred):
    return K.mean(K.equal(y_true, K.cast(y_pred < 0.5, y_true.dtype)))


# model.compile(loss=contrastive_loss, optimizer=rms, metrics=[accuracy])
# model.fit([img_1, img_2], y_train, validation_split=.2, batch_size=128, verbose=2, nb_epoch=epochs)
# model.save(r'newmodel_06131006.h5')
# pred = model.predict([x_test[:, 0], x_test[:, 1]])
# print(pred)
def compute_accuracy(predictions, labels):
    return labels[predictions.ravel() < 0.5].mean()
# acc = compute_accuracy(pred, y_test)
# print(acc)
