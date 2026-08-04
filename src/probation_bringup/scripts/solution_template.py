#!/usr/bin/env python3
import rclpy
from rclpy.node import Node


class GateNavigator(Node):

    def __init__(self):
        super().__init__('gate_navigator')
        # TODO: Implement node initialization


def main(args=None):
    rclpy.init(args=args)
    node = GateNavigator()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
