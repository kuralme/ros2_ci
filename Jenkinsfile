pipeline {
    agent any

    stages {
        stage('Install Docker if Needed') {
            steps {
                sh '''
                if ! command -v docker &> /dev/null; then
                    echo "Docker is not installed. Installing now..."

                    # Clean up old repo
                    echo "Cleaning up old ROS repo sources..."
                    sudo rm -f /etc/apt/sources.list.d/ros-latest.list
                    sudo rm -f /etc/apt/sources.list.d/ros2.list
                    sudo rm -f /etc/apt/sources.list.d/ros.list

                    # Download and dearmor the GPG key (required for signed-by)
                    echo "Downloading and installing ROS GPG key..."
                    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc -o ros.asc
                    gpg --dearmor -o ros.gpg ros.asc
                    sudo mv ros.gpg /usr/share/keyrings/ros-archive-keyring.gpg
                    rm ros.asc

                    # Add the ROS and ROS 2 sources with proper signed-by usage
                    echo "Adding ROS repositories..."
                    echo "deb [signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros/ubuntu focal main" | sudo tee /etc/apt/sources.list.d/ros-latest.list > /dev/null
                    echo "deb [signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu focal main" | sudo tee -a /etc/apt/sources.list.d/ros-latest.list > /dev/null

                    sudo apt-get update
                    sudo apt-get install -y docker.io
                    sudo service docker start
                    echo "Docker is installed successfully!"
                fi
                '''
            }
        }

        stage('Build ROS2 Docker Image') {
            steps {
                sh '''
                cd ~/ros2_ws/src/ros2_ci
                sudo docker build -t fastbot-ros2-test .
                '''
            }
        }

        stage('Run ROS2 Test in Container') {
            steps {
                sh '''
                sudo docker run --rm \
                    --env="DISPLAY=$DISPLAY" \
                    --env="QT_X11_NO_MITSHM=1" \
                    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
                    fastbot-ros2-test:latest \
                    bash -c "source /colcon_ws/install/setup.bash && ros2 launch fastbot_gazebo test_fastbot_waypoints.launch.py"
                '''
            }
        }
    }
}
