import rclpy
from rclpy.node import Node

from std_msgs.msg import String, Bool
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

from module.twist import Turtlebot

from time import sleep

from numpy import *

class Control(Node):
    def __init__(self):
        super().__init__("Control")

        self.turtle = Turtlebot()

        self.flag_publisher_cerebrum = self.create_publisher(
            String,
            "/cerebrum/command",
            10
        )

        self.flag_publisher_sound = self.create_publisher(
            String,
            "/sound_system/command",
            10
        )

        self.create_subscription(
            String,
            "/control_system/command",
            self.receiveFlag,
            10
        )

        try:
            rclpy.spin(self.turtle)
        except TypeError:
            pass

    def receiveFlag(self, msg):
        print("control received" + msg.data, flush=True)
        self.Command, Contents = msg.data.split(",")

        Contents = Contents.split(":")
        degree = int(Contents[1])

        if 0 < degree and degree < 180:
            degree *= -1
        else:
            degree = 360 - degree

        self.sender = Contents[2]

        print(degree, flush=True)

        Command = self.Command.split(":")[1]

        if Command == "turn":
            self.turtle.OnEnd = self.OnEnd
            self.turtle.degree = degree
            self.turtle.run(-30.0)
            print("[*] START TURN {0} DEGREE".format(degree), flush=True)

    def OnEnd(self):
        if self.sender == "sound":
            self.sendFinishFlag("sound_system", "Command:finish,Content:None")

        if self.sender == "cerebrum":
            self.sendFinishFlag("cerebrum", "Command:{0},Content:None".format(self.Command))

    def sendFinishFlag(self, topic, content):

        if topic == "sound_system":

            self.flag = String()
            self.flag.data = content + ":control_system"

            self.flag_publisher_sound.publish(self.flag)

            self.flag.data = "Command:angular,Content:None"
            print("control send" + self.flag, flush=True)

            self.flag_publisher_cerebrum.publish(self.flag)


        elif topic == "cerebrum":

            self.flag = String()
            self.flag.data = content + ":control_system"

            print("control send" + str(self.flag), flush=True)
            self.flag_publisher_cerebrum.publish(self.flag)


def main():
    rclpy.init()

    node = Control()

    rclpy.spin(node)


if __name__ == "__main__":
    main()