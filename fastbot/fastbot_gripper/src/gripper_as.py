#!/usr/bin/env python3

import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from control_msgs.action import GripperCommand
import RPi.GPIO as GPIO
import time
from rclpy.executors import MultiThreadedExecutor
from rclpy.action import CancelResponse, GoalResponse


class GripperActionServer(Node):
    def __init__(self):
        super().__init__("gripper_action_server")
        self._action_server = ActionServer(
            self,
            GripperCommand,
            "gripper_command",
            self.execute_callback,
            goal_callback=self.goal_callback,
            handle_accepted_callback=self.handle_accepted_callback,
            cancel_callback=self.cancel_callback,
        )
        self.servo_pin = 19
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        self.p = GPIO.PWM(self.servo_pin, 100)
        # Declare parameters for open and close duty cycles
        self.declare_parameter("close_duty", 6)    # e.g. 90 degrees (closed)
        self.declare_parameter("open_duty", 12)    # e.g. 0 degrees (open)
        self.close_duty = self.get_parameter("close_duty").value
        self.open_duty = self.get_parameter("open_duty").value
        self.get_logger().info(
            f"Gripper Action Server has been started (close_duty={self.close_duty}, open_duty={self.open_duty})"
        )

    def goal_callback(self, goal_request):
        self.get_logger().info("Received goal request")
        # Accept any goal request
        return GoalResponse.ACCEPT

    def handle_accepted_callback(self, goal_handle):
        self.get_logger().info("Goal accepted, executing")
        # Spin off the goal processing to a new thread
        goal_handle.execute()

    def cancel_callback(self, goal_handle):
        self.get_logger().info("Received cancel request")
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        self.get_logger().info(
            f"Executing goal... position: {goal_handle.request.command.position}"
        )

        self.p.start(12)

        if goal_handle.request.command.position < 0:  # close the gripper
            self.p.ChangeDutyCycle(self.close_duty)  # e.g., 90 degrees
            time.sleep(0.5)
            self.get_logger().info("Gripper closed")
        else:  # open the gripper
            self.p.ChangeDutyCycle(self.open_duty)  # e.g., 0 degrees
            time.sleep(0.5)
            self.get_logger().info("Gripper opened")

        self.p.ChangeDutyCycle(0.0)

        # Publish the result
        goal_handle.succeed()

        result = GripperCommand.Result()
        result.effort = 0.0  # Placeholder, you can set a real value if applicable
        result.stalled = False
        result.reached_goal = True
        return result


def main(args=None):
    rclpy.init(args=args)
    gripper_action_server = GripperActionServer()

    # Use a multi-threaded executor if handling multiple clients is needed
    executor = MultiThreadedExecutor()
    rclpy.spin(gripper_action_server, executor=executor)

    # Shutdown
    gripper_action_server.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

