#!/bin/bash
#Use this to start all parts of the Robot.
sudo gnome-terminal -- sh -c "chmod 666 /dev/ttyUSB0; sleep 1"
sleep 0.1
gnome-terminal -- sh -c "roslaunch rplidar_ros rplidar.launch; bash"
sleep 3
gnome-terminal -- sh -c "roslaunch ros_nodes launcher.launch; bash"
