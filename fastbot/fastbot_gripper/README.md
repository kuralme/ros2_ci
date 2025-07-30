#  Gripper Servo Motor Calibration Guide

## Requirements
Before starting, ensure you have the necessary packages installed:

```bash
sudo apt install python3-pip
pip install RPi.GPIO
```

## Safe Operating Ranges
For our 6V hobby servos, these are the recommended duty cycle ranges after testing them:

### Standard Values
- **Middle Position (90°)**: 12.5%
- **Minimum (towards 0°)**: 5.0%
- **Maximum (towards 180°)**: 20.0%

### Initial Code Values
```python
# Start with these conservative values
self.close_duty = 10.0  # closed position (gripping BotBox cube)
self.open_duty = 20.0  # open position
```

## Testing Procedure

### Prepare Servo

1. Unscrew servo from gripper.
2. Attach cross servo horn to servo, making sure it is aligned with the hub.
3. Mark the top horn (away from motor center) with visible tape.
4. Fix servo in place (i.e. duct tape).

### Calibration Steps

5. **Run `servo_calibration.py`: `python3 ~/git-repo/fastbot/fastbot_gripper/src/servo_calibration.py`

6. **Start at middle position**
   - Begin with 12.5% duty cycle
   - This is the safest starting point

7. **Test minimum position**
   - Gradually decrease from 12.5% towards 5.0%
   - Move in 0.5% increments
   - Stop if servo strains

8. **Test maximum position**
   - Gradually increase from 12.5% towards 20.0%
   - Move in 0.5% increments
   - Stop if servo strains

9. 🚨 **Set servo to minimum position: 5.0%** 🚨

### Reattach servo to gripper

10. Exit program.
11. Remove servo horn.
12. Place and screw servo to gripper **in completely closed position.**
13. Re-run `python3 ~/git-repo/fastbot/fastbot_gripper/src/servo_calibration.py`
14. Run maximum/minimum position a couple of times and verify everything moves correctly.
15. From maximum position, go down in 0.5 increments until it lightly grasps BotBox cube. Check that you can pull back the cube with the grip. 
   * Note that position, which will be `close_duty`, the minimum closed position for the gripper.
16. Stop FastBot docker container if it's running.
17. Edit duty cycle parameters in `~/git-repo/fastbot/docker/volumes/bringup.launch.xml`
   * `close_duty` is the position where cube was grasped (Usually 10).
   * `open_duty` is the maximum position (Usually 20).
18. Start FastBot docker container.
19. Test gripper through ROS 2 actions.


### Safety Guidelines
- Always start from middle position (12.5%)
- Make small adjustments (0.5% increments)
- Listen for straining/grinding sounds
- Stop immediately if:
    - Servo makes unusual noises
    - Movement seems forced
    - Servo gets hot
- Verify power supply is adequate
- Check wiring before assuming range issues


## Current Implementation
The default values in the code (10% to 20%) are within reasonable range after testing.

### Parameter Adjustment
To modify the servo range:
1. Stop docker container: `docker compose -f ~/git-repo/fastbot/docker/docker-compose.yaml down`
2. Edit duty cycle parameters in `~/git-repo/fastbot/docker/volumes/bringup.launch.xml`
3. Start docker container `docker compose -f ~/git-repo/fastbot/docker/docker-compose.yaml up`

## ROS 2 Action
To open/close gripper through ROS 2:
* Open
```
ros2 action send_goal /gripper_command control_msgs/action/GripperCommand "command:
  position: 0.1
  max_effort: 0.0"
```
* Close
ros2 action send_goal /gripper_command control_msgs/action/GripperCommand "command:
  position: -0.1
  max_effort: 0.0"