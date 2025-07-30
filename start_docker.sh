#!/bin/bash

# Build docker image
docker build -t fastbot-ros2-test .

# Start the container and run the gazebo node
docker run --rm \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    fastbot-ros2-test:latest \
    bash -c "source /colcon_ws/install/setup.bash && ros2 launch fastbot_gazebo one_fastbot_room.launch.py"