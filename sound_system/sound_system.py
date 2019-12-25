import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from module import module_count
from module import module_count_people
from module import module_angular
from module import module_QandA
from module import module_QandAandA
from module import module_pico
from module import module_beep

from std_msgs.msg import String

class SoundSystem(Node): 
    def __init__(self):
        super(SoundSystem, self).__init__('SoundSystem')

        self.command = None

        self.create_subscription(
            String, '/sound_system/command',
            self.command_callback,
            10
        )

        self.senses_publisher = self.create_publisher(
            String,
            'cerebrum/command',
            10
        )
    def command_callback(self, msg):
        print("sound received " + msg.data, flush=True)
        self.command = msg.data
        command = msg.data.split(',')

        

        # 10秒カウント
        if 'count' == command[0].replace('Command:', ''):
            print("start count", flush=True)
            if module_count.count() == 1:
                print("end count", flush=True)
                self.cerebrum_publisher('Return:0,Content:None')

        # 人数発話
        if 'count_people' == command[0].replace('Command:', ''):
            print("start count_people", flush=True)
            if module_count_people.count_people(str(command[1].replace('Content:', ''))) == 1: # ここの引数に人数を入れる
                print("end count_people", flush=True)
                self.cerebrum_publisher('Return:0,Content:None')
        
        # QandA開始
        if 'QandA' == command[0].replace('Command:', ''):
            print("start QandA", flush=True)
            if module_QandA.QandA(5) == 1:
                print("end QandA", flush=True)
                self.cerebrum_publisher('Return:0,Content:None')

        # 音限定位➀
        if 'angular_and_question' == command[0].replace('Command:', ''):
            return_list = module_QandAandA.angular()
            self.temp_angular = return_list[0]
            self.answer_angular = return_list[1]
            if self.temp_angular >= 0:
                self.cerebrum_publisher('Return:0,Content:' + str(self.temp_angular))

        # 音源定位➁
        if 'answer' == command[0].replace('Command:', ''):
            module_pico.speak(str(self.answer_angular)) 
            self.cerebrum_publisher('Return:0,Content:None')


    def cerebrum_publisher(self, message):
        _trans_message = String()
        _trans_message.data = message
        print("sound send " + str(_trans_message.data), flush=True) # 間違えてた
        self.senses_publisher.publish(_trans_message)
    
def main():
    rclpy.init()
    node = SoundSystem()
    rclpy.spin(node)


if __name__ == '__main__':
    main()