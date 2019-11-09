import rclpy
from rclpy.node import Node

from std_msgs.msg import String

from time import sleep

class CIC(Node):
    def __init__(self):
        super().__init__("CIC")

        self.create_subscription(String, "/cerebrum/command", self.receive, 10)

        self.timer = self.create_timer(2.0, self.state)

        self.data = String()

        sleep(1)

        self.tasks = {
            "1": ["sound",   "count",   "None"],
            "2": ["control", "turn",    180   ],
            "3": ["image",   "capture", "None"],
            "4": ["sound",   "QandA",   5     ],
            "5": ["sound",   "angular", "None"],
            "6": ["sound",   "angular", "None"],
            "7": ["sound",   "angular", "None"],
            "8": ["sound",   "angular", "None"],
            "9": ["sound",   "angular", "None"],
        }

        self.executing = "1"
        self.did = "0"

        print("[*] START SPR", flush=True)

    def state(self):
        for number, task in self.tasks.items():
            self.executing = number
            if self.executing != self.did:
                self.send_with_content(task[0], task[1], task[2])
            self.did = self.executing
            break

    def receive(self, msg):
        flag = msg.data.split(",")[0].split(":")[1]

        number = 0
        tasks = None

        for number, task in self.tasks.items():
            break

        if flag == task[1]:
            print(self.tasks.pop(self.executing), flush=True)

    def send_with_content(self, topic, Command, Content):
        self.sound_system_pub = self.create_publisher(
            String,
            "/"+topic+"_system/command",
            10
        )

        sleep(1)

        print("send to /{0}_system/command Command:{1} Content:{2}".format(topic, Command, Content), flush=True)

        self.data.data = "Command:" + Command + ",Content:" + str(Content) + ":cerebrum"
        self.sound_system_pub.publish(self.data)

def main():
    rclpy.init()

    node = CIC()

    rclpy.spin(node)

if __name__ == "__main__":
    main()
