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
        if angle > 180: #移動した角度の合計　回転する角度の入力(音声藩用メモ)
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

class Euler(Node):
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.orientation = Quaternion()
        #クオータニオン→回転行列
    def Quaternion2Matrix(ary: Quaternion) -> array:
        
        x, y, z, w = msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,msg.pose.pose.orientation.z,msg.pose.pose.orientation.w

        m00 = 1     - 2*y**2 - 2*z**2
        m01 = 2*x*y + 2*w*z
        m02 = 2*x*z - 2*w*y
        m03 = 0

        m10 = 2*x*y - 2*w*z
        m11 = 1     - 2*x**2 - 2*z**2
        m12 = 2*y*z + 2*w*x
        m13 = 0

        m20 = 2*x*z + 2*w*y
        m21 = 2*y*z - 2*w*x
        m22 = 1     - 2*x**2 - 2*y**2
        m23 = 0

        m30 = 0
        m31 = 0
        m32 = 0
        m33 = 1

        return array([
            [m00, m01, m02, m03],
            [m10, m11, m12, m13],
            [m20, m21, m22, m23],
            [m30, m31, m32, m33]
            ])

    #回転行列→オイラー角
    def Matrix2Euler(ary: array) -> array:
        euler = Matrix2Euler()

        euler.x = arcsin(ary[2][1])
        euler.y = arctan2(-ary[2][0], ary[2][2])
        euler.z = arctan2(-ary[0][1], ary[1][1])

        if ary[2][1] == 1:
            euler.x = pi/2
            euler.y = 0
            euler.z = arctan2(ary[1][0], ary[0][0])

        elif ary[2][1] == -1:
            euler.x = -pi/2
            euler.y = 0
            euler.z = arctan(ary[1][0], ary[0][0])

        return euler

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


    '''#クオータニオン→回転行列
    def Quaternion2Matrix(ary: Quaternion) -> array:

    x, y, z, w = ary.x, ary.y, ary.z, ary.w

    m00 = 1     - 2*y**2 - 2*z**2
    m01 = 2*x*y + 2*w*z
    m02 = 2*x*z - 2*w*y
    m03 = 0

    m10 = 2*x*y - 2*w*z
    m11 = 1     - 2*x**2 - 2*z**2
    m12 = 2*y*z + 2*w*x
    m13 = 0

    m20 = 2*x*z + 2*w*y
    m21 = 2*y*z - 2*w*x
    m22 = 1     - 2*x**2 - 2*y**2
    m23 = 0

    m30 = 0
    m31 = 0
    m32 = 0
    m33 = 1

    return array([
        [m00, m01, m02, m03],
        [m10, m11, m12, m13],
        [m20, m21, m22, m23],
        [m30, m31, m32, m33]
        ])

    #回転行列→オイラー角
    def Matrix2Euler(ary: array) -> array:
    euler = Euler()

    euler.x = arcsin(ary[2][1])
    euler.y = arctan2(-ary[2][0], ary[2][2])
    euler.z = arctan2(-ary[0][1], ary[1][1])

    if ary[2][1] == 1:
        euler.x = pi/2
        euler.y = 0
        euler.z = arctan2(ary[1][0], ary[0][0])

    elif ary[2][1] == -1:
        euler.x = -pi/2
        euler.y = 0
        euler.z = arctan(ary[1][0], ary[0][0])

    return euler

    arctanを使えば一発でクオータニオ→オイラー角できるかも

    #class
    class Euler():
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0'''
    