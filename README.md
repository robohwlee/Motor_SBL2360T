# roboteq_diff_driver

ROS driver for the Roboteq SDC21xx family of motor controllers in a differential-drive configuration.

Subscribes to cmd_vel, publishes to odom, and broadcasts odom tf.

Also publishes sensor data to some ancillary topics including roboteq/voltage, roboteq/current, roboteq/energy, and roboteq/temperature.

Does not require any MicroBasic script to operate.

## Usage

Clone to src directory of catkin workspace, then `catkin_make`.

Requires ROS serial package. If not already installed:
```
sudo apt-get install ros-<dist>-serial
```

Sample launch files in roboteq_diff_driver/launch.


## cmd_vel topic publisher
You can use any type of publisher as an input of motor controller
This driver subscribe /cmd_vel topic as an iput

### teleop keyboard node
```
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
```

### Terminal
```
rostopic pub /cmd_vel geometry_msgs/Twist -r 20 '[1, 0, 0]' '[0, 0, 5]'
```
publish topic as linear velocity / angular velocity


## Authors

* **Chad Attermann** - *Initial work* - [Ecos Technologies](https://github.com/ecostech)

## License

This project is licensed under the BSD License.

