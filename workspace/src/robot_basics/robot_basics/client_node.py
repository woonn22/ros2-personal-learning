import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
from std_msgs.msg import String

import time

class RobotClientNode(Node):
    def __init__(self):
        super().__init__('robot_client_node')

        self.client = self.create_client( Trigger, '/robot/check')

        self.timer = self.create_timer(1.0 , self.send_request)
        self.sent_count = 0
        self.response_count = 0
        
        self.count = 0 

        self.sub_ = self.create_subscription(String ,'/robot/job_result', self.result_callback,10)

        self.pending_future = None

    def result_callback(self,msg):
        self.get_logger().info(f'Topic received: {msg.data}')

    def timer_callback(self):
        self.count += 1
        self.get_logger().info(f'client: COUNT - {self.count}')

    def send_request(self):

        if self.sent_count >= 5:
            self.timer.cancel()
            return
        if ( self.pending_future is not None and not self.pending_future.done()):

            self.get_logger().info( 'Previous service request is still pending')
            return
    
        if (not self.client.service_is_ready()):
            self.get_logger().warn('Service not available')
            return

        self.sent_count += 1

        request = Trigger.Request()

        self.pending_future = self.client.call_async(request)
        #future.add_done_callback(self.response_callback)

        self.request_number = self.sent_count

        self.get_logger().info('Service request, SENT ->')

        #future.add_done_callback(lambda completed_future, number=request_number: self.response_callback(completed_future, number))
        
        self.pending_future.add_done_callback(self.response_callback)


    def response_callback(self,future):
        try:
            response = future.result()
            self.get_logger().info(
                f'Response: {response.message}'
            )
        except Exception as e:
            self.get_logger().error(f'Service failed: {e}')
        finally:
            self.response_count += 1
            self.get_logger().info(f'Responses recevied: {self.response_count}/5')

def main(args=None):
    rclpy.init(args=args)
    node = RobotClientNode()

    try:
        #node.send_request()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
