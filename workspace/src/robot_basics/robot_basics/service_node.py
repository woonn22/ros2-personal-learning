import rclpy
from rclpy.node import Node

from std_srvs.srv import Trigger

class RobotServiceNode(Node):
    def __init__(self):
        super().__init__('robot_service_node')
        self.service = self.create_service(Trigger,'/robot/check',self.check_callback)

        self.get_logger().info('Service request ready')

    def check_callback(self, request,response):
        self.get_logger().info('Service request received')
        response.success = True
        response.message = 'Robot is running normally'

        return response
    
def main(args=None):
    rclpy.init(args=args)
    node = RobotServiceNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()


