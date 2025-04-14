import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json

class ManagerNode(Node):
    def __init__(self):
        super().__init__('manager_node')
        self.publisher_ = self.create_publisher(String, 'topic_cmd', 10)
        self.timer = self.create_timer(1.0, self.publish_command)

    def publish_command(self):
        command = {'left': 100, 'right': 120}
        msg = String()
        msg.data = json.dumps(command)
        self.publisher_.publish(msg)
        self.get_logger().info(f"Published: {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = ManagerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
