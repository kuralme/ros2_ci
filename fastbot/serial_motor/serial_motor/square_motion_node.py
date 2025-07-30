import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from math import sqrt, pow, atan2


class SquareMotionNode(Node):
    def __init__(self):
        super().__init__("square_motion_node")

        # Publishers and Subscribers
        odom_topic = "fastbot/odom"
        cmd_vel_topic = "fastbot/cmd_vel"
        self.cmd_vel_pub = self.create_publisher(Twist, cmd_vel_topic, 10)
        self.odom_sub = self.create_subscription(
            Odometry, odom_topic, self.odom_callback, 10
        )

        # Parameters for movement
        self.side_length = 0.3  # 30 cm
        self.linear_speed = 0.1  # m/s
        self.angular_speed = 0.8  # rad/s
        self.state = "MOVE_FORWARD"  # State to track motion stages
        self.start_position = None
        self.target_yaw = None

        # Initialize position and orientation
        self.position = None
        self.orientation = None

        # Timer to run control loop
        self.timer = self.create_timer(0.1, self.control_loop)

    def odom_callback(self, msg):
        # Extract the robot's position and orientation from odometry
        self.position = msg.pose.pose.position
        self.orientation = msg.pose.pose.orientation

    def calculate_distance(self, start, end):
        return sqrt(pow(end.x - start.x, 2) + pow(end.y - start.y, 2))

    def calculate_yaw(self):
        # Simplified 2D yaw calculation
        siny = 2.0 * (
            self.orientation.w * self.orientation.z
            + self.orientation.x * self.orientation.y
        )
        cosy = 1.0 - 2.0 * (self.orientation.y**2 + self.orientation.z**2)
        return atan2(siny, cosy)

    def control_loop(self):
        twist = Twist()

        # Ensure position is initialized by odom_callback
        if self.position is None:
            self.get_logger().warn("Waiting for initial position data...")
            return

        if self.state == "MOVE_FORWARD":
            if self.start_position is None:
                self.start_position = self.position

            distance_traveled = self.calculate_distance(
                self.start_position, self.position
            )

            if distance_traveled < self.side_length:
                twist.linear.x = self.linear_speed
            else:
                twist.linear.x = 0.0
                self.state = "TURN"
                self.target_yaw = (
                    self.calculate_yaw() + 1.57
                )  # Approx. 90 degrees in radians

        elif self.state == "TURN":
            current_yaw = self.calculate_yaw()
            yaw_diff = abs(current_yaw - self.target_yaw)

            if yaw_diff > 0.1:
                twist.angular.z = self.angular_speed
            else:
                twist.angular.z = 0.0
                self.state = "MOVE_FORWARD"
                self.start_position = None  # Reset for next side

        # Publish command
        self.cmd_vel_pub.publish(twist)


def main(args=None):
    rclpy.init(args=args)

    node = SquareMotionNode()

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
