FROM osrf/ros:humble-desktop-full
ENV LANG en_US.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
SHELL [ "/bin/bash" , "-c" ]

# Install system and ROS 2 dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    python3-colcon-common-extensions \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-xacro \
    ros-humble-tf2* \
    ros-humble-joint-state-publisher \
    && rm -rf /var/lib/apt/lists/*

# Create ROS2 workspace
RUN mkdir -p /colcon_ws/src
COPY ./fastbot/fastbot_gazebo /colcon_ws/src/fastbot_gazebo
COPY ./fastbot/fastbot_description /colcon_ws/src/fastbot_description
COPY ./fastbot_waypoints /colcon_ws/src/fastbot_waypoints

RUN source /opt/ros/humble/setup.bash \
 && cd /colcon_ws \
 && colcon build
WORKDIR /colcon_ws
