import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MonitorNode(Node):
    def __init__(self):
        super().__init__('monitor_node')
        self.subscription = self.create_subscription(String,'/robot/status',self.status_callback,10)
     
    def status_callback(self,msg):
        self.get_logger().info(f'Received: {msg.data}')
		
def main(args=None):
    rclpy.init(args=args)
    node = MonitorNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
if __name__ == '__main__' :
    main()
