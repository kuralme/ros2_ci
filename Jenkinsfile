pipeline {
    agent any

    stages {
        stage('Install Docker if Needed') {
            steps {
                sh '''
                if ! command -v docker &> /dev/null; then
                    echo "Docker is not installed. Installing now..."

                    # Remove both ROS1 & ROS2 apt sources
                    sudo rm -f /etc/apt/sources.list.d/ros-latest.list
                    sudo rm -f /etc/apt/sources.list.d/ros2-latest.list

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
