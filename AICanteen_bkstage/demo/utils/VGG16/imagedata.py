from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import os
import random
import shutil


def move_images(path):
    """移动部分训练图片到测试集中"""
    test_dir = path.replace('train', 'test')
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    dirs = os.listdir(path)
    for d in dirs:
        fileDir = path + d + '/'
        tarDir = fileDir.replace('train', 'test')
        if not os.path.exists(tarDir):
            os.makedirs(tarDir)
        rate = 0.2
        pathDir = os.listdir(fileDir)  # scan
        filenumber = len(pathDir)
        picknumber = int(filenumber * rate)
        sample = random.sample(pathDir, picknumber)
        for name in sample:
            shutil.move(fileDir + name, tarDir + name)
        print('succeed moved {} pictures from {} to {}'.format(picknumber, fileDir, tarDir))

def get_images(path):
    """获取图片绝对路径"""
    images = []
    for root, dirs, files in os.walk(path):
        for file in files:
            name = os.path.join(root, file)
            images.append(name)
    return images


def generator(path, shop_id):
    origin_dir = path + '/proPics/'
    train_dir = path + '/generator/train/'
    if os.path.exists('/generator'):
        shutil.rmtree('/generator')
    datagen = ImageDataGenerator(
            rotation_range=180,
            width_shift_range=0.08,
            height_shift_range=0.08,
            shear_range=0.1,
            zoom_range=0.1,
            fill_mode='nearest')
    images = get_images(origin_dir)
    for img in images:
        gen_num = 200 // len(os.listdir(os.path.dirname(img)))       # 用于控制每一类总图片数
        save_dir = os.path.dirname(img).replace('proPics', 'generator/train')   # 获取训练图片所在目录
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        img = load_img(img)  # 这是一个PIL图像
        x = img_to_array(img)
        x = x.reshape((1,) + x.shape)
        i = 0
        for batch in datagen.flow(x, batch_size=1,
                                  save_to_dir=save_dir, save_prefix='914', save_format='jpg'):
            i += 1
            if i > gen_num:
                break
    move_images(train_dir)

