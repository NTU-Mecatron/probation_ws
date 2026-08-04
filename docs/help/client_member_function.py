from mavros_msgs.srv import SetMode
import rclpy
from rclpy.node import Node


class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(SetMode, '/mavros/set_mode')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = SetMode.Request()

    def send_request(self):
        self.req.custom_mode = 'GUIDED'
        return self.cli.call_async(self.req)


def main():
    rclpy.init()

    minimal_client = MinimalClientAsync()
    future = minimal_client.send_request()
    rclpy.spin_until_future_complete(minimal_client, future)
    response = future.result()
    if response.mode_sent:
        minimal_client.get_logger().info('Service call successful')
    else:
        minimal_client.get_logger().info('Service call failed')

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
