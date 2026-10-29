import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time


class RobotNode(Node):
    def __init__(self):
        super().__init__('robot_node')

        self.publisher = self.create_publisher( String,'/robot/status',10)

        self.timer1 = self.create_timer(0.5,self.publish_status)
        self.timer2 = self.create_timer(1.0,self.monitor_status)

        self.count = 0

    def publish_status(self):
        self.get_logger().info('Timer A : Start')

        time.sleep(2.0)

        self.count += 1

        msg = String()
        msg.data = f'Robot running: {self.count}'
        self.publisher.publish(msg)

        self.get_logger().info('Timer A : End')

    def monitor_status(self):
        self.get_logger().info('Timer B : CHECK')
        


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
