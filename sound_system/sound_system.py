import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from module import module_count
from module import module_count_people
from module import module_angular
from module import module_QandA
from module import module_pico
from module import module_beep

from std_msgs.msg import String

class SoundSystem(Node): 
    def __init__(self):
        super(SoundSystem, self).__init__('SoundSystem')

        self.command = None

        self.create_subscription(
            String, 'sound_system/command',
            self.command_callback,
            10
        )

        self.senses_publisher = self.create_publisher(
            String,
            'cerebrum/command',
            10
        )
    def command_callback(self, msg):
    
        self.command = msg.data
        command = msg.data.split(',')

        

        # 10秒カウント
        if 'count' == command[0].replace('Command:', ''):
            if module_count.count() == 1:
                self.cerebrum_publisher('Return:0,Content:None')
        # 人数発話
        if 'count_people' == command[0].replace('Command:', ''):
            if module_count_people.count_people(str(command[1].replace('Content:', ''))) == 1: # ここの引数に人数を入れる
                self.cerebrum_publisher('Return:0,Content:None')
        
        # QandA開始
        if 'QandA' == command[0].replace('Command:', ''):
            if module_QandA.QandA(5) == 1:
                self.cerebrum_publisher('Return:0,Content:None')

        # 音限定位
        if 'augular' == command[0].replace('Command:', ''):
            if module_angular.angular() == 1:
                self.temp_angular = module_angular.angular()
                if self.temp_angular > 0:
                    self.cerebrum_publisher(
                    'Command:find,Content:'+str(self.temp_angular))


    def cerebrum_publisher(self, message):
        _trans_message = String()
        _trans_message.data = message

        self.senses_publisher.publish(_trans_message)
    
def main():
    rclpy.init()
    node = SoundSystem()
    rclpy.spin(node)


if __name__ == '__main__':
    main()






