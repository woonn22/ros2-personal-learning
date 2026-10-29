import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

class RobotClientNode(Node):
    def __init__(self):
        super().__init__('robot_client_node')

        self.client = self.create_client( Trigger, '/robot/check')

    def send_request(self):
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for Service...')
        
        request = Trigger.Request()
        future = self.client.call_async(request)

        return future

def main(args=None):
    rclpy.init(args=args)
    node = RobotClientNode()

    try:
        future = node.send_request()

        node.get_logger().info(f'Before spin: {future.done()}')

        rclpy.spin_until_future_complete(node, future)

        node.get_logger().info(f'After spin: {future.done()}')

        if future.result() is not None:
            response = future.result()
            node.get_logger().info(
                f'Success: {response.success}, '
                f'Message: {response.message}'
            )
        else:
            node.get_logger().error('Service request failed')

    except KeyboardInterrupt:
        pass
    
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
