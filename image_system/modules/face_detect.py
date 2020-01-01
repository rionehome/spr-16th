import rclpy
from rclpy.node import Node
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
import os
import shutil
import sys
from cv_bridge import CvBridge

from time import sleep

def detect():
    file_path = os.path.abspath(__file__)

    # カメラから取得した画像をおいてある場所
    image_path = file_path.replace('modules/face_detect.py', 'image/people_image.jpg')
        
    # カスケードファイルをおいてある場所
    cascade_path = file_path.replace('modules/face_detect.py', 'cascades/haarcascade_frontalface_default.xml')

    image = cv2.imread(image_path)

    # 画像データを開けなかったときにその旨をメッセージとして出力させる
    if(image is None):
        print ('画像を開けません')
        quit()

    # 取得した画像をグレースケールに変換
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #カスケードに分類させる
    cascade = cv2.CascadeClassifier(cascade_path)

    # 物体認識（顔認識）の実行
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))

    print ("face rectangle")
    print (facerect)

    # ディレクトリの作成
    if len(facerect) > 0:
        path = os.path.splitext(image_path)
        dir_path = path[0] + '_face'
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)
        os.mkdir(dir_path)

    i = 0
    for rect in facerect:
        #顔だけ切り出して保存
        x = rect[0]
        y = rect[1]
        width = rect[2]
        height = rect[3]
        dst = image[y:y+height, x:x+width]
        new_image_path = dir_path + '/' + str(i) + path[1]
        cv2.imwrite(new_image_path, dst)
        i += 1
    files = os.listdir(dir_path)
    count = len(files)  
    print("\n人数は {} 人".format(count))
    return count

if __name__=='__main__':
    detect()