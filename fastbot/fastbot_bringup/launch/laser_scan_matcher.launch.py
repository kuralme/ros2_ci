#!/usr/bin/python3
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.actions import OpaqueFunction
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.conditions import IfCondition


def launch_setup(context, *args, **kwargs):
    ####### DATA INPUT ##########
    use_sim_time = LaunchConfiguration("use_sim_time").perform(context)
    # This is to access the argument variables. Otherwise we cant access the values
    robot_name = LaunchConfiguration("robot_name").perform(context)

    odometry_node = Node(
        package="ros2_laser_scan_matcher",
        condition=IfCondition(PythonExpression(["not ", use_sim_time])),
        parameters=[
            {
                "base_frame": robot_name + "_base_link",
                "odom_frame": robot_name + "_odom",
                "laser_frame": robot_name + "_lidar_frame",
                "robot_name": robot_name,
                "publish_odom": robot_name + "/odom",
                "publish_tf": True,
            }
        ],
        remappings=[("/scan", robot_name + "/scan")],
        executable="laser_scan_matcher",
        name="odometry_publisher",
    )

    return [odometry_node]


def generate_launch_description():

    robot_name_arg = DeclareLaunchArgument("robot_name", default_value="fastbot_X")
    use_sim_time_arg = DeclareLaunchArgument(name="use_sim_time", default_value="False")

    return LaunchDescription(
        [robot_name_arg, use_sim_time_arg, OpaqueFunction(function=launch_setup)]
    )
