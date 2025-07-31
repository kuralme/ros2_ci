import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, TimerAction, ExecuteProcess, RegisterEventHandler, Shutdown
from launch.event_handlers import OnProcessExit


def generate_launch_description():
    # Gazebo launch
    gz_node = IncludeLaunchDescription(
        launch_description_source=os.path.join(
            get_package_share_directory(
                'fastbot_gazebo'), 'launch', 'one_fastbot_room.launch.py'
        ),
        launch_arguments={}.items()
    )

    # Action server
    waypoint_action_server = Node(
        package='fastbot_waypoints',
        executable='fastbot_action_server',
        name='waypoint_action_server',
        output={'both': 'log'}
    )

    # Execute the ROS2 testing process
    gtest_cmd = ExecuteProcess(
        cmd=['colcon', 'test', '--packages-select',
             'fastbot_waypoints', '--event-handler', 'console_direct+'],
        output='screen'
    )

    # Delayed to ensure Gazebo is up
    delayed_as = TimerAction(
        period=25.0,
        actions=[waypoint_action_server]
    )

    # Delayed to start the test
    delayed_test = TimerAction(
        period=27.0,
        actions=[gtest_cmd]
    )

    # Register shutdown after tests finish
    shutdown = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=gtest_cmd,
            on_exit=[Shutdown()]
        )
    )

    return LaunchDescription([
        gz_node,
        delayed_as,
        delayed_test,
        shutdown,
    ])
