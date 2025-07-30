#!/bin/bash
set -e
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export CYCLONEDDS_URI=/var/lib/theconstruct.rrl/cyclonedds.xml
# setup ros2 environment
source "/opt/ros/$ROS_DISTRO/setup.bash" --
source "/root/ros2_ws/install/setup.bash"
exec "$@"
