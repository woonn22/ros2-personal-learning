

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class RobotNode(Node):
    def __init__(self):
        super().__init__('robot_node')

        self.publisher = self.create_publisher(
            String,
            '/robot/status',
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.publish_status
        )

        self.count = 0

    def publish_status(self):
        self.count += 1

        msg = String()
        msg.data = f'Robot running: {self.count}'

        self.publisher.publish(msg)
        self.get_logger().info(f'Published: {msg.data}')


def main(args=None):
    rclpy.init(args=args)

    node = RobotNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
