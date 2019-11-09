from modules import face

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from cv_bridge import CvBridge
from time import sleep
from sensor_msgs.msg import Image


class ImageSystem(Node):
    def __init__(self):
        super(ImageSystem, self).__init__('ImageSystem')

        self.senses_publisher = self.create_publisher(
                String,
                'cerebrum/command',
                10
        )

        self.answor_human_number = self.create_publisher(
                String,
                "sound_system/command",
                10
        )

        self.create_subscription(
                String,
                '/image_system/command',
                self.command_callback,
                10
        )

        self.create_subscription(
                Image,
                '/camera/color/image_raw',
                self.get_image,
                10
        )

        self.message = None
        self.command = None
        self._trans_message = String()

        self.bridge = CvBridge()

        sleep(1)

    def command_callback(self, msg):

        # contain command data
        self.command = msg.data

        # Command:speak , Content:hello!
        command = msg.data.split(',')

        if 'capture' == command[0].replace('Command:', ''):
            human_number = self.detect_human()
            print("HUMAN : {0}".format(human_number), flush=True)
            self.answor_human_number.publish(self._trans_message)
            #self.cerebrum_publisher('Return:0,Content:')

              
    # get image from realsense
    def get_image(self, msg):
        self.image = self.bridge.imgmsg_to_cv2(msg)
    # detect number's human
    def detect_human(self):
        number = face(self.image)
        print(number)
        return number

    # メッセージ送るやつ
    def cerebrum_publisher(self, message):

        self._trans_message.data = message
        self.senses_publisher.publish(self._trans_message)

def main():
    rclpy.init()
    node = ImageSystem()
    rclpy.spin(node)

if __name__ == "__main__":
    main()
