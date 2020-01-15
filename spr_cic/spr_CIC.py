import rclpy
from rclpy.node import Node

from std_msgs.msg import String

from time import sleep

import re

class CIC(Node):
    def __init__(self):
        super().__init__("CIC")

        self.create_subscription(String, "/cerebrum/command", self.subscribe_command, 10)

        sleep(1)

        self.publisher_dict = {
            "sound": self.create_publisher(String,"/sound_system/command",10), 
            "control": self.create_publisher(String,"/control_system/command",10),
            "image": self.create_publisher(String,"/image_system/command",10),
        }
        self.tasks = [
                ["sound",   "count",        "None"],
                ["control", "turn",         180],
                ["image",   "capture",      "None"],
                ["sound",   "count_people", lambda content: content],
                ["sound",   "QandA",        "None"],
            (*[
                ["sound",   "angular_and_question", "None"],
                ["control", "turn",    0 ],
                ["sound",   "answer", "None"]
            ] * 5) 
        ]
        """
        [タスクのターゲット, コマンド名, 与えるデータ] の配列。

        与えるデータは 単純な値もしくは１つ前のタスクの結果を引数に受け取る関数。

        *([タスク] * 5) の部分は、配列 を 5回繰り返して展開している。
        これで、
            ["sound",   "angular_and_question", "None"],
            ["control", "turn",    lambda d: d ],
            ["sound",   "answer", "None"]
        を5回繰り返すことになる。
        """
        
        self.executing_task_number = -1

        self.latest_return = None


        self.angular =  -1
        self.run_task(0)

    def subscribe_command(self,msg):
        m = re.match(r"Return:([0-9]+),Content:(.+)",msg.data)
        return_str,content = m.groups()
          
        print(f"task {self.executing_task_number} : {str(self.tasks[self.executing_task_number])}is done.",flush=True)
        print(f"return: {return_str}, content:{content}",flush=True)

        self.latest_return = content 

        if len(self.tasks) <= self.executing_task_number:
            return

        self.run_task(self.executing_task_number + 1)

    def run_task(self, task_number): 
        # 実行するタスクが連続でなければ、実行しない
        if task_number  != self.executing_task_number + 1: 
            return
        self.executing_task_number = task_number

        sleep(1)

        target, command, content = self.tasks[task_number]

        # content がcallable(関数)だったら一つ前のtaskの実行結果のcontentを引数に与えて実行した返り値にする
        if callable(content):
            content = content(self.latest_return)

        msg = String()
        msg.data = f"Command:{command},Content:{str(content)}:cerebrum"
        self.publisher_dict[target].publish(msg)
        print(f"task {self.executing_task_number} : {str(self.tasks[self.executing_task_number])} send.",flush=True)


def main():
    rclpy.init()

    node = CIC()

    rclpy.spin(node)

if __name__ == "__main__":
    main()
