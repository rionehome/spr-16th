import rclpy
from rclpy.node import Node

from std_msgs.msg import String, Bool
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


from time import sleep

from numpy import *

class Control(Node):
    def __init__(self):
        super().__init__("Control")

       self.publish_velocity = self.create_publisher(Twist, "/turtlebot2/commands/velocity")
        self.create_subscription(
            Odometry,
            "/turtlebot2/odometry",
            self.Odometry,
            10
        )

        self.publish_reset = self.create_publisher(Twist, "turtlebot2/commands/reset_pose")
        self.create_subscription(
            String,
            "/topic/fromCIC",
            self.make_flag_true,
            10
        )
  
    def Odometry(self,angular):
        if self.turn_flag==True:
            self.publish_velocity(1)
        if self.stop(angular)==1:
            self.publish_velocity(0)
            self.publish_CIC() 
            self.reset()   


    def make_flag_true(self,msg):
        if msg != None:
            self.turn_flag=True

    def stop(self):
        #なんか角度を計算して止まる角度か判定
def main():
    rclpy.init()

    node = Control()

    rclpy.spin(node)


if __name__ == "__main__":
    main()