from modules import face_detect
from modules import screenshot
from modules import module_sex_detect
from modules import wide_resnet
from std_msgs.msg import String
import rclpy
from rclpy.node import Node

from time import sleep

class ImageSystem(Node):
    def __init__(self):
        super(ImageSystem, self).__init__('ImageSystem')

        self.senses_publisher = self.create_publisher(
                String,
                'cerebrum/command',
                10
        )

        self.create_subscription(
                String,
                '/image_system/command',
                self.command_callback,
                10
        )

        self.message = None
        self.command = None
        self._trans_message = String()

        sleep(1)

    def command_callback(self, msg):

        # contain command data
        print("image recerved " + str(msg.data), flush=True)
        self.command = msg.data

        # Command:speak , Content:hello!
        command = msg.data.split(',')

        if 'capture' == command[0].replace('Command:', ''):
            print("start capture", flush=True)
            if screenshot.screenshot() == 1:
                self.temp_number = module_sex_detect.main()
                #if self.temp_number >= 0:  # 人数のみカウントのとき
                if type(self.temp_number) == str: # 男女認識よう
                    print("end capture", flush=True)
                    self.cerebrum_publisher(
                        'Return:0,Content:'+str(self.temp_number))

    # メッセージ送るやつ
    def cerebrum_publisher(self, message):

        self._trans_message.data = message
        print("image send " + str(self._trans_message), flush=True)
        self.senses_publisher.publish(self._trans_message)


def main():
    rclpy.init()
    node = ImageSystem()
    rclpy.spin(node)

if __name__ == "__main__":
    main()