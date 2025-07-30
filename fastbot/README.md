# FastBot Student

## Setup

After robot assembly, these are the steps to setup the robot's software:

1. Install Ubuntu server 24.04 in Raspberry Pi's mini SD card.
2. Clone this repo in `~/git-repo`
3. `/home/fastbot/git-repo/fastbot/docker/install_docker.sh`
4. Add docker to sudo group.
4. Upload `ROSArduinoBridge.ino` to Arduino with Arduino's IDE.
5. Add udev rules for Arduino and LS Lidar.
6. Edit `/boot/config.txt` - `camera_autodetect=0`, `start_x=1` to setup raspicam.

