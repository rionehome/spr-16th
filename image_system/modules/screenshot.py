import pyrealsense2 as rs
import numpy as np
from time import sleep
import cv2
import os

file_path = os.path.abspath(__file__)
image_path = ('/home/kohei/spr/spr-16th/image_system/image/people_image.jpg')
#file_path.replace(
    #'modules/screenshot.py', 'image/people_image.jpg')


def screenshot():
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    i = 0
    pipeline.start(config)

    try:
        while (i < 5):
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue
            
            depth_image = np.asanyarray(depth_frame.get_data())  # これ使われてないなんやこれ
            color_image = np.asanyarray(color_frame.get_data())
            images = color_image
            cv2.imshow('RealSense', images)
            cv2.waitKey(1)
            cv2.imwrite(image_path, images)
            sleep(1)
            i = i + 1
            print("captured" + str(i))

    finally:

        pipeline.stop()
        
        return 1

if __name__=='__main__':
    screenshot()