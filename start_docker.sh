#!/bin/bash

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Installing now..."
    sudo apt-get update
    sudo apt-get install -y docker.io docker-compose
    sudo service docker start

    # Enable docker without sudo
    sudo usermod -aG docker $USER
    newgrp docker
    sudo service docker restart

    echo "Docker is installed successfully!"
fi

# Build docker image
docker build -t fastbot-ros2-test .

# Start the container and run the gazebo node
docker run --rm \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    fastbot-ros2-test:latest \
    bash -c "source /colcon_ws/install/setup.bash && ros2 launch fastbot_gazebo test_fastbot_waypoints.launch.py"