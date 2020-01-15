import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
from time import sleep
import re
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

        self.create_subscription(
            String,
            '/control_system/command',
            self.subscribe_command,
            10
        )

        self.command_publisher = self.create_publisher(
            String,
            '/cerebrum/command',
            10
        )

        self.velocity_publisher = self.create_publisher(Twist, "/turtlebot2/commands/velocity",10)

        self.reset_publisher = self.create_publisher(Bool, "/turtlebot2/commands/reset_pose", 10)

        self.twist = Twist()

        self.goal_degree = 0

        self.is_running=False

        self.angle=0

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
    this method calcurates angle by odometry.
    odometry から角度を計算する。
    """

    def normalize_goal_degree(self, goal_degree):
        goal_degree %= (360 if goal_degree>0 else -360) 

        if -360 < goal_degree < -180:
            goal_degree += 360
        elif  180 < goal_degree < 359:
            goal_degree -= 360

        if goal_degree == 180:  #180度が観測されないのでgoal_degreeが180度になったら179度に変換する
            goal_degree = 178
        if goal_degree == -180:
            goal_degree = -178
        
        print("GOAL: " + str(goal_degree), flush=True)
        
        return goal_degree
    """
    this method is to chang angle.
    止まる角度を-180~180の間に変換する。
    """

    def odometry_subscriber(self, msg):
        angle = self.get_angle_by_pose(msg.pose)
        self.stop_turtlebot_judgement(angle)
        if self.is_running == True:
            print(angle, flush=True)
    """
    this method is callback of `/turtlebot2/odometry` topic. 
    `/turtlebot2/odometry` トピックのコールバック。
    """

    def subscribe_command(self,msg):
        command,content = self.parse_command(msg.data)
        print(f"got command ${command} width content: ${content}", flush=True)
        if command =="turn":
            self.turn_to(int(content),30.0)
    """
    The method receive command from CIC. 
    CICからのcommandを受け取る。
    """

    def parse_command(self,commad_str):
        m = re.match(r"Command:([a-z]+),Content:(.+):cerebrum",commad_str)
        return m.groups()
    """
    The method resding commad data.
    データの読み取り。
    """

    def stop_turtlebot_judgement(self,turtlebot_angle):
        if self.is_running == True:
            if (self.goal_degree > 0 and turtlebot_angle > self.goal_degree) or (self.goal_degree < 0 and turtlebot_angle < self.goal_degree):
                print(f"goal_degree :{self.goal_degree},angular :{turtlebot_angle}", flush=True)
                self.stop_turtlebot()
    """
    this method is judgment of stopping turtlebot
    turtlebot の停止の判定
    """

    def stop_turtlebot(self):
        self.twist.angular.z = 0.0
        print("STOP TURTLEBOT", flush=True)
        self.is_running=False
        self.velocity_publisher.publish(self.twist)
        self.cerebrum_publisher('Return:0,Content:True')
    """
    the method let turtlebot stopping. 
    turtlebot を止まらせる。
    """

    def cerebrum_publisher(self, message_str):
        msg_str = String()
        msg_str.data = message_str
        self.command_publisher.publish(msg_str)
    """
    The method send data to CIC. 
    CICにデータを送る。
    """

    def reset_pose(self):
        reset_flag = Bool()
        reset_flag.data = True
        self.reset_publisher.publish(reset_flag)
        print("pose rested", flush=True)
    """
    this method set pose of turtlebot to (0, 0, 0).
    turtlebot のポーズを(0, 0, 0)にセットする。
    """

    def turn_to(self, goal_degree, angular_speed):
        if (not self.is_running) and (angular_speed==0) :     #止まってる際に(速さ)0を連続で送らないようにする
            print("if(not self.is_running) and (angular_speed==0)", flush=True)
            return

        if angular_speed <= 0.0:
            raise Exception("angular_speed must be greater than 0.")

        print("received run_to", flush=True)

        self.goal_degree = self.normalize_goal_degree(goal_degree)

        self.reset_pose()

        self.twist.linear.x = 0.0
        self.twist.angular.z = angular_speed if self.goal_degree < 0.0 else -1.0 *angular_speed 
        self.is_running = angular_speed != 0

        self.velocity_publisher.publish(self.twist)
        print("running...", flush=True)
    """
    this method let turtlebot running.
    Turtlebot を走らせる。
    """

def main():
    rclpy.init()

    node = ControlSystem()

    node.turn_to(180,30)
    rclpy.spin(node)

if __name__ == "__main__":
    main()