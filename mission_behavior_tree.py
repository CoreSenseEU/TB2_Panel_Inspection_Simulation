"""
mission_behavior_tree.py
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_system_default
from std_msgs.msg import String


class StartBehaviorTree(Node):
    """Drone interface base node"""

    def __init__(self, namespace):
        super().__init__('start_bt', namespace=namespace)

        self.start_pub = self.create_publisher(
            String, "start", qos_profile_system_default)

        self.start_pub.publish(String())


if __name__ == "__main__":
    rclpy.init()
    start_bt = StartBehaviorTree(namespace="drone0")
    rclpy.spin_once(start_bt, timeout_sec=1)
    rclpy.shutdown()
