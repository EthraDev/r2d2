import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import json

class DriverNode(Node):
    def __init__(self):
        super().__init__('driver_node')

        self.serial_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        self.subscription = self.create_subscription(
            String,
            'topic_cmd',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        try:
            command = json.loads(msg.data)
            self.get_logger().info(f"Received: {command}")
            payload = json.dumps(command) + '\n'
            self.serial_port.write(payload.encode('utf-8'))
        except Exception as e:
            self.get_logger().error(f"Error: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = DriverNode()
    rclpy.spin(node)
    node.serial_port.close()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
