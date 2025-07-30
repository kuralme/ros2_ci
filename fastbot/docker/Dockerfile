# Stage 1: Build Stage
FROM ros:humble-ros-core AS build_stage

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    python3-colcon-common-extensions \
    git \
    python3-rosdep \
    ros-humble-tf2-ros \
    ros-humble-tf2-geometry-msgs \
    ros-humble-pcl-conversions \
    ros-humble-diagnostic-updater \
    libboost-all-dev \
    libpcap-dev \
    && rm -rf /var/lib/apt/lists/*

# Clone the repositories for the project
WORKDIR /root/ros2_ws/src
ARG CACHEBUST=1
RUN git clone -b student https://bitbucket.org/theconstructcore/fastbot.git \
    && git clone https://bitbucket.org/theconstructcore/lslidar_ros2_driver.git

# Use /bin/bash for the next RUN command
SHELL ["/bin/bash", "-c"]

# Build the workspace
WORKDIR /root/ros2_ws
RUN source /ros_entrypoint.sh && colcon build --executor sequential

# Stage 2: Runtime Stage (final image)
FROM ros:humble-ros-core

# Install runtime dependencies (only those needed to run the application)
RUN apt-get update && apt-get install -y \
    ros-humble-tf2-ros \
    ros-humble-tf2-geometry-msgs \
    ros-humble-diagnostic-updater \
    ros-humble-rmw-cyclonedds-cpp \
    ros-humble-xacro \
    ros-humble-robot-state-publisher \
    ros-humble-v4l2-camera \
    ros-humble-image-transport-plugins \
    ros-humble-control-msgs \
    ros-humble-teleop-twist-keyboard \
    python3-pip \
    i2c-tools \
    libgpiod2 \
    libpcap0.8 \
    libboost-thread1.74.0 \
    && rm -rf /var/lib/apt/lists/* \
    && pip install RPi.GPIO pyserial adafruit-circuitpython-ina219 smbus2   

# Copy the build artifacts from the build stage
COPY --from=build_stage /root/ros2_ws /root/ros2_ws

# Set the entrypoint for the runtime container
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]
