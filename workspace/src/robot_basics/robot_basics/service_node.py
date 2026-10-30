import rclpy
from rclpy.node import Node

from std_srvs.srv import Trigger

import time
from collections import deque
from std_msgs.msg import String

class RobotServiceNode(Node):
    def __init__(self):
        super().__init__('robot_service_node')
        self.service = self.create_service(Trigger,'/robot/check',self.check_callback)

        self.get_logger().info('Service request ready')

        self.timer = self.create_timer(3.0, self.proceess_callback)
        self.job_queue = deque()
        self.job_id = 0

        self.publicher_ = self.create_publisher( String, '/robot/job_result', 10)

    def check_callback(self, request, response):
        self.job_id += 1
        j = self.job_id

        self.job_queue.append(j)
        self.get_logger().info(f'Request {j} Received')

        response.success = True
        response.message = f'Job {j} Accepted'
        return response
    
    def proceess_callback(self):
        if not self.job_queue:
            return
        j = self.job_queue.popleft()

        self.get_logger().info(f'Procceeing job {j}') 

        msg = String()
        msg.data = f'job {j} completed'
        self.publicher_.publish(msg)

        self.get_logger().info(f'Request {j} completed')
    
    
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


