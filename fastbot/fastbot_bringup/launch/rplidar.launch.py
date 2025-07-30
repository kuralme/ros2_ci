from launch import LaunchDescription
from launch_ros.actions import Node, LifecycleNode
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, OpaqueFunction


def launch_setup(context, *args, **kwargs):
    """Accept arguments from a parent launch (include)"""
    robot_name = LaunchConfiguration("robot_name").perform(context)

    rplidar_node = Node(
        package="rplidar_ros",
        executable="rplidar_composition",
        name="rplidar_node",
        output="screen",
        parameters=[
            {
                "serial_port": "/dev/rplidar",
                "serial_baudrate": 115200,  # A1 / A2
                "frame_id": robot_name + "_lidar",
                "inverted": False,
                "angle_compensate": True,
            }
        ],
    )

    return [rplidar_node]


def generate_launch_description():

    robot_name_arg = DeclareLaunchArgument("robot_name", default_value="fastbot_1")

    return LaunchDescription([robot_name_arg, OpaqueFunction(function=launch_setup)])
