# -*- coding:utf-8 -*-
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Reshape
from tensorflow.keras.layers import Conv2D, MaxPool2D
from tensorflow.keras import Sequential
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os, glob


class CNN(object):
    def __init__(self, train=False):
        ## -----*----- コンストラクタ -----*----- ##
        # ファイルパス
        #self.format_path = './config/format.jpg'
        self.model_path = './model/model.hdf5'
        self.img_path = './teacher_data/'

        #self.img_size = Image.open(self.format_path).size
        self.img_size = (128, 128)

        # モデルのビルド
        self.__model = self.__build()

        if train:
            # 学習
            x, y = self.__features_extracter()
            self.__train(x, y)
        else:
            # モデルの読み込み
            self.__load_model(self.model_path)

    def __build(self):
        ## -----*----- NNの構築 -----*----- ##
        model = Sequential()
        model.add(Conv2D(filters=16, kernel_size=(3, 3), strides=(1, 1),
                         input_shape=(self.img_size[0], self.img_size[1], 1), padding='same', activation='relu'))
        model.add(Conv2D(filters=16, kernel_size=(3, 3), strides=(1, 1),
                         padding='same', activation='relu'))
        model.add(MaxPool2D(pool_size=(2, 2)))
        model.add(Dropout(0.5))
        model.add(Conv2D(filters=64, kernel_size=(3, 3), strides=(1, 1),
                         padding='same', activation='relu'))
        model.add(Conv2D(filters=64, kernel_size=(3, 3), strides=(1, 1),
                         padding='same', activation='relu'))
        model.add(MaxPool2D(pool_size=(2, 2)))
        model.add(Dropout(0.5))
        model.add(Flatten())
        model.add(Dense(units=512, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(2, activation='softmax'))

        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=["accuracy"])

        return model

    def __train(self, x, y, epochs=50):
        for step in range(epochs // 10):
            self.__model.fit(x, y, initial_epoch=step * 10, epochs=(step + 1) * 10, batch_size=100)
            self.__model.save_weights(self.model_path.replace('.hdf5', '_{0}.hdf5'.format((step + 1))))

        # 最終の学習モデルを保存
        self.__model.save_weights(self.model_path)

    def __features_extracter(self):
        ## -----*----- 特徴量を抽出 -----*----- ##
        x = []
        y = []
        man = glob.glob(self.img_path + '*')[0]
        woman = glob.glob(self.img_path + '*')[1]

        num = len(glob.glob(self.img_path + '*/*'))
        print(num)
        cnt = 1

        # 男性
        for f in glob.glob(man + '/*'):
            print("\033[1ASTEP：{0}/{1}".format(cnt, num));
            cnt += 1
            x.append(self.__read_img(f))
            y.append([0])
        # 女性
        for f in glob.glob(woman + '/*'):
            print("\033[1ASTEP：{0}/{1}".format(cnt, num));
            cnt += 1
            x.append(self.__read_img(f))
            y.append([1])

        x = np.array(x)
        y = np.array(y)
        return x, y

    def __read_img(self, file):
        ## -----*----- 画像を読み取り -----*----- ##
        ret = load_img(file, grayscale=True, target_size=(self.img_size))
        ret = img_to_array(ret) / 255
        ret = self.nomalize(ret)

        return np.reshape(ret, (self.img_size[0], self.img_size[1], 1))

    def nomalize(self, x, axis=None):
        ## -----*----- 0~1に正規化 -----*----- ##
        x = np.array(x)
        min = x.min(axis=axis, keepdims=True)
        max = x.max(axis=axis, keepdims=True)
        if not (max - min) == 0:
            result = (x - min) / (max - min)
        else:
            result = x
        return result

    def predict(self, file):
        ## -----*----- 推論 -----*-----##
        data = self.__read_img(file)
        return self.__model.predict(np.array([data]))[0]

    def __load_model(self, path):
        ## -----*----- 学習済みモデルの読み込み -----*-----##
        # モデルが存在する場合，読み込む
        if os.path.exists(path):
            self.__model.load_weights(path)


if __name__ == '__main__':
    infer = CNN()
    for f in glob.glob('./teacher_data/man/*'):
        #pred = infer.predict(glob.glob('./teacher_data/woman/*')[3])
        pred = infer.predict(f)
        print('man：%5.3f  woman：%5.3f' % (pred[0], pred[1]))
