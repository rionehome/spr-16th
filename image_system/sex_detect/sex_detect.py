import argparse
import cv2
import dlib
import numpy as np
from pathlib import Path
from contextlib import contextmanager
from wide_resnet import WideResNet
from keras.utils.data_utils import get_file

pretrained_model = "https://github.com/yu4u/age-gender-estimation/releases/download/v0.5/weights.28-3.73.hdf5"
modhash = 'fbe63257a054c1c5466cfd7bf14646d6'


def get_args():
    parser = argparse.ArgumentParser(description="This script detects faces from web cam input, "
                                                 "and estimates age and gender for the detected faces.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--weight_file", type=str, default=None,
                        help="path to weight file (e.g. weights.28-3.73.hdf5)")
    parser.add_argument("--depth", type=int, default=16,
                        help="depth of network")
    parser.add_argument("--width", type=int, default=8,
                        help="width of network")
    parser.add_argument("--margin", type=float, default=0.4,
                        help="margin around detected face for age-gender estimation")
    parser.add_argument("--image_dir", type=str, default=None,
                        help="target image directory; if set, images in image_dir are used instead of webcam")
    args = parser.parse_args()
    return args



def draw_label(image, point, label, font=cv2.FONT_HERSHEY_SIMPLEX,
               font_scale=0.8, thickness=1):
    size = cv2.getTextSize(label, font, font_scale, thickness)[0]
    x, y = point
    cv2.rectangle(image, (x, y - size[1]), (x + size[0], y), (255, 0, 0), cv2.FILLED)
    cv2.putText(image, label, point, font, font_scale, (255, 255, 255), thickness, lineType=cv2.LINE_AA)


@contextmanager
def video_capture(*args, **kwargs):
    cap = cv2.VideoCapture(*args, **kwargs)
    try:
        yield cap
    finally:
        cap.release()


#カメラから画像をとってくる
def yield_images():
    with video_capture(0) as cap:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        while True:
            ret, img = cap.read()
            if not ret:
                raise RuntimeError("Failed to capture image")
            yield img


#ディレクトリから画像をとってきて全てリサイズして返す
def yield_images_from_dir(image_dir):
    #パスのオブジェクトを生成
    image_dir = Path(image_dir)
    #~.~という正規表現にマッチするファイルを全て取得する
    for image_path in image_dir.glob("*.*"):
        #RGBで画像読み込み
        img = cv2.imread(str(image_path), 1)

        if img is not None:
            h, w, _ = img.shape
            r = 640 / max(w, h)
            yield cv2.resize(img, (int(w * r), int(h * r)))

def main():

    args = get_args()
    depth = args.depth
    k = args.width
    weight_file = args.weight_file
    margin = args.margin
    image_dir = args.image_dir
    male_num=0
    female_num=0

    if not weight_file:
        #重みのファイルがないなら自動でファイルをダウンロードしてダウンロードしたファイルへのパスを返す
        weight_file = get_file("weights.28-3.73.hdf5", pretrained_model, cache_subdir="pretrained_models",
                               file_hash=modhash, cache_dir=str(Path(__file__).resolve().parent))

    #顔検出の準備
    detector = dlib.get_frontal_face_detector()

    img_size = 64
    #CNNの重みの準備
    model = WideResNet(img_size, depth=depth, k=k)()
    model.load_weights(weight_file)
    #ディレクトリから画像をとってきて全てリサイズして返す、もしimage_dirに画像が設定されてなければカメラから画像をとってくる
    image_generator = yield_images_from_dir(image_dir) if image_dir else yield_images()



    for img in image_generator:
        #BGRからRGBへの変換
        input_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #画像の高さと幅の取得
        img_h, img_w, _ = np.shape(input_img)

        #dlibを使った顔の検出
        detected = detector(input_img, 1)
        faces = np.empty((len(detected), img_size, img_size, 3))



        if len(detected) > 0:
            for i, d in enumerate(detected):
                x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()
                xw1 = max(int(x1 - margin * w), 0)
                yw1 = max(int(y1 - margin * h), 0)
                xw2 = min(int(x2 + margin * w), img_w - 1)
                yw2 = min(int(y2 + margin * h), img_h - 1)
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                # cv2.rectangle(img, (xw1, yw1), (xw2, yw2), (255, 0, 0), 2)
                faces[i, :, :, :] = cv2.resize(img[yw1:yw2 + 1, xw1:xw2 + 1, :], (img_size, img_size))

            #検出した顔から年齢と性別を予想
            results = model.predict(faces)
            predicted_genders = results[0]

            #結果をファイルに書き込む
            for i, d in enumerate(detected):
                label = "{}".format("M" if predicted_genders[i][0] < 0.5 else "F")
                draw_label(img, (d.left(), d.top()), label)
                if predicted_genders[i][0] < 0.5:
                    male_num=male_num+1
                else:
                    female_num=female_num+1
            print(male_num,female_num)

                
        #画像を表示
        cv2.imshow("result", img)
        key = cv2.waitKey(-1) if image_dir else cv2.waitKey(30)

        #ESCキーで終了
        if key == 27:  
            break

if __name__ == '__main__':
    main()
