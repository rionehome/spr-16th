import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
from time import sleep

from numpy import *

class ControlSystem(Node):
    def __init__(self):
        super().__init__("ControlSystem")

        self.flag_publisher_cerebrum = self.create_publisher(
            String,
            "/cerebrum/command",
            10
        )

        self.create_subscription(
            Odometry,
            "/turtlebot2/odometry",
            self.odometry_subscriber,
            10
        )

        self.velocity_publisher = self.create_publisher(Twist, "/turtlebot2/commands/velocity",10)

        self.reset_publisher = self.create_publisher(Bool, "/turtlebot2/commands/reset_pose", 10)

        self.twist = Twist()

        self.goal_degree = 180

        self.is_running=False

        self.angle=0

    """
    this method calcurates angle by odometry.
    odometry から角度を計算する。
    """
    def get_angle_by_pose(self, pose):
        z = pose.pose.orientation.z 
        w = pose.pose.orientation.w #w,zはクオータニオン表記　

        angle = 0 #初期値

        if z > 0.0:
            angle = -arccos(w)*360 / pi #cosの長さを角度に変換
        else:
            angle =  arccos(w)*360 / pi

        return angle

    """
    this method is to chang angle.
    止まる角度を-180~180の間に変換する。
    """
    def normalize_goal_degree(self, goal_degree):
        goal_degree %= (360 if goal_degree>0 else -360) 

        if -360 < goal_degree < -180:
            goal_degree += 360
        elif  180 < goal_degree < 359:
            goal_degree -= 360

        if goal_degree == 180:  #180度が観測されないのでgoal_degreeが180度になったら179度に変換する
            goal_degree = 179
        if goal_degree == -180:
            goal_degree = -179
        
        print("GOAL: " + str(goal_degree))
        
        return goal_degree

    """
    this method is callback of `/turtlebot2/odometry` topic. 
    this method is judgment of stopping turtlebot
    `/turtlebot2/odometry` トピックのコールバック。
    turtlebot の停止の判定
    """
    def odometry_subscriber(self, msg):
        angle = self.get_angle_by_pose(msg.pose)
        print(angle)
        
        if (self.goal_degree > 0 and angle > self.goal_degree) or (self.goal_degree < 0 and angle < self.goal_degree):
            self.stop_turtlebot()

    """
    the method let turtlebot stopping. 
    turtlebot を止まらせる。
    """
    def stop_turtlebot(self):
        self.twist.angular.z = 0.0
        print("STOP TURTLEBOT")
        self.is_running=False
        self.velocity_publisher.publish(self.twist)

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
    Turtlebot を走らせる。
    """
    def turn_to(self, goal_degree, angular_speed):
        if (not self.is_running) and (angular_speed==0) :     #止まってる際に(速さ)0を連続で送らないようにする
            return

        if angular_speed < 0.0:
            raise Exception("angular_speed must be greater than 0.")

        self.goal_degree = self.normalize_goal_degree(goal_degree)

        self.reset_pose()

        self.twist.linear.x = 0.0
        self.twist.angular.z = angular_speed if self.goal_degree < 0.0 else -1.0 *angular_speed 
        self.is_running = angular_speed != 0

        self.velocity_publisher.publish(self.twist)
        print("running...")

def main():
    rclpy.init()

    node = ControlSystem()

    sleep(1)
    node.turn_to(180, 30.0)

    #rclpy.spin(node)
    #node.destroy_node()
    #rclpy.shutdown()

    sleep(1)
    node.turn_to(90, 20.0)

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()