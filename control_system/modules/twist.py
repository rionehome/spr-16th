import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
from time import sleep

from numpy import *

class Controle(Node):
    def __init__(self):
        super().__init__("turtlebot2")
        self.publish_velocity = self.create_publisher(Twist, "/turtlebot2/commands/velocity")
        self.create_subscription(
            Odometry,
            "/turtlebot2/odometry",
            self.sendVelocity,
            10
        )
        self.publish_reset = self.create_publisher(Twist, "turtlebot2/commands/reset_pose")

        self.twist = Twist()

        self.degree = 180
        
        #self.orientation = Quaternion()

    def sendVelocity(self, msg):
        w = msg.pose.pose.orientation.w #wはクオータニオン表記　オイラー角に直す必要あり
        z = msg.pose.pose.orientation.z 

        angle = 0 #初期値

        if z > 0:
            angle = -arccos(w)*360 / pi #cosの長さを角度に変換
        else:
            angle =  arccos(w)*360 / pi
        if angle < 0:
            angle = angle+360

        print(self.twist)
        print(f"rotated{angle}")
        # if reach target angular
        if angle > self.degree: #移動した角度の合計　回転する角度の入力(音声藩用メモ)
            print("greater than 180")
            self.stop()
            print(self.twist)

    def run(self, a):
        self.twist.linear.x = 0.0
        self.twist.angular.z = a
        self.publish_velocity.publish(self.twist)
        print('running...')

    def stop(self):
        self.twist.angular.z = 0.0 #目標の角度になったら止める=(0)にする
        self.publish_velocity.publish(self.twist)

def main():
    rclpy.init()

    node = Controle()

    sleep(1)
    #node.degree=90
    node.run(-30.0)

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
