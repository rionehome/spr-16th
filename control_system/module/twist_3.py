import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
from time import sleep

from numpy import *

class ControlSystem(Node):
    def __init__(self):
        super().__init__("ControlSystem")
        self.velocity_publisher = self.create_publisher(Twist, "/turtlebot2/commands/velocity",10)

        self.create_subscription(
            Odometry,
            "/turtlebot2/odometry",
            self.odometry_subscriber,
            10
        )

        self.reset_publisher = self.create_publisher(Bool, "/turtlebot2/commands/reset_pose", 10)

        self.twist = Twist()

        self.goal_degree = 500

        self.is_running=False

        self.angle=0

    """
    this method calcurates angle by odometry.
    odometry から角度を計算する。
    """
    def get_angle_by_pose(self, pose):
        z = pose.pose.orientation.z 
        w = pose.pose.orientation.w #w,zはクオータニオン表記　

        self.angle=angle

        self.angle = 0 #初期値

        if z > 0.0:
            self.angle = -arccos(w)*360 / pi #cosの長さを角度に変換
        else:
            self.angle =  arccos(w)*360 / pi
        if self.angle < 0:
            self.angle = self.angle+360

        if self.angle > 180:
            self.angle-=360

        return self.angle
    """
    this method is to chang angle.
    止まる角度を-180~180の間に変換する。
    """
    def shouldStop(self, goal_degree):
        self.goal_degree %= (360 if self.goal_degree>0 else -360) 

        if -360 < self.goal_degree < -180:
            self.goal_degree += 360
        elif  180 < self.goal_degree < 359:
            self.goal_degree -= 360
        
        print(self.goal_degree)
        
        return self.goal_degree

    """
    this method is callback of `/turtlebot2/odometry` topic. 
    `/turtlebot2/odometry` トピックのコールバック。
    """
    def odometry_subscriber(self, msg):
        print(self.get_angle_by_pose(msg.pose))

        if self.shouldStop(self.goal_degree) > 0:   #目標の角度が+の場合
            if self.angle > self.shouldStop(self.goal_degree):  #目標の角度を越えたら速度を0にする
                self.turn_to(0,0.0)
                print("STOP TURTLEBOT")
                self.is_running=False
        if self.shouldStop(self.goal_degree) < 0:   #目標の角度が-の場合
            if self.angle < self.shouldStop(self.goal_degree):  #目標の角度を越えたら速度を0にする
                self.turn_to(0,0.0)
                print("STOP TURTLEBOT")
                self.is_running=False

    """
    this method set pose of turtlebot to (0, 0, 0).
    turtlebot のポーズを(0, 0, 0)にセットする。
    """
    def reset_pose(self):
        reset_flag = Bool()
        reset_flag.data = True
        self.reset_publisher.publish(reset_flag)
        print("pose rested")

    """
    this method let turtlebot running.
    to stop, assign 0.0 to a.
    Turtlebot を走らせる。
    止めるには a に 0.0 を代入。
    """
    def turn_to(self, goal_degree, angular_speed):
        if (not self.is_running) and (angular_speed==0) :     #止まってる際に(速度)0を連続で送らないようにする
            return

        self.goal_degree = goal_degree

        self.reset_pose()

        if angular_speed > 0.0:         #与えられた速度の向きを揃える
            angular_speed = -1*angular_speed

        self.twist.linear.x = 0.0
        self.twist.angular.z = angular_speed if self.shouldStop(self.goal_degree) > 0.0 else -1.0 *angular_speed 
        self.is_running= angular_speed != 0

        if (goal_degree==0) and (angular_speed==0.0):
            self.twist.angular.z=0.0

        self.velocity_publisher.publish(self.twist)
        print('running...')

def main():
    rclpy.init()

    node = ControlSystem()

    sleep(1)
    node.turn_to(500, 30.0)

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()