# ROS2 Continuous Integration

This project implements a Continuous Integration (CI) pipeline for testing a ROS2-based action server that controls the Fastbot, guiding it to predefined 2D waypoints. The testing is carried out inside a Docker container, where the robot simulation runs. The CI pipeline ensures that code changes automatically trigger tests that verify the robot's ability to navigate and reach target waypoints with the correct orientation.

By running the tests in a containerized environment, we can ensure consistency across different setups, making the testing process both scalable and reliable. Jenkins is used to manage the build process, triggering the tests whenever changes are made to the codebase via GitHub pull requests.

This setup helps detect issues early in development, providing confidence that the system will behave as expected when deployed to physical hardware.

## Prerequisites

The build process will automatically install all necessary dependencies. However, the commands and scripts provided in this project are intended to be run on an **Ubuntu** system or any other **Debian-based system**.

## Getting Started

Please note that the Jenkins setup for this project is specifically designed for the Masterclass course and it is not provided within this repository.

To get up and running with Jenkins and the ROS CI pipeline, use the provided installation script to set up and start Jenkins. The script will handle the installation of all necessary dependencies.

```bash
cd webpage_ws
bash start_jenkins.sh
```

Once Jenkins has started, you can access the Jenkins dashboard at the URL provided in the *jenkins__pid__url.txt* file located in home directory.

*Note*: Stopping command for jenkins process is also provided in the file.

Login as \
**username**: *guest* \
**password**: *guest*

## Build process

To trigger the build process, do a simple modification to this repository (like a small text file on Github) and create a **Pull Request**. The build process will automatically start once the PR is created and accepted.

**Monitoring the Build Process**

As a guest user, you can monitor the status of the build job. Navigate to the **Dashboard** and select **FastbotWaypointsTest** on the list. Click on the ongoing job under build section to monitor the build process, provides view of the **Console Output** including logs for the Docker build, test execution, and results.
