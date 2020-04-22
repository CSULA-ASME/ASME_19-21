#! /usr/bin/env python
import rospy
from ros_nodes.msg import smach2controls
from ros_nodes.msg import sensors2smach
from ros_nodes.msg import cameras2smach
from ros_nodes.msg import lidar2smach
from ros_nodes.msg import controls2smach

def lidar_2_smach(lidar_data):
	print(lidar_data)

def sensors_2_smach(sensors_data):
        print(sensors_data)

def cameras_2_smach(cameras_data):
	the_something = cameras_data.something
	print(cameras_data)

def controls_2_smach(controls_feedback):
	print (controls_feedback)

while True:
	rospy.init_node('SMACH')
	smach_2_controls_pub = rospy.Publisher('smach2controls', smach2controls, queue_size=10)
	rospy.Subscriber('sensors2smach', sensors2smach, sensors_2_smach)
	rospy.Subscriber('cameras2smach', cameras2smach, cameras_2_smach)
	rospy.Subscriber('lidar2smach', lidar2smach, lidar_2_smach)
	rospy.Subscriber('controls2smach', controls2smach, controls_2_smach)
	rate = rospy.Rate(10)
	final_message = smach2controls()
	while not rospy.is_shutdown():
		#State Machine Here
		final_message.yaw_input = 1
		final_message.yaw_setpoint = 2
                final_message.distance_input = 3
                final_message.distance_setpoint = 5
		smach_2_controls_pub.publish(final_message)
		rate.sleep()

	else:
		exit()
