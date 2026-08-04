from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import AnyLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():
    """
    Probation Task Bringup Launch File
    ===================================
    Starts two processes needed to connect Unity simulation to ROS2:

    1. ROS-TCP-Endpoint  - Listens on port 10000 for the Unity simulation to connect and bridges Unity topics into ROS2.

    2. Foxglove Bridge   - Listens on port 8765. Open Foxglove Studio on your host machine and connect to ws://localhost:8765 to visualise topics and vehicle state.
    """

    probation_bringup_share = FindPackageShare('probation_bringup')
    foxglove_share = FindPackageShare('foxglove_bridge')

    # 1. Unity ROS-TCP Endpoint — bridges Unity simulation into ROS2
    ros_tcp_endpoint_node = Node(
        package='ros_tcp_endpoint',
        executable='default_server_endpoint',
        name='default_server_endpoint',
        output='screen'
    )

    # 2. Foxglove Bridge — visualise ROS2 topics in Foxglove Studio
    foxglove_bridge_launch = IncludeLaunchDescription(
        AnyLaunchDescriptionSource(
            PathJoinSubstitution([foxglove_share, 'launch', 'foxglove_bridge_launch.xml'])
        )
    )

    return LaunchDescription([
        ros_tcp_endpoint_node,
        foxglove_bridge_launch,
    ])
