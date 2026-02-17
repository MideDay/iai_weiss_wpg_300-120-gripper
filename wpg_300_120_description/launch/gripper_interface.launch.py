from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.parameter_descriptions import ParameterValue
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    # ---------------- Robot description paths ----------------
    pkg_path = get_package_share_directory('wpg_300_120_description')
    urdf_file = os.path.join(pkg_path, 'urdf', 'wpg_300-120_meshed.urdf')
    rviz_config_file = os.path.join(pkg_path, 'rviz2', 'rviz.rviz')

    # ---------------- Launch arguments for Griplink ----------------
    griplink_ip_arg = DeclareLaunchArgument(
        "griplink_ip_address",
        description="IP address of the griplink that should be connected to",
        default_value="192.168.1.40"
    )

    griplink_port_arg = DeclareLaunchArgument(
        "griplink_network_port",
        description="The Griplink should be connected to this network port",
        default_value="10001"
    )

    # ---------------- Nodes ----------------

    # Joint State Publisher GUI
    joint_state_pub_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    # Robot State Publisher
    robot_state_pub_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': ParameterValue(
                Command(['cat ', urdf_file]), value_type=str
            )
        }]
    )

    # RViz2
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]
    )

    # Griplink node
    griplink_node = Node(
        package='griplink',
        namespace='griplink_node',
        executable='griplink_node',
        name='griplink_node',
        parameters=[
            {"ip": LaunchConfiguration("griplink_ip_address")},
            {"port": LaunchConfiguration("griplink_network_port")}
        ],
        output='screen'
    )

    # Demo node
    gripper_node = Node(
        package='griplink',
        namespace='demo_node',
        executable='demo_node',
        name='demo_node',
        output='screen'
    )

    # ---------------- LaunchDescription ----------------
    return LaunchDescription([
        griplink_ip_arg,
        griplink_port_arg,
        joint_state_pub_node,
        robot_state_pub_node,
        rviz_node,
        griplink_node,
        gripper_node
    ])