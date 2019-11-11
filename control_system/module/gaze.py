import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

from time import sleep

from numpy import *

class Controle(Node):
    def __init__(self):
        super().__init__("turtlebot3")
        self.pub = self.create_publisher(Twist, "/cmd_vel")

        self.create_subscription(
            Odometry,
            "/odom",
            self.sendVelocity,
            10
        )

        self.twist = Twist()

        self.degree = 180

    def sendVelocity(self, msg):
        w = msg.pose.pose.orientation.w #角度をcosの長さに変換
        z = msg.pose.pose.orientation.z

        angle = 0 #初期値

        if z > 0:
            angle = -arccos(w)*360 / pi #cosの長さを角度に変換
        else:
            angle =  arccos(w)*360 / pi
        # if reach target angular
        if angle > 180 : #移動した角度の合計　
            print("greater than 180")
            self.stop()
            print(self.twist)

    def run(self, a):
        self.twist.angular.z = a
        self.pub.publish(self.twist)

    def stop(self):
        self.twist.angular.z = 0.0 #目標の角度になったら止める=(0)にする
        self.pub.publish(self.twist)

def main():
    rclpy.init()

    node = Controle()

    sleep(1)
    node.run(-0.3) #　-で時計回り, +で反時計回り速度は自由に変えていいよ

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()